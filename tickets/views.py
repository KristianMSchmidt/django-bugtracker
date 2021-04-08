from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
) 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Ticket

from django.db.models import Q

# Create your views here.

class TicketListView(LoginRequiredMixin, ListView):

    model = Ticket
    context_object_name = 'ticket_list'
    template_name = 'tickets/ticket_list.html'

    def get_queryset(self):
        """
        Override. 
        Admins should see all projects. 
        Developer and Project Managers should see tickets where they are developers or submitters
        TODO: Project Managers should see all tickets to all the projects they are enrolled in (perhaps this is not necessary, as ticket are shown in individual projects...)
        """
        if self.request.user.is_admin():
            return Ticket.objects.all()
        return Ticket.objects.filter(Q(developer=self.request.user) | Q(submitter=self.request.user))

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'tickets/ticket_detail.html'

class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    context_object_name = 'ticket'
    fields = ('title', 'description', 'project', 'type', 'status', 'priority', 'developer',)
    template_name = 'tickets/ticket_edit.html'

class TicketDeleteView(
        LoginRequiredMixin, 
        #PermissionRequiredMixin,
        DeleteView):
    model = Ticket
    template_name = 'tickets/ticket_delete.html'
    success_url = reverse_lazy('ticket_list')
    
    # NB: 
    #permission_required = 'tickets.delete_ticket'  #could also be multiple permissions
    # Custom permissions er nemme a lave. 
    #persmission kan tildeles indiduelt eller gennem grupper. Er dett smart i mit tilfælde?
    # I could also implement permisions with "user passes test...fx based on role"
    

class TicketCreateView(LoginRequiredMixin, CreateView):
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
