# $ docker-compose exec web python manage.py test projects.tests.test_models

from django.test import TestCase
from django.urls import reverse
from ..models import Project
from django.contrib.auth import get_user_model
from accounts.tests.factories import UserFactory


class ProjectForeignKeyTests(TestCase):

    def setUp(self):

        User = get_user_model()
        self.user1 = User.objects.create_user(
            username='kris',
            password='testpass123'
        )

        self.user2 = User.objects.create_user(
            username='tom',
            password='testpass123'
        )

        self.project1 = Project.objects.create(
            title='Test title',
            description='Test description',
            created_by=self.user1
        )

    def test_many_to_many(self):
        self.project1.users.add(self.user1)
        self.assertEqual(self.project1.users.count(), 1)
        self.project1.users.add(self.user2)
        self.assertEqual(self.project1.users.count(), 2)
        self.assertEqual(self.user1.projects.count(), 1)

    def test_many_to_one(self):
        self.assertEqual(self.project1.created_by.username, 'kris')
        self.assertNotEqual(self.project1.created_by.username, 'tom')
