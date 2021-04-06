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
        self.testuser1 = User.objects.create_user(
            username='kris',
            email='kris@email.com',
            password='testpass123'
        )
        self.testuser2 = User.objects.create_user(
            username='tom',
            email='tom@email.com',
            password='tompass123'
        )
        self.ticket = Ticket.objects.create(
            title="Test Ticket",
            description = "Test Ticket Description",
            project = self.testproject,
            submitter = self.testuser1,
            developer=self.testuser2,
            status=Ticket.OPEN,
            type=Ticket.BUG,
            priority=Ticket.HIGH
        )

    def test_ticket_listing(self):
        self.assertEqual(f'{self.ticket.title}', 'Test Ticket'),
        self.assertEqual(f'{self.ticket.description}', 'Test Ticket Description'),
        self.assertEqual(f'{self.ticket.project}', 'Test Project'),
        self.assertEqual(f'{self.ticket.submitter}', 'kris'),
        self.assertEqual(f'{self.ticket.developer}', 'tom'),
        self.assertEqual(f'{self.ticket.status}', 'OP'),
        self.assertEqual(f'{self.ticket.type}', 'BG'),
        self.assertEqual(f'{self.ticket.priority}', 'H'),

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
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All Tickets')
        self.assertNotContains(response, 'Fantasy Ticket Text'),
        self.assertTemplateUsed(response, 'tickets/ticket_list.html'),
        self.assertTemplateNotUsed(response, 'tickets/fantasy_list.html'),

    def test_ticket_detail_view(self):
        response = self.client.get(self.ticket.get_absolute_url())
        no_response = self.client.get('/ticket/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Ticket Details')
        self.assertTemplateUsed(response, 'tickets/ticket_detail.html')
        self.assertTemplateNotUsed(response, 'tickets/ticket_list.html')

    def test_ticket_update_view(self):
        response = self.client.get(
            reverse('ticket_edit', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit')
        self.assertTemplateUsed(response, 'tickets/ticket_edit.html')
        # permissions etc  

    def test_ticket_create_view(self):
        response = self.client.get(reverse('ticket_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Ticket')
        self.assertTemplateUsed(response, 'tickets/ticket_new.html')
        # permissions etc

    def test_ticket_delete_view(self):
        response = self.client.get(
        reverse('ticket_delete', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete')
        self.assertTemplateUsed(response, 'tickets/ticket_delete.html')
        # permissions etc
    
    # man kunne også teste selve update funktionaliteten et ticket post-requests
    # Fx kan update funktionaliteten tjekkes sådan her: https://stackoverflow.com/questions/48814830/how-to-test-djangos-updateview
    # Men der er selvfølgelig ingen grund til at teste djangos indbyggede funktionalitet


   
