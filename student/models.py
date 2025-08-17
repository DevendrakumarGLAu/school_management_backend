from django.db import models

from core.models import TimeStampedModel
from registration.models import UserAccount

# Create your models here.
class Students(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="student_profile")
    grade = models.CharField(max_length=10)  # "Grade 1", "Grade 2", etc.
    section = models.CharField(max_length=10)  # "A", "B", "C" section
    date_of_birth = models.DateField()
    mother_name = models.CharField(max_length=100)
    mother_contact = models.CharField(max_length=15)
    father_name = models.CharField(max_length=100)
    father_contact = models.CharField(max_length=15)
    roll_number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.grade} {self.section}"
    
    class Meta:
        db_table = 'student_details'
        