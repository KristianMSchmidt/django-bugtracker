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


def chart_context():
    """ 
    Collects data to be shown in dashboard charts.
    In this version, all users - regardless of their role - will see all info on all tickets in the system.
    In a real-world scenario, most users should probably only see charts representing their own tickets (see partial implementation below).
    """

    busy_users = Ticket.objects.exclude(status=Ticket.Status.CLOSED).exclude(developer=None).values(
        'developer').annotate(cnt=Count('id')).order_by('-cnt')
    busy_user_count = min(busy_users.count(), 5)
    context = {
        'priority': {
            'low': Ticket.objects.filter(priority=Ticket.Priority.LOW).count(),
            'medium': Ticket.objects.filter(priority=Ticket.Priority.MEDIUM).count(),
            'high': Ticket.objects.filter(priority=Ticket.Priority.HIGH).count(),
            'urgent': Ticket.objects.filter(priority=Ticket.Priority.URGENT).count()

        },
        'status': {
            'open': Ticket.objects.filter(status=Ticket.Status.OPEN).count(),
            'info_required': Ticket.objects.filter(status=Ticket.Status.INFO_REQUIRED).count(),
            'in_progress': Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS).count(),
            'closed': Ticket.objects.filter(status=Ticket.Status.CLOSED).count(),
        },
        'type': {
            'feature_request': Ticket.objects.filter(type=Ticket.Type.FEATURE_REQUEST).count(),
            'bug': Ticket.objects.filter(type=Ticket.Type.BUG).count(),
            'other': Ticket.objects.filter(type=Ticket.Type.OTHER).count(),
        },
        'busy_users_labels': [get_user_model().objects.get(id=busy_users[index]['developer']).username for index in range(busy_user_count)],
        'busy_users_data': [busy_users[index]['cnt'] for index in range(busy_user_count)],
    }
    return context


# def chart_context():
    # num_tickets_in_progress = Ticket.objects.filter(
    #    status=Ticket.Status.IN_PROGRESS).count()

    # if self.request.user.is_admin():
    #     # alternative
    #     from django.db.models import Count
    #     priority_count = Ticket.objects.values('priority').annotate(cnt=Count('id'))
    #     'low': priority_count.get(priority=Ticket.Priority.LOW)['cnt'],

    #     busy_user_list = Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS).values(
    #         'developer').annotate(cnt=Count('id')).order_by('-cnt')
    #     busy_user_count = min(busy_user_list.count(), 5)
    #     context = {
    #         'priority': {
    #             'low': Ticket.objects.filter(priority=Ticket.Priority.LOW).count(),
    #             'medium': Ticket.objects.filter(priority=Ticket.Priority.MEDIUM).count(),
    #             'high': Ticket.objects.filter(priority=Ticket.Priority.HIGH).count(),
    #             'urgent': Ticket.objects.filter(priority=Ticket.Priority.URGENT).count()

    #         },
    #         'status': {
    #             'open': Ticket.objects.filter(status=Ticket.Status.OPEN).count(),
    #             'info_required': Ticket.objects.filter(status=Ticket.Status.INFO_REQUIRED).count(),
    #             'in_progress': Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS).count(),
    #             'closed': Ticket.objects.filter(status=Ticket.Status.CLOSED).count(),
    #         },
    #         'type': {
    #             'feature_request': Ticket.objects.filter(status=Ticket.Type.FEATURE_REQUEST).count(),
    #             'bug': Ticket.objects.filter(status=Ticket.Type.BUG).count(),
    #             'other': Ticket.objects.filter(status=Ticket.Type.OTHER).count(),
    #         },

    #         'busy_users_labels': [get_user_model().objects.get(id=busy_user_list[index]['developer']).username for index in range(busy_user_count)],
    #         'busy_users_data': [busy_user_list[index]['cnt'] for index in range(busy_user_count)],
    #     }

    # elif self.request.user.is_developer():
    #     context = {
    #         'priority': {
    #             'low': Ticket.objects.filter(priority=Ticket.Priority.LOW).filter(developer=self.request.user).count(),
    #             'medium': Ticket.objects.filter(priority=Ticket.Priority.MEDIUM).filter(developer=self.request.user).count(),
    #             'high': Ticket.objects.filter(priority=Ticket.Priority.HIGH).filter(developer=self.request.user).count(),
    #             'urgent': Ticket.objects.filter(priority=Ticket.Priority.URGENT).filter(developer=self.request.user).count()

    #         },
    #         'status': {
    #             'open': Ticket.objects.filter(status=Ticket.Status.OPEN).count(),
    #             'info_required': Ticket.objects.filter(status=Ticket.Status.INFO_REQUIRED).count(),
    #             'in_progress': Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS).count(),
    #             'closed': Ticket.objects.filter(status=Ticket.Status.CLOSED).count(),
    #         }
    #     }
    # else:
    #     # user is PM

    #     # Dette er vist nok rigtigt, men skal testes:  (se også https://docs.djangoproject.com/en/3.2/ref/models/querysets/ )

    #     # All project_id where PM is enrolled (Dette er jeg ret sikker på!)
    #     projects = Project.objects.filter(users=self.request.user)
    #     # Herefter: alle tickets hvor til de udvalgte projekter
    #     tickets = Ticket.objects.filter(project__in=projects)

    #     context = {
    #         'priority': {
    #             'low': tickets.filter(priority=Ticket.Priority.LOW).count(),
    #             'medium': tickets.filter(priority=Ticket.Priority.MEDIUM).count(),
    #             'high': tickets.filter(priority=Ticket.Priority.HIGH).count(),
    #             'urgent': tickets.filter(priority=Ticket.Priority.URGENT).count()
    #         },
    #         'status': {
    #             'open': tickets.filter(status=Ticket.Status.OPEN).count(),
    #             'info_required': tickets.filter(status=Ticket.Status.INFO_REQUIRED).count(),
    #             'in_progress': tickets.filter(status=Ticket.Status.IN_PROGRESS).count(),
    #             'closed': tickets.filter(status=Ticket.Status.CLOSED).count(),
    #         },
    #     }
