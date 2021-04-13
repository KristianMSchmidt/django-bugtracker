from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False)
    
    class Role(models.IntegerChoices):
        DEVELOPER = 1
        ADMIN = 2 
        PROJECT_MANAGER = 3

    role = models.PositiveSmallIntegerField(
        choices=Role.choices, null=True, default=Role.DEVELOPER
    )

    # Model methods
    def is_developer(self):
        return self.role == self.Role.DEVELOPER

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_pm(self):
        return self.role == self.Role.PROJECT_MANAGER

    def get_absolute_url(self):
        return reverse("user_detail", args=[self.username])
