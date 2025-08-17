# sidebar/models.py
from django.db import models
from core.models import TimeStampedModel
from role.models import Role

class Sidebar(TimeStampedModel):
    title = models.CharField(max_length=100)
    path = models.CharField(max_length=255)  # route path
    icon = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    roles = models.ManyToManyField(Role, related_name='sidebars')  # permission-based

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Sidebar_routes" 
