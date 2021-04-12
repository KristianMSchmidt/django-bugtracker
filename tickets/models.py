
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from projects.models import Project
from django.utils.translation import gettext_lazy as _


class Ticket(models.Model):

    title = models.CharField(max_length=200, unique=True, default="Ticket #")
    description = models.CharField(max_length=300, default="Default ticket description")
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        related_name='tickets',
        null=True,
        blank=True
    )
    submitter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='submitter_set'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_at = models.DateTimeField(auto_now=True, null=True)
    developer = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='developer_set',
        blank=True
    )
    
    class Status(models.IntegerChoices):
        OPEN = 1
        INFO_REQUIRED = 2
        IN_PROGRESS = 3
        CLOSED = 4
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, null=True, default=Status.OPEN
    )
    
    class Priority(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        URGENT = 4
    priority = models.IntegerField(
        choices=Priority.choices, null=True, default=Priority.LOW
    )
    
    class Type(models.IntegerChoices):
        FEATURE_REQUEST = 1
        BUG = 2, _('Bug/Error')
        OTHER = 3 

    type = models.PositiveSmallIntegerField(
        choices=Type.choices, null=True, default=Type.BUG
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ticket_detail", args=[str(self.id)])

    # status methods
    def is_open(self):
        return self.status == self.status.OPEN

    def is_in_progress(self):
        return self.status == self.status.IN_PROGRESS

    def is_closed(self):
        return self.status == self.status.CLOSED

    def info_required(self):
        return self.status == self.status.INFO_REQUIRED

    # priority methods

    def priority_is_low(self):
        return self.priority == self.priority.LOW

    def priority_is_medium(self):
        return self.priority == self.priority.MEDIUM

    def priority_is_high(self):
        return self.priority == self.priority.HIGH

    def priority_is_urgent(self):
        return self.priority == self.priority.URGENT

    # type methods

    def type_is_bug(self):
        return self.type == self.type.BUG

    def type_is_feature_request(self):
        return self.type == self.type.FEATURE_REQUEST

    def type_is_other(self):
        return self.type == self.type.OTHER

    #def is_open_or_closed(self):
    #    return self.status in {self.OPEN, self.CLOSED}


class TicketEvent(models.Model):
    # Event type choices
    CREATED = 1
    STATUS = 2
    PRIORITY = 3
    TYPE = 4
    DEVELOPER = 5
    TITLE = 6
    DESCRIPTION = 7
    DELETED = 8
    CHANGED_PROPERTY_CHOICES = [
        (CREATED, 'TicketCreated'),
        (STATUS, 'StatusChange'), 
        (PRIORITY, 'PriorityChange'),
        (TYPE, 'TypeChange'),
        (DEVELOPER, 'DeveloperChange'),
        (TITLE, 'TitleChange'),
        (DESCRIPTION, 'DescriptionChange'),
        (DELETED, 'TicketDeleted')
        ]
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        null=True
    )
    property_changed = models.PositiveSmallIntegerField(
        choices = CHANGED_PROPERTY_CHOICES,
    )
    old_value = models.CharField(max_length=200, default="")
    new_value = models.CharField(max_length=300, default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # Using a separate database to store choices is only recommended when rows are changing dynamiccally.  I do it the recommeneded way by adding choices
