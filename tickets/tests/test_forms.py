"""
To only run tests in this file:
$ docker-compose exec web python manage.py test tests.test_forms
"""
# Create your tests here.
from django.test import TestCase
from tickets.models import Ticket
from tickets.forms import TicketCreateForm
from django.core.exceptions import ValidationError
from accounts.tests.factories import UserFactory
from projects.tests.factories import ProjectFactory


class TicketCreateFormTest(TestCase):

    def setUp(self):
        self.data = {
            'title': 'ticket title',
            'description': 'ticket description',
            'project': ProjectFactory(),
            'submitter': UserFactory(username='bobby-submitter'),
            'developer': UserFactory(username='leonard-developer'),
            'status': 1,
            'priority': 1,
            'type': 1
        }

    def test_ticket_created(self):
        """ Submitting the ticket form form creates a ticket."""
        form = TicketCreateForm(data=self.data)

        is_valid = form.is_valid()
        form.save()

        self.assertTrue(is_valid)
        self.assertEqual(Ticket.objects.filter(
            title='ticket title').count(), 1)

    def test_no_title_is_invalid(self):
        """ Omitting required field will invalidate form and generate error """
        self.data['title'] = ''
        form = TicketCreateForm(data=self.data)

        is_valid = form.is_valid()

        self.assertFalse(is_valid)

        self.assertTrue('title' in form.errors)
        self.assertFalse('description' in form.errors)


class CommentCreateFormTest(TestCase):
    pass
