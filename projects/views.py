from tickets.models import Ticket
from .models import Project
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.shortcuts import get_object_or_404, render

def manage_enrollments_view(request):
    return render(request, 'projects/manage_enrollments.html')

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        """
        Override. 
        Admins will see all projects. 
        Other users will only see the projects thery are enrolled in. 
        """
        if self.request.user.is_admin():
            return Project.objects.all()
        return Project.objects.filter(users=self.request.user)

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/project_new.html'
    fields = ('title', 'description', 'users')

    def form_valid(self, form):
        """Override. If the form is valid do these extra things before default behavior"""
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    context_object_name = 'project'
    fields = ('title', 'description', 'users',)
    template_name = 'projects/project_edit.html'


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('project_list')


class AddTicketToProjectView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'tickets/ticket_new.html'
    fields = ('title', 'description', 'type',
              'status', 'priority', 'developer',)


    def get_context_data(self, **kwargs):
        """
        Override. We need to add some context to the default context
        """
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['project_title'] = self.project.title 
        return context

    def form_valid(self, form):
        """
        Overridde. We need to set submitter and project values before saving to the db.
        This method is called when valid form data has been POSTed.
        """
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.submitter = self.request.user    
        form.instance.project = self.project

        return super().form_valid(form)

