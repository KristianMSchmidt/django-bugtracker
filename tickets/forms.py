from django.forms import ModelForm
from .models import TicketComment

# Form to update users 'profile'
class CommentCreateForm(ModelForm):
    class Meta:
        model = TicketComment
        fields = ['message']
