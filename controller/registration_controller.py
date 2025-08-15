# controller/registration_controller.py
from datetime import timezone
from registration.models import UserAccount
from fastapi import HTTPException
from django.contrib.auth.hashers import make_password
from role.models import Role

class RegistrationController:

    def register_user(email: str, password: str, full_name: str, role_id: int, created_by: str = None):
        if UserAccount.objects.filter(email=email).exists():
            raise HTTPException(status_code=400, detail="Email already registered")
        try:
            role = Role.objects.get(id=role_id, is_active=True)
        except Role.DoesNotExist:
            raise HTTPException(status_code=404, detail="Role not found")

        user = UserAccount.objects.create(
            email=email,
            password=make_password(password),
            full_name=full_name,
            role=role,
            created_by=created_by
        )
        return user
    
    def update_user(user_id: int, email: str = None, password: str = None,
                    full_name: str = None, role_id: int = None, updated_by: str = None):
        try:
            user = UserAccount.objects.get(id=user_id, is_active=True)
        except UserAccount.DoesNotExist:
            raise HTTPException(status_code=404, detail="User not found")

        if email:
            if UserAccount.objects.filter(email=email).exclude(id=user_id).exists():
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = email

        if password:
            user.password = make_password(password)

        if full_name:
            user.full_name = full_name

        if role_id:
            try:
                role = Role.objects.get(id=role_id, is_active=True)
                user.role = role
            except Role.DoesNotExist:
                raise HTTPException(status_code=404, detail="Role not found")

        user.updated_by = updated_by
        user.updated_at = timezone.now()
        user.save()
        return user
