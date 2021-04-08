from django.test import TestCase
from django.urls import reverse
from .models import Ticket
from projects.models import Project
from django.contrib.auth import get_user_model

class TicketTests(TestCase):

    def setUp(self):
        self.testproject = Project.objects.create(
            title='Test Project',
            description='Test Project description',
        )
        User = get_user_model()
        self.testuser_admin = User.objects.create_user(
            username='kris',
            password='testpass123',
            role = User.ADMIN
        )
        self.testuser_dev1 = User.objects.create_user(
            username='tom',
            password='testpass123',
            role=User.DEVELOPER
        )
        self.testuser_dev2 = User.objects.create_user(
            username='hank',
            password='testpass123',
            role=User.PROJECT_MANAGER
        )
        self.testuser_dev3 = User.objects.create_user(
            username='bob',
            password='testpass123',
            role=User.PROJECT_MANAGER
        )

        self.ticket  = Ticket.objects.create(
            title="Test Ticket 1",
            description = "Test Ticket 1 Description",
            project = self.testproject,
            submitter = self.testuser_admin,
            developer = self.testuser_dev1,
            status=Ticket.OPEN,
            type=Ticket.BUG,
            priority=Ticket.HIGH
        )
        Ticket.objects.create(
            title="Test Ticket 2",
            description="Test Ticket 2 Description",
            project=self.testproject,
            submitter=self.testuser_dev2,
            status=Ticket.OPEN,
            type=Ticket.BUG,
            priority=Ticket.HIGH
        )
 

    def test_ticket_listing(self):
        self.assertEqual(f'{self.ticket.title}', 'Test Ticket 1'),
        self.assertEqual(f'{self.ticket.description}', 'Test Ticket 1 Description'),
        self.assertEqual(f'{self.ticket.project}', 'Test Project'),
        self.assertEqual(f'{self.ticket.submitter}', 'kris'),
        self.assertEqual(f'{self.ticket.developer}', 'tom'),
        self.assertEqual(self.ticket.status, Ticket.OPEN),
        self.assertEqual(self.ticket.type, Ticket.BUG),
        self.assertEqual(self.ticket.priority, Ticket.HIGH),

        # status methods
        self.assertTrue(self.ticket.is_open())
        self.assertFalse(self.ticket.is_closed())
        self.assertFalse(self.ticket.is_in_progress())
        self.assertFalse(self.ticket.info_required())

        #priority methods
        self.assertTrue(self.ticket.priority_is_high())
        self.assertFalse(self.ticket.priority_is_urgent())
        self.assertFalse(self.ticket.priority_is_low())
        self.assertFalse(self.ticket.priority_is_medium())

        #type methods
        self.assertTrue(self.ticket.type_is_bug())
        self.assertFalse(self.ticket.type_is_feature_request())
        self.assertFalse(self.ticket.type_is_other())

    def test_ticket_list_view(self):
        # login required
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 302)

        # login as admin -- context should contain ticket 1 and ticket 2
        self.client.login(username='kris', password='testpass123')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ticket 1')
        self.assertContains(response, 'Test Ticket 2')
        self.assertNotContains(response, 'Fantasy Ticket Text')
        self.assertTemplateUsed(response, 'tickets/ticket_list.html')
        self.assertTemplateNotUsed(response, 'tickets/fantasy_list.html')
        self.client.logout()

        # log in as developer 1 --- context should contain ticket 1 as developer1 is assigned to ticket
        self.client.login(username='tom', password='testpass123')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ticket 1')
        self.assertNotContains(response, 'Test Ticket 2')
        self.assertAlmostEqual(response.context['ticket_list'].count(), 1)

        self.client.logout()

        # log in as developer 2 --- context should only contain ticket 2 
        self.client.login(username='hank', password='testpass123')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ticket 2')
        self.assertNotContains(response, 'Test Ticket 1')
        self.assertAlmostEqual(response.context['ticket_list'].count(), 1)

        self.client.logout()

        # log in as developer 3 --- context should not contain any tickets
        self.client.login(username='bob', password='testpass123')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Ticket 2')
        self.assertNotContains(response, 'Test Ticket 1')
        self.assertAlmostEqual(response.context['ticket_list'].count(), 0)        


    def test_ticket_detail_view(self):
        # login required
        response = self.client.get(self.ticket.get_absolute_url())
        self.assertEqual(response.status_code, 302)

        self.client.login(username='kris', password='testpass123')
        response = self.client.get(self.ticket.get_absolute_url())
        no_response = self.client.get('/ticket/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Ticket Details')
        self.assertTemplateUsed(response, 'tickets/ticket_detail.html')
        self.assertTemplateNotUsed(response, 'tickets/ticket_list.html')

    def test_ticket_update_view(self):
        #login required
        response = self.client.get(
            reverse('ticket_edit', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='kris', password='testpass123')
        response = self.client.get(
            reverse('ticket_edit', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Edit')
        self.assertTemplateUsed(response, 'tickets/ticket_edit.html')

    def test_ticket_create_view(self):
        #login required
        response = self.client.get(reverse('ticket_create'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='kris', password='testpass123')
        response = self.client.get(reverse('ticket_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Ticket')
        self.assertTemplateUsed(response, 'tickets/ticket_new.html')

    def test_ticket_delete_view(self):
        # login required 
        response = self.client.get(reverse('ticket_delete', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='kris', password='testpass123')
        response = self.client.get(
        reverse('ticket_delete', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete')
        self.assertTemplateUsed(response, 'tickets/ticket_delete.html')
    
    # man kunne også teste selve update funktionaliteten et ticket post-requests
    # Fx kan update funktionaliteten tjekkes sådan her: https://stackoverflow.com/questions/48814830/how-to-test-djangos-updateview
    # Men der er selvfølgelig ingen grund til at teste djangos indbyggede funktionalitet

