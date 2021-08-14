# $ docker-compose exec web python manage.py test projects.tests.test_views

from django.test import TestCase
from django.urls import reverse
from ..models import Project
from django.contrib.auth import get_user_model
from accounts.tests.factories import UserFactory


class ProjectCreateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by multiple test methods in class
        cls.user = UserFactory()

    def setUp(self):
        """ log in user before each test """
        self.client.login(username=self.user.username,
                          password='defaultpassword')

        # valid post data
        self.data = {
            'title': 'project title',
            'description': 'project description',
        }

    def test_project_create_view_requires_login(self):
        """ An attempt to access project create page without login will result in redirect to login page """
        self.client.logout()
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'],
                         '/accounts/login/?next=/projects/new/')

    def test_project_create_view_exists(self):
        """ Project create view return 200 on get requests and uses correct template """
        self.client.login(
            username=self.user.username, password='defaultpassword')
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('Save Project', response.content.decode())
        self.assertTemplateUsed(response, 'projects/project_new.html')

    def test_project_create_view(self):
        """ A new project is created when input is valid """
        self.client.login(
            username=self.user.username, password='defaultpassword')
        response = self.client.post(reverse('project_create'), self.data)
        self.assertEqual(Project.objects.all().count(), 1)
        #html = response.content.decode('utf8')
        ticket = Project.objects.first()
        self.assertEqual(ticket.created_by, self.user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'project_list'))

    def test_project_create_view(self):
        """ A new project is NOT created when input is invalid """
        self.client.login(
            username=self.user.username, password='defaultpassword')
        self.data['title'] = ""
        response = self.client.post(reverse('project_create'), self.data)
        self.assertEqual(Project.objects.all().count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_new.html')
        html = response.content.decode('utf8')
        self.assertIn('This field is required', html)
