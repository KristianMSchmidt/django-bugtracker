from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Project
from notifications.models import Notification


@receiver(m2m_changed, sender=Project.users.through)
def create_notifications(action, instance, model, pk_set, **kwargs):
    """
    Notify users when they are enrolled in or disenrolled from project
    """
    if action == 'pre_remove':
        for pk in pk_set:
            Notification.objects.create(
                recipient=model.objects.get(pk=pk), 
                sender=model.objects.get(pk=pk), #skal ændres
                type=Notification.Type.PROJECT_DISENROLLMENT,
                project=instance
            )
    if action == 'post_add':
        for pk in pk_set:
            Notification.objects.create(
                recipient=model.objects.get(pk=pk), 
                sender=model.objects.get(pk=pk), #skal ændres
                type=Notification.Type.PROJECT_ENROLLMENT,
                project=instance
            )
