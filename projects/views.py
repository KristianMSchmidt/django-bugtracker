from django.contrib import messages
from .forms import ProjectCreateForm
from tickets.models import Ticket
from .models import Project
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View
)
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse


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


class ProjectDetailCardBodyView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form = ProjectCreateForm(instance=project)
        return render(request, 'projects/project_detail_card_body.html', {"project": project, "form": form})


class ProjectCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.created_by = self.request.user
            new_project.save()

            messages.success(
                request, f"You successfully created a new project")
            return redirect(reverse('project_list'))
        else:
            # print(form.errors)
            return render(request, 'projects/project_new.html', {'form': form})

    def get(self, request):
        form = ProjectCreateForm()
        return render(request, 'projects/project_new.html', {'form': form})

    template_name = 'projects/project_new.html'
    fields = ('title', 'description', 'users')

    def form_valid(self, form):
        """Override. If the form is valid do these extra things before default behavior"""
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    context_object_name = 'project'
    # fields = ('title', 'description', 'users',)
    fields = ('title', 'description')
    template_name = 'projects/project_edit.html'

    def form_valid(self, form):
        """Override. If the form is valid do these extra things before default behavior"""
        messages.success(
            self.request, f"You successfully updated this project")
        self.success_url = reverse_lazy('project_detail_card_body', kwargs={
                                        'pk': self.get_object().pk})

        return super().form_valid(form)


# class ProjectUpdateView(LoginRequiredMixin, UpdateView):
#     model = Project
#     context_object_name = 'project'
#     fields = ('title', 'description', 'users',)
#     template_name = 'projects/project_edit.html'

#     def form_valid(self, form):
#         """Override. If the form is valid do these extra things before default behavior"""
#         messages.success(
#             self.request, f"You successfully updated this project")
#         return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('project_list')
