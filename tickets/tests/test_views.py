from django.test import TestCase
from django.urls import reverse
from ..models import Ticket, TicketComment
from projects.models import Project
from django.contrib.auth import get_user_model
from accounts.tests.factories import UserFactory
from projects.tests.factories import ProjectFactory


class TicketCreateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by multiple test methods in class
        cls.user = UserFactory()

    def setUp(self):
        """ log in user before each test """
        self.client.login(username=self.user.username,
                          password='defaultpassword')

        project = ProjectFactory()

        # valid post data
        self.data = {
            'title': 'ticket title',
            'description': 'ticket description',
            'project': 1,  # option 1 from scroll down menu
            'status': 1,
            'priority': 1,
            'type': 1
        }

    def test_ticket_create_view_requires_login(self):
        """ An attempt to access ticket create page without login will result in redirect to login page """
        self.client.logout()
        response = self.client.get(reverse('ticket_create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'],
                         '/accounts/login/?next=/tickets/new/')

    def test_ticket_create_view_exists(self):
        """ Ticket create view return 200 on get requests and uses correct template """
        self.client.login(
            username=self.user.username, password='defaultpassword')
        response = self.client.get(reverse('ticket_create'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('New ticket', response.content.decode())
        self.assertTemplateUsed(response, 'tickets/ticket_new.html')

    def test_ticket_create_view(self):
        """ A new ticket is created when input is valid """
        self.client.login(
            username=self.user.username, password='defaultpassword')
        response = self.client.post(reverse('ticket_create'), self.data)
        self.assertEqual(Ticket.objects.all().count(), 1)
        #html = response.content.decode('utf8')
        ticket = Ticket.objects.first()
        self.assertEqual(ticket.submitter, self.user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'ticket_list') + '?order=updated_at')

    def test_ticket_create_view(self):
        """ A new ticket is NOT created when input is invalid """
        self.client.login(
            username=self.user.username, password='defaultpassword')
        self.data['title'] = ""
        response = self.client.post(reverse('ticket_create'), self.data)
        self.assertEqual(Ticket.objects.all().count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/ticket_new.html')
        html = response.content.decode('utf8')
        self.assertIn('This field is required', html)
