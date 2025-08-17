from django.utils import timezone
from registration.models import UserAccount
from fastapi import HTTPException
from django.contrib.auth.hashers import make_password
from role.models import Role
from schemas.schema import UserUpdateBaseSchema
from student.models import Students
from teacher.models import TeacherProfile

class RegistrationController:

    def register_user(data):
        if UserAccount.objects.filter(email=data.email).exists():
            raise HTTPException(status_code=400, detail="Email already registered")

        try:
            role = Role.objects.get(id=data.role_id, is_active=True)
        except Role.DoesNotExist:
            raise HTTPException(status_code=404, detail="Role not found")

        hashed_password = make_password(data.password)

        # Create base user
        user = UserAccount.objects.create(
            email=data.email,
            password=hashed_password,
            full_name=data.full_name,
            role=role,
            phone=data.phone,
            address=data.address,
            is_active=True
        )

        # Register role-specific profile
        if role.name == "student":
            required_fields = [data.grade, data.section, data.date_of_birth, data.roll_number]
            if not all(required_fields):
                raise HTTPException(status_code=400, detail="Missing student profile fields")
            
            Students.objects.create(
                user=user,
                grade=data.grade,
                section=data.section,
                date_of_birth=data.date_of_birth,
                mother_name=data.mother_name,
                mother_contact=data.mother_contact,
                father_name=data.father_name,
                father_contact=data.father_contact,
                roll_number=data.roll_number
            )

        elif role.name == "teacher":
            required_fields = [data.department, data.subjects_taught, data.hire_date, data.employee_id]
            if not all(required_fields):
                raise HTTPException(status_code=400, detail="Missing teacher profile fields")
            
            TeacherProfile.objects.create(
                user=user,
                department=data.department,
                subjects_taught=data.subjects_taught,
                hire_date=data.hire_date,
                employee_id=data.employee_id
            )

        else:
            raise HTTPException(status_code=400, detail="Unsupported role for registration")

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": role.name,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "is_active": user.is_active
        }

    def update_user(user_id: int, data: UserUpdateBaseSchema):
        try:
            user = UserAccount.objects.get(id=user_id, is_active=True)
        except UserAccount.DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")

        # Update User Details (email, password, full_name, role)
        if data.email:
            if UserAccount.objects.filter(email=data.email).exclude(id=user_id).exists():
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = data.email

        if data.password:
            user.password = make_password(data.password)

        if data.full_name:
            user.full_name = data.full_name

        if data.role_id:
            try:
                role = Role.objects.get(id=data.role_id, is_active=True)
                user.role = role
            except Role.DoesNotExist:
                raise HTTPException(status_code=404, detail="Role not found")

        user.updated_by = data.updated_by
        user.updated_at = timezone.now()
        user.save()

        # Update Student-Specific Data (if role is student)
        if user.role.name == "student":
            student_data = data.dict(exclude_unset=True)  # Get the updated fields
            if "phone" in student_data or "grade" in student_data or "section" in student_data:
                student = Students.objects.get(user=user)
                if "phone" in student_data:
                    student.phone = student_data["phone"]
                if "grade" in student_data:
                    student.grade = student_data["grade"]
                if "section" in student_data:
                    student.section = student_data["section"]
                if "date_of_birth" in student_data:
                    student.date_of_birth = student_data["date_of_birth"]
                student.save()

        # Update Teacher-Specific Data (if role is teacher)
        if user.role.name == "teacher":
            teacher_data = data.dict(exclude_unset=True)
            if "subject" in teacher_data or "department" in teacher_data:
                teacher = TeacherProfile.objects.get(user=user)
                if "subject" in teacher_data:
                    teacher.subject = teacher_data["subject"]
                if "department" in teacher_data:
                    teacher.department = teacher_data["department"]
                teacher.save()

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.name,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "is_active": user.is_active
        }