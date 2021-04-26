from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps


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

  # override save method to create ticket events & notifications

    def save(self, actor=None, *args, **kwargs):
        Notification = apps.get_model('notifications', 'Notification') # to avoid circular imports
        if self.pk: # we are updating an existing account
            user_before_save = CustomUser.objects.get(pk=self.pk)
            if user_before_save.role != self.role:
                Notification.objects.create(
                    recipient=self,
                    sender=actor,
                    type=Notification.Type.ROLE_UPDATE,
                    new_role=self.role
            )
        
        super().save(*args, **kwargs)


