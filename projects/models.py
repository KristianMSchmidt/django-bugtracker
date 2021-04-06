from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse 

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=301, default="")
    
    # one-to-many
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete = models.SET_NULL,
        null=True,
        #related_name='created_by'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    users = models.ManyToManyField(get_user_model(), related_name='projects') 
    # by default: related_name = 'project_set'    ->   someuser.projects_set.all()  giver alle projekter til given bruger
    # someproject.users  --> giver alle users til projektet 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.id)])
    
