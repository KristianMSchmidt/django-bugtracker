
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from projects.models import Project

class Ticket(models.Model):

    # Priority choices
    LOW, MEDIUM, HIGH, URGENT = 'L', 'M', 'H', 'U'
    PRIORITY_CHOICES = [(LOW, 'Low'), (MEDIUM, 'Medium'),
                        (HIGH, 'High'), (URGENT, 'Urgent')]

    # Status choices
    OPEN, IN_PROGRESS, CLOSED, INFO_REQUIRED = 'OP', 'IP', 'CL', 'IR'
    STATUS_CHOICES = [(OPEN, 'Open'), (IN_PROGRESS, 'In progress'),
                      (CLOSED, 'Closed'), (INFO_REQUIRED, 'More info required')]

    # Type choices
    FEATURE_REQ, BUG, OTHER = 'FR', 'BG', 'OT'
    TYPE_CHOICES = [(FEATURE_REQ, 'Feature request'), (BUG, 'Bug/Error'),
                    (OTHER, 'Other')]

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=301)

    # one to many
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        related_name='tickets',
        null=True
    )
    submitter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='submitter'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    developer = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='developer'
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=OPEN,
    )

    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default=LOW,
    )

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=OPEN,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ticket_detail", args=[str(self.id)])

    # status methods
    def is_open(self):
        return self.status == 'OP'  # self.OPEN also works... but might be slower?

    def is_in_progress(self):
        return self.status == 'IP'

    def is_closed(self):
        return self.status == 'CL'

    def info_required(self):
        return self.status == 'IR'

    # priority methods

    def priority_is_low(self):
        return self.priority == 'L'

    def priority_is_medium(self):
        return self.priority == 'M'

    def priority_is_high(self):
        return self.priority == 'H'

    def priority_is_urgent(self):
        return self.priority == 'U'

    # type methods

    def type_is_bug(self):
        return self.type == 'BG'

    def type_is_feature_request(self):
        return self.type == 'FR'

    def type_is_other(self):
        return self.type == 'OT'



    #def is_open_or_closed(self):
    #    return self.status in {self.OPEN, self.CLOSED}

    # Using a separate database to store choices is only recommended when rows are changing dynamiccally.  I do it the recommeneded way by adding choices
