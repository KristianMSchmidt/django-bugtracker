from django.views.generic import ListView, DetailView
from .models import Project
#from django.shortcuts import render

# Create your views here.

class ProjectListView(ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects/project_list.html'


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'
