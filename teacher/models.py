from django.db import models

from core.models import TimeStampedModel
from registration.models import UserAccount

# Create your models here.
class TeacherProfile(TimeStampedModel):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="teacher_profile")
    department = models.CharField(max_length=100)
    subjects_taught = models.CharField(max_length=255)  # e.g., "Math, Science"
    hire_date = models.DateField()
    employee_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Teacher: {self.user.full_name}, Department: {self.department}"
    class Meta:
        db_table = "teachers_details" 