from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project
from tickets.models import Ticket
from django.apps import apps
from django.utils import timezone
import math

class Notification(models.Model):
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)  #null bør strengt taget være false, men så skal mine tests omskrives
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='send_set', null=True) # samme kommentar som ovenfor
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    class Type(models.IntegerChoices):
        ROLE_UPDATE = 1  
        TICKET_ASSIGNMENT = 2  
        TICKET_UNASSIGNMENT = 3
        PROJECT_ENROLLMENT = 4
        PROJECT_DISENROLLMENT = 5
        NEW_TICKET_COMMENT = 6
    type = models.PositiveSmallIntegerField(
        choices=Type.choices, null=True, 
    )
    unseen = models.BooleanField(default=True)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        Ticket, null=True, blank=True, on_delete=models.CASCADE)
    new_role = models.PositiveSmallIntegerField(
        choices=get_user_model().Role.choices, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return str(self.type)
   
    def time_ago(self):
        now = timezone.now()

        diff = now - self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"
