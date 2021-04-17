from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='send_set')

    class Type(models.IntegerChoices):
        ROLE_UPDATE = 1
        TICKET_ASSIGNMENT = 2
        TICKET_UNASSIGMENT = 3
        PROJECT_ENROLLEMENT = 4
        PROJECT_DISENROLLEMENT = 5
        NEW_TICKET_COMMENT = 6

    type = models.PositiveSmallIntegerField(
        choices=Type.choices, null=True, 
    )
    info_id = models.PositiveSmallIntegerField() #id to new ticket, project, role or comment in question 
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
   
    def __str__(self):
        #return f"Notification from {self.sender} to {self.receiver}"
        return f"Notification from Hans to Grete"
