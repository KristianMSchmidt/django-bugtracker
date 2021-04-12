from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from tickets.models import Ticket
from django.views.decorators.http import require_GET
from django.views.generic.base import View

class DemoLoginView(TemplateView):
    template_name = 'demo_login.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class UserListView(ListView):
    model = get_user_model()
    context_object_name = 'user_list'
    template_name = 'user_list.html'

@require_GET
def user_detail_view(request, username):
    some_user = get_object_or_404(get_user_model(), username=username)
    context = {
        'some_user': some_user,
        'project_list': some_user.projects.all(),
        'ticket_list': Ticket.objects.filter(Q(submitter=some_user) | Q(developer=some_user))
    }
    return render(request, 'user_details.html', context)


#This does exacly the same as the above function based view -- and passes tests
"""
class UserDetailView(View):
    def get(self, request, username):
        some_user = get_object_or_404(get_user_model(), username=username)
        context = {
            'some_user': some_user,
            'project_list': some_user.projects.all(),
            'ticket_list': Ticket.objects.filter(Q(submitter=some_user) | Q(developer=some_user))
        }
        return render(request, 'user_details.html', context)
"""