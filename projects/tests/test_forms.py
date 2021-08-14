"""
To only run tests in this file:
$ docker-compose exec web python manage.py test projects.tests.test_forms
"""
# Create your tests here.
from django.test import TestCase
from projects.models import Project
from projects.forms import ProjectCreateForm
from django.core.exceptions import ValidationError
from accounts.tests.factories import UserFactory
from projects.tests.factories import ProjectFactory


class ProjectCreateFormTest(TestCase):

    def setUp(self):
        self.data = {
            'title': 'project title',
            'description': 'project description',
        }

    def test_ticket_created(self):
        """ Submitting the projectcreate form form creates a project."""
        form = ProjectCreateForm(data=self.data)

        is_valid = form.is_valid()
        form.save()

        self.assertTrue(is_valid)
        self.assertEqual(Project.objects.filter(
            title='project title').count(), 1)

    def test_no_title_is_invalid(self):
        """ Omitting required field will invalidate form and generate error """

        self.data['title'] = ''
        form = ProjectCreateForm(data=self.data)

        is_valid = form.is_valid()

        self.assertFalse(is_valid)

        self.assertTrue('title' in form.errors)
        self.assertFalse('description' in form.errors)
