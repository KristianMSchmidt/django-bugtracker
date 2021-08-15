from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from tickets.models import Ticket
from django.views.decorators.http import require_GET
from django.views.generic.base import View
from tickets.models import Ticket
from projects.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from notifications.models import Notification
from .utils import chart_context


class ChartView(View):
    def get(self, request):
        return render(request, 'pages/charts.html', context=chart_context())


def user_list_view(request):
    context = {'user_list': get_user_model().objects.all()}
    return render(request, 'pages/user_list.html', context)


class UserDetailView(View):

    def get(self, request, username):
        some_user = get_object_or_404(get_user_model(), username=username)
        context = {
            'some_user': some_user,
            'project_list': some_user.projects.all(),
            'ticket_list': Ticket.objects.filter(Q(submitter=some_user) | Q(developer=some_user))
        }
        return render(request, 'pages/user_details.html', context)


class DashboardView(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, 'pages/dashboard.html', context=chart_context())
