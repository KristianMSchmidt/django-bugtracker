from django.test import TestCase
from django.urls import reverse
from ..models import Project
from django.contrib.auth import get_user_model


class ProjectViewsTests(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            title='Test title',
            description='Test description',
        )
        User = get_user_model()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpass123',
            role=User.Role.ADMIN
        )
        self.dev_user = User.objects.create_user(
            username='developer',
            password='testpass123',
            role=User.Role.DEVELOPER
        )

    def test_project_listing(self):
        self.assertEqual(f'{self.project.title}', 'Test title')
        self.assertEqual(f'{self.project.title}', 'Test title')
        self.assertEqual(f'{self.project.description}', 'Test description')

    def test_project_list_view(self):
        # login requierd
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 302)

        # log in as admin -- respinse should contain all projects
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test title')
        self.assertNotContains(response, 'Fantasy Project'),
        # response.context['project_list']
        self.assertTemplateUsed(response, 'projects/project_list.html'),
        self.assertTemplateNotUsed(response, 'projects/fantasy_list.html'),
        self.client.logout()

        # login as developer - developer is not enrolled in projekct, so response should not contain project
        self.client.login(username='developer', password='testpass123')
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test title')

        # assign developer to project - response should now contain project
        self.project.users.add(self.dev_user)
        response = self.client.get(reverse('project_list'))
        self.assertContains(response, 'Test title'),

    def test_project_detail_view(self):
        # login required
        response = self.client.get(self.project.get_absolute_url())
        self.assertEqual(response.status_code, 302)

        self.client.login(username='developer', password='testpass123')
        response = self.client.get(self.project.get_absolute_url())
        no_response = self.client.get('/project/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test title')
        self.assertTemplateUsed(response, 'projects/project_detail.html')

    def test_project_update_view(self):
        # login required
        response = self.client.get(
            reverse('project_edit', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='developer', password='testpass123')

        response = self.client.get(
            reverse('project_edit', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit')
        self.assertTemplateUsed(response, 'projects/project_edit.html')

    def test_project_create_view(self):
        # login required
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='developer', password='testpass123')
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Project')
        self.assertTemplateUsed(response, 'projects/project_new.html')

    def test_project_delete_view(self):
        # login required
        response = self.client.get(
            reverse('project_delete', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='developer', password='testpass123')
        response = self.client.get(
            reverse('project_delete', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete')
        self.assertTemplateUsed(response, 'projects/project_delete.html')

    def test_add_ticket_to_project_view_get_request(self):
        # login required
        response = self.client.get(
            reverse('add_ticket_to_project', kwargs={'pk': self.project.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='developer', password='testpass123')
        response = self.client.get(
            reverse('add_ticket_to_project', kwargs={'pk': self.project.id}))
        no_response = self.client.get(
            reverse('add_ticket_to_project', kwargs={'pk': 12934747}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'tickets/ticket_new.html')
