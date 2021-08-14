# $ docker-compose exec web python manage.py test accounts.tests.test_factories

from .factories import UserFactory
from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUserFactory(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by multiple test methods in class
        cls.user = UserFactory()

    def test_sanity_check(self):
        """ User factory produces user objects """
        self.assertIsInstance(self.user, get_user_model())
        self.assertTrue('john' in self.user.username)

    def test_can_log_in(self):
        """ User factory produces users that can log in """
        is_logged_in = self.client.login(
            username=self.user.username, password='defaultpassword')
        self.assertTrue(is_logged_in)
