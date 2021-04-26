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
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='updater_set'
    )
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

    # override save method to create ticket events
    def save(self, request=None, *args, **kw):
        if self.pk is not None: # we are updating an existing ticket                    
            orig = Ticket.objects.get(pk=self.pk)
            for field_name in ('title', 'description', 'developer', 'status', 'type', 'priority'):
                try:
                    old_value = getattr(orig, f"get_{field_name}_display")()
                    new_value = getattr(self, f"get_{field_name}_display")()
                except:
                    old_value = str(getattr(orig, field_name))
                    new_value = str(getattr(self, field_name))
                if old_value != new_value:
                    TicketEvent.objects.create(
                        user=request.user,
                        ticket=self,
                        property_changed=getattr(
                            TicketEvent.ChangedProperty, field_name.upper() + '_CHANGE'),
                        old_value=old_value,
                        new_value=new_value
                    )
        super(Ticket, self).save(*args, **kw)

class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE
    )
    commenter = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL
    )
    message = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse("ticket_detail", args=[self.ticket.id])

class TicketEvent(models.Model):
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

    # Event type choices
    class ChangedProperty(models.IntegerChoices):
        STATUS_CHANGE = 1
        PRIORITY_CHANGE = 2
        TYPE_CHANGE = 3
        DEVELOPER_CHANGE = 4
        TITLE_CHANGE = 5
        DESCRIPTION_CHANGE = 6
        DELETED_CHANGE = 7

    property_changed = models.IntegerField(choices=ChangedProperty.choices)
    old_value = models.CharField(max_length=300, null=True)
    new_value = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.get_property_changed_display()
