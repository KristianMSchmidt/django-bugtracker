from django.test import TestCase
from django.urls import reverse
from .models import Project


class ProjectTests(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            title='Test title',
            description='Test description',
        )

    def test_project_listing(self):
        self.assertEqual(f'{self.project.title}', 'Test title')
        self.assertEqual(f'{self.project.title}', 'Test title')
        self.assertEqual(f'{self.project.description}', 'Test description')

    def test_project_list_view(self):
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test title')
        self.assertContains(response, 'Test title')
        self.assertNotContains(response, 'Fantasy Project'),
        self.assertTemplateUsed(response, 'projects/project_list.html'),
        self.assertTemplateNotUsed(response, 'projects/fantasy_list.html'),


    def test_project_detail_view(self):
        response = self.client.get(self.project.get_absolute_url())
        no_response = self.client.get('/project/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test title')
        self.assertTemplateUsed(response, 'projects/project_detail.html')
