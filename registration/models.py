# registration/models.py
from django.db import models
from login.models import Role, TimeStampedModel
from django.contrib.auth.hashers import make_password

class UserAccount(TimeStampedModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")

    def save(self, *args, **kwargs):
        # Hash password before saving
        if not self.pk:  # only hash when creating new user
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.role.name})"
