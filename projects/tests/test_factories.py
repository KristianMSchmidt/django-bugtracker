# $ docker-compose exec web python manage.py test projects.tests.test_factories

from ..models import Project
from .factories import ProjectFactory
from django.test import TestCase

from django.contrib.auth import get_user_model


class TestProjectFactory(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by multiple test methods in class
        cls.project = ProjectFactory()

    def test_instances_of_default_product_market(self):
        self.assertIsInstance(self.project, Project)
        self.assertIsInstance(self.project.created_by, get_user_model())
        self.assertIsInstance(self.project.title, str)
        self.assertEqual(self.project.title, 'test project title0')
