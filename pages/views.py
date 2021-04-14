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


"""
This does exacly the same as the above function based view -- and passes tests

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


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self):
        tickets_in_progress = Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS)
        num_tickets_in_progess = tickets_in_progress.count()
        #if self.request.user.is_admin():
        if True:
            #alternative
            #from django.db.models import Count
            #priority_count = Ticket.objects.values('priority').annotate(cnt=Count('id'))
            #'low': priority_count.get(priority=Ticket.Priority.LOW)['cnt'],
            
            busy_user_list = Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS).values('developer').annotate(cnt=Count('id')).order_by('-cnt')
            busy_user_count = min(busy_user_list.count(),5)
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
                    'feature_request': Ticket.objects.filter(status=Ticket.Type.FEATURE_REQUEST).count(),
                    'bug': Ticket.objects.filter(status=Ticket.Type.BUG).count(),
                    'other': Ticket.objects.filter(status=Ticket.Type.OTHER).count(),
                },

                'busy_users_labels': [get_user_model().objects.get(id=busy_user_list[index]['developer']).username for index in range(busy_user_count)],
                'busy_users_data': [busy_user_list[index]['cnt'] for index in range(busy_user_count)]
            }
        """
        elif self.request.user.is_developer():
            context = {
                'priority': {
                    'low': Ticket.objects.filter(priority=Ticket.Priority.LOW).filter(developer=self.request.user).count(),
                    'medium': Ticket.objects.filter(priority=Ticket.Priority.MEDIUM).filter(developer=self.request.user).count(),
                    'high': Ticket.objects.filter(priority=Ticket.Priority.HIGH).filter(developer=self.request.user).count(),
                    'urgent': Ticket.objects.filter(priority=Ticket.Priority.URGENT).filter(developer=self.request.user).count()

                },
                'status': {
                    'open': Ticket.objects.filter(status=Ticket.Status.OPEN).count(),
                    'info_required': Ticket.objects.filter(status=Ticket.Status.INFO_REQUIRED).count(),
                    'in_progress': Ticket.objects.filter(status=Ticket.Status.IN_PROGRESS).count(),
                    'closed': Ticket.objects.filter(status=Ticket.Status.CLOSED).count(),
                }
            }
        else:
            # user is PM

            #Dette er vist nok rigtigt, men skal testes:  (se også https://docs.djangoproject.com/en/3.2/ref/models/querysets/ )

            # All project_id where PM is enrolled (Dette er jeg ret sikker på!)
            projects = Project.objects.filter(users=self.request.user)
            # Herefter: alle tickets hvor til de udvalgte projekter
            tickets = Ticket.objects.filter(project__in=projects)

            context = {
                'priority': {
                    'low': tickets.filter(priority=Ticket.Priority.LOW).count(),
                    'medium': tickets.filter(priority=Ticket.Priority.MEDIUM).count(),
                    'high': tickets.filter(priority=Ticket.Priority.HIGH).count(),
                    'urgent': tickets.filter(priority=Ticket.Priority.URGENT).count()
                },
                'status': {
                    'open': tickets.filter(status=Ticket.Status.OPEN).count(),
                    'info_required': tickets.filter(status=Ticket.Status.INFO_REQUIRED).count(),
                    'in_progress': tickets.filter(status=Ticket.Status.IN_PROGRESS).count(),
                    'closed': tickets.filter(status=Ticket.Status.CLOSED).count(),
                },
            }
        """
        return context
