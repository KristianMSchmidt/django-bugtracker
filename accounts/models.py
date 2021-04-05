from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Role choices
    DEVELOPER, ADMIN, PROJECT_MANAGER = 'D', 'A', 'PM'
    ROLE_CHOICES = [(DEVELOPER, 'Developer'), (ADMIN, 'Admin'),
                        (PROJECT_MANAGER, 'Project Manager')]
    role = models.CharField(max_length=2,
                            choices=ROLE_CHOICES,
                            default=DEVELOPER,
                            )
