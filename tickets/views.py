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

class TicketDetailView(DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'tickets/ticket_detail.html'

class TicketUpdateView(UpdateView):
    model = Ticket
    context_object_name = 'ticket'
    fields = ('title', 'description', 'project', 'type', 'status', 'priority', 'developer',)
    template_name = 'tickets/ticket_edit.html'

class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_delete.html'
    success_url = reverse_lazy('ticket_list')


class TicketCreateView(CreateView):
    model = Ticket
    template_name = 'tickets/ticket_new.html'
    fields = ('title', 'description', 'project', 'type',
              'status', 'priority', 'developer',)


    def form_valid(self, form):
        """
        Override. We need to set submitter to currently logged in user before creating ticket. 
        This method is called when valid form data has been POSTed.
        It should return an HttpResponse.
        """
        form.instance.submitter = self.request.user

        return super().form_valid(form)
