# $ docker-compose exec web python manage.py test pages.tests.test_utils

from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project
from tickets.models import Ticket
from tickets.tests.factories import TicketFactory
from projects.tests.factories import ProjectFactory
from accounts.tests.factories import UserFactory
from ..utils import chart_context


class ChartContextTests(TestCase):

    def setUp(self):
        """ will be run before every test """
        pass

    def test_empty_context(self):
        ctx = chart_context()
        self.assertIsInstance(ctx, dict)
        expected = {
            'priority':
                {'low': 0, 'medium': 0, 'high': 0, 'urgent': 0},
            'status':
                {'open': 0, 'info_required': 0, 'in_progress': 0, 'closed': 0},
            'type':
                {'feature_request': 0, 'bug': 0, 'other': 0},
            'busy_users_labels': [],
            'busy_users_data': []
        }
        self.assertEqual(ctx, expected)

    def test_one_ticket(self):
        ticket = TicketFactory(
            priority=Ticket.Priority.HIGH,
            status=Ticket.Status.IN_PROGRESS,
            type=Ticket.Type.BUG,
            developer=UserFactory(username='Gretha')
        )
        ctx = chart_context()
        expected = {
            'priority':
                {'low': 0, 'medium': 0, 'high': 1, 'urgent': 0},
            'status':
                {'open': 0, 'info_required': 0, 'in_progress': 1, 'closed': 0},
            'type':
                {'feature_request': 0, 'bug': 1, 'other': 0},
            'busy_users_labels': ['Gretha'],
            'busy_users_data': [1]
        }
        self.assertIsInstance(ctx, dict)
        self.assertEqual(ctx, expected)

    def test_one_ticket_with_null_value_for_developer(self):
        ticket = TicketFactory(
            priority=Ticket.Priority.HIGH,
            status=Ticket.Status.IN_PROGRESS,
            type=Ticket.Type.BUG,
            developer=None
        )
        ctx = chart_context()
        expected = {
            'priority':
                {'low': 0, 'medium': 0, 'high': 1, 'urgent': 0},
            'status':
                {'open': 0, 'info_required': 0, 'in_progress': 1, 'closed': 0},
            'type':
                {'feature_request': 0, 'bug': 1, 'other': 0},
            'busy_users_labels': [],
            'busy_users_data': []
        }
        self.assertIsInstance(ctx, dict)
        self.assertEqual(ctx, expected)

    def test_three_tickets(self):
        Gretha = UserFactory(username='Gretha')
        TicketFactory(
            priority=Ticket.Priority.HIGH,
            status=Ticket.Status.IN_PROGRESS,
            type=Ticket.Type.BUG,
            developer=Gretha
        )

        TicketFactory(
            priority=Ticket.Priority.HIGH,
            status=Ticket.Status.OPEN,
            type=Ticket.Type.OTHER,
            developer=Gretha
        )
        TicketFactory(
            priority=Ticket.Priority.LOW,
            status=Ticket.Status.CLOSED,
            type=Ticket.Type.OTHER,
            developer=UserFactory(username='TOM')
        )

        ctx = chart_context()
        expected = {
            'priority':
                {'low': 1, 'medium': 0, 'high': 2, 'urgent': 0},
            'status':
                {'open': 1, 'info_required': 0, 'in_progress': 1, 'closed': 1},
            'type':
                {'feature_request': 0, 'bug': 1, 'other': 2},
            'busy_users_labels': ['Gretha'],
            'busy_users_data': [2]
        }
        self.assertIsInstance(ctx, dict)
        self.assertEqual(ctx, expected)

    def test_four_tickets(self):
        Gretha = UserFactory(username='Gretha')
        TicketFactory(
            priority=Ticket.Priority.HIGH,
            status=Ticket.Status.IN_PROGRESS,
            type=Ticket.Type.BUG,
            developer=Gretha
        )

        TicketFactory(
            priority=Ticket.Priority.HIGH,
            status=Ticket.Status.OPEN,
            type=Ticket.Type.OTHER,
            developer=Gretha
        )
        TicketFactory(
            priority=Ticket.Priority.LOW,
            status=Ticket.Status.CLOSED,
            type=Ticket.Type.OTHER,
            developer=UserFactory(username='TOM')
        )

        TicketFactory(
            priority=Ticket.Priority.URGENT,
            status=Ticket.Status.INFO_REQUIRED,
            type=Ticket.Type.FEATURE_REQUEST,
            developer=UserFactory(username='KIM')
        )

        ctx = chart_context()
        expected = {
            'priority':
                {'low': 1, 'medium': 0, 'high': 2, 'urgent': 1},
            'status':
                {'open': 1, 'info_required': 1, 'in_progress': 1, 'closed': 1},
            'type':
                {'feature_request': 1, 'bug': 1, 'other': 2},
            'busy_users_labels': ['Gretha', 'KIM'],
            'busy_users_data': [2, 1]
        }
        self.assertIsInstance(ctx, dict)
        self.assertEqual(ctx, expected)
