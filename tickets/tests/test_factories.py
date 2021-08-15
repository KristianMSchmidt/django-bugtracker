# $ docker-compose exec web python manage.py test tickets.tests.test_factories

from ..models import Ticket
from .factories import TicketFactory
from django.test import TestCase

from django.contrib.auth import get_user_model


class TestProductFactory(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by multiple test methods in class
        cls.ticket = TicketFactory()

    def test_instances_of_default_product_market(self):
        self.assertIsInstance(self.ticket, Ticket)
        self.assertIsInstance(self.ticket.submitter, get_user_model())
        self.assertIsInstance(self.ticket.developer, get_user_model())
        self.assertIsInstance(self.ticket.title, str)
