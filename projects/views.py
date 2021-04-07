from .models import Project
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from tickets.models import Ticket
from django.shortcuts import get_object_or_404

# Create your views here.

class ProjectListView(ListView):
    """
    Jeg får brug for tricks her fra, når/hvis kun visse projekter skal vises i 'My Projects'
    https: // docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/
    """
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'



class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projects/project_new.html'
    fields = ('title', 'description', 'users')


class ProjectUpdateView(UpdateView):
    model = Project
    context_object_name = 'project'
    fields = ('title', 'description', 'users',)
    template_name = 'projects/project_edit.html'


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('project_list')


class AddTicketToProjectView(CreateView):
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


