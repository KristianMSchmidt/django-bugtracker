from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Role choices
    DEVELOPER, ADMIN, PROJECT_MANAGER = 1, 2, 3
    ROLE_CHOICES = [(DEVELOPER, 'Developer'), (ADMIN, 'Admin'),
                        (PROJECT_MANAGER, 'Project Manager')]
    role = models.PositiveSmallIntegerField(
                            choices=ROLE_CHOICES,
                            default=DEVELOPER,
                            null=True,
                            )
    def is_developer(self):
        return self.role == self.DEVELOPER

    def is_admin(self):
        return self.role == self.ADMIN

    def is_developer(self):
        return self.role == self.PROJECT_MANAGER
