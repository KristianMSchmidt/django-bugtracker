from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from .models import Ticket, TicketComment, TicketEvent
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CommentCreateForm
from django.urls import reverse

from django.contrib import messages


@login_required
def ticket_list_view(request):

    order = request.GET['order']
    if request.user.is_admin():
        tickets = Ticket.objects.all().order_by(order)
    tickets = Ticket.objects.filter(
        Q(developer=request.user) | Q(submitter=request.user)).order_by(order)
    return render(request, 'tickets/ticket_list.html', {"tickets": tickets})


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
            return Ticket.objects.all()[:10]
        return Ticket.objects.filter(Q(developer=self.request.user) | Q(submitter=self.request.user))


@login_required
def ticket_detail_view(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commenter = request.user
            comment.ticket = ticket
            comment.save()
            return redirect(ticket.get_absolute_url())

    else:
        form = CommentCreateForm()

    context = {
        'ticket': ticket,
        'comment_list': TicketComment.objects.filter(ticket=ticket),
        'event_list': TicketEvent.objects.filter(ticket=ticket).order_by('-created_at'),
        'form': form
    }
    return render(request, 'tickets/ticket_detail.html', context)


"""
class TicketDetailView(LoginRequiredMixin, DetailView):
    # Lav den først som en funktion-based view. Få den til at virke med al funktionaliteten.
    # Herefter eventuelt som clas-base-view, hvorden arver fra View
    # Herefter eventuelt som templateview -- men jeg er ikke sikker på, at dette er smart.

    model = Ticket
    context_object_name = 'ticket'
    template_name = 'tickets/ticket_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        ticket_id = kwargs['object'].id

        context['comment_list'] = TicketComment.objects.filter(
            ticket=kwargs['object'])

        return context
"""


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    context_object_name = 'ticket'
    fields = ('title', 'description', 'type',
              'status', 'priority', 'developer',)
    template_name = 'tickets/ticket_edit.html'

    def form_valid(self, form):
        # old_ticket = self.get_object()
        form.instance.updated_by = self.request.user
        new_ticket = form.save(commit=False)
        new_ticket.save(request=self.request)
        return super().form_valid(form)


@login_required
def ticket_delete_view(request, pk):

    if request.method == 'DELETE':
        ticket = Ticket.objects.filter(pk=pk)
        ticket_title = ticket.first().title
        ticket.delete()
        messages.success(
            request, f"You deleted the ticket {ticket_title}")

        # Same code as in ticket_list_view
        if request.user.is_admin():
            tickets = Ticket.objects.all().order_by('-updated_at')
        tickets = Ticket.objects.filter(
            Q(developer=request.user) | Q(submitter=request.user)).order_by('updated_at')

        # should this be redirected?
        return render(request, 'tickets/ticket_list.html', {"tickets": tickets})

    elif request.method == 'GET':
        ticket = Ticket.objects.get(pk=pk)
        return render(request, 'tickets/ticket_delete.html', {"ticket": ticket})
    # NB:
    # permission_required = 'tickets.delete_ticket'  #could also be multiple permissions
    # Custom permissions er nemme a lave.
    # persmission kan tildeles indiduelt eller gennem grupper. Er dett smart i mit tilfælde?
    # I could also implement permisions with "user passes test...fx based on role"


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'tickets/ticket_new.html'
    fields = ('title', 'description', 'project', 'type',
              'status', 'priority', 'developer',)

    def form_valid(self, form):
        """Override. If the form is valid do these extra things before default behavior"""
        form.instance.submitter = self.request.user
        form.instance.updated_by = self.request.user

        # self.object = form.save()
        # TicketEvent.objects.create(ticket=self.object, property_changed=TicketEvent.CREATED, user=self.request.user)
        return super().form_valid(form)


class TicketCommentUpdateView(LoginRequiredMixin, UpdateView):
    # TODO: user_passes_test .... skal være skaberen af the ticket
    model = TicketComment
    context_object_name = 'comment'
    fields = ('message',)
    template_name = 'tickets/comment_edit.html'


class TicketCommentDeleteView(LoginRequiredMixin, DeleteView):
    # TODO: user_passes_test .... skal være skaberen af the ticket
    model = TicketComment
    context_object_name = 'comment'
    template_name = 'tickets/comment_delete.html'

    def delete(self, request, *args, **kwargs):
        """
        Override to redirect to ticket details after deleting.
        """
        self.object = self.get_object()
        success_url = reverse_lazy('ticket_detail', kwargs={
            'pk': self.object.ticket.id})
        self.object.delete()
        return HttpResponseRedirect(success_url)


"""
def my_view(request):

    if request.method == 'POST':
        print request.POST.get('my_field')

        form = MyForm(request.POST)

        print form['my_field'].value()
        print form.data['my_field']

        if form.is_valid():

            print form.cleaned_data['my_field']
            print form.instance.my_field

            form.save()
            print form.instance.id  # now this one can access id/pk
"""
