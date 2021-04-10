
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from projects.models import Project

class Ticket(models.Model):

    # Priority choices
    LOW, MEDIUM, HIGH, URGENT = 1, 2, 3, 4
    PRIORITY_CHOICES = [(LOW, 'Low'), (MEDIUM, 'Medium'),
                        (HIGH, 'High'), (URGENT, 'Urgent')]

    # Status choices
    OPEN, IN_PROGRESS, CLOSED, INFO_REQUIRED = 1, 2, 3, 4
    STATUS_CHOICES = [(OPEN, 'Open'), (IN_PROGRESS, 'In progress'),
                      (CLOSED, 'Closed'), (INFO_REQUIRED, 'More info required')]

    # Type choices
    FEATURE_REQ, BUG, OTHER = 1, 2, 3
    TYPE_CHOICES = [(FEATURE_REQ, 'Feature request'), (BUG, 'Bug/Error'),
                    (OTHER, 'Other')]

    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=301)

    # one to many
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
        related_name='developer_set'
    )

    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        null=True
    )

    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES,
        null=True
    )

    type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ticket_detail", args=[str(self.id)])

    # status methods
    def is_open(self):
        return self.status == self.OPEN

    def is_in_progress(self):
        return self.status == self.IN_PROGRESS

    def is_closed(self):
        return self.status == self.CLOSED

    def info_required(self):
        return self.status == self.INFO_REQUIRED

    # priority methods

    def priority_is_low(self):
        return self.priority == self.LOW

    def priority_is_medium(self):
        return self.priority == self.MEDIUM

    def priority_is_high(self):
        return self.priority == self.HIGH

    def priority_is_urgent(self):
        return self.priority == self.URGENT

    # type methods

    def type_is_bug(self):
        return self.type == self.BUG

    def type_is_feature_request(self):
        return self.type == self.FEATURE_REQ

    def type_is_other(self):
        return self.type == self.OTHER



    #def is_open_or_closed(self):
    #    return self.status in {self.OPEN, self.CLOSED}

    # Using a separate database to store choices is only recommended when rows are changing dynamiccally.  I do it the recommeneded way by adding choices
