from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse 

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, default="")
    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.id)])
    
