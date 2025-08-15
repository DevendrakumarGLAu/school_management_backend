from django.db import models

# Create your models here.
class UserAccount(models.Model):
    # username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.email} ({self.id})"
    
    class Meta:
        db_table = "user_account" 
