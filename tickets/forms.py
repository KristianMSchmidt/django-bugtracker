from django.forms import ModelForm
from .models import Ticket, TicketComment


class TicketCreateForm(ModelForm):

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'project', 'type',
                  'status', 'priority', 'developer',)


class CommentCreateForm(ModelForm):
    class Meta:
        model = TicketComment
        fields = ['message']
