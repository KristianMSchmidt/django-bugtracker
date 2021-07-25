from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Ticket, TicketComment
from notifications.models import Notification


@receiver(pre_save, sender=Ticket)
def create_notification_when_editing_existing_ticket(instance, *args, **kwargs):
    new_developer = instance.developer
    if instance.pk:  # We are updating an existing ticket
        old_developer = Ticket.objects.get(pk=instance.pk).developer
        if old_developer != new_developer:
            Notification.objects.create(
                recipient=old_developer,
                sender=instance.updated_by,
                type=Notification.Type.TICKET_UNASSIGNMENT,
                ticket=instance
            )
            Notification.objects.create(
                recipient=new_developer,
                sender=instance.updated_by,
                type=Notification.Type.TICKET_ASSIGNMENT,
                ticket=instance
            )


@receiver(post_save, sender=Ticket)
def create_notifications_when_new_ticket(instance, created, *args, **kwargs):
    if created:  # a new ticket has been created
        Notification.objects.create(
            recipient=instance.developer,
            sender=instance.submitter,
            type=Notification.Type.TICKET_ASSIGNMENT,
            ticket=instance
        )


@receiver(post_save, sender=TicketComment)
def create_notifications_when_new_ticket_comments(instance, created, *args, **kwargs):
    if created:  # a new ticket comment been created
        Notification.objects.create(
            recipient=instance.ticket.developer,
            sender=instance.commenter,  # skal ændres
            type=Notification.Type.NEW_TICKET_COMMENT,
            ticket=instance.ticket
        )
