from django.test import TestCase
from django.urls import reverse
from .models import Project
from django.contrib.auth import get_user_model


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


class ProjectForeignKeyTests(TestCase):

    def setUp(self):
       
        User = get_user_model()
        self.user1 = User.objects.create_user(
            username='kris',
            email='kris@email.com',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            username='tom',
            email='tom@email.com',
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
        self.assertEqual(self.user1.projects.count(),1)

    def test_many_to_one(self):
        self.assertEqual(self.project1.created_by.username, 'kris')
        self.assertNotEqual(self.project1.created_by.username, 'tom')
