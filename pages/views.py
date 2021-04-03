#from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class DemoLoginView(TemplateView):
    template_name = 'demo_login.html'
