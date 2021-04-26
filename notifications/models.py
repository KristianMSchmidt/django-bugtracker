from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project
from tickets.models import Ticket
from django.apps import apps

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
 
    def __str__(self):
        return str(self.type)
        
