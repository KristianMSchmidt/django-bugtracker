from django.views.generic import ListView, DetailView
from .models import Ticket
#from django.shortcuts import render

# Create your views here.

class TicketListView(ListView):
    model = Ticket
    context_object_name = 'ticket_list'
    template_name = 'tickets/ticket_list.html'


class TicketDetailView(DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'tickets/ticket_detail.html'
