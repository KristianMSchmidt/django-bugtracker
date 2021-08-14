from django.test import TestCase
from django.urls import reverse
from ..models import Ticket, TicketComment
from projects.models import Project
from django.contrib.auth import get_user_model
from projects.tests.factories import ProjectFactory
from accounts.tests.factories import UserFactory


class TicketModelTests(TestCase):
    pass


class TicketEventsTests(TestCase):
    pass


class TicketCommentModelTests(TestCase):
    pass
