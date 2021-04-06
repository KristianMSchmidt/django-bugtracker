from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
) 
from django.urls import reverse_lazy
from .models import Ticket


# Create your views here.

class TicketListView(ListView):
    model = Ticket
    context_object_name = 'ticket_list'
    template_name = 'tickets/ticket_list.html'


class TicketCreateView(CreateView):
    model = Ticket
    template_name = 'tickets/ticket_new.html'
    fields = '__all__'


class TicketDetailView(DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'tickets/ticket_detail.html'

class TicketUpdateView(UpdateView):
    model = Ticket
    context_object_name = 'ticket'
    fields = ('title', 'description', 'project', 'type', 'status', 'submitter', 'developer',)
    template_name = 'tickets/ticket_edit.html'

class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_delete.html'
    success_url = reverse_lazy('ticket_list')
