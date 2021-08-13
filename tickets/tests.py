from django.test import TestCase
from django.urls import reverse
from .models import Ticket, TicketComment
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
            role=User.Role.ADMIN
        )
        self.testuser_dev1 = User.objects.create_user(
            username='tom',
            password='testpass123',
            role=User.Role.DEVELOPER
        )
        self.testuser_dev2 = User.objects.create_user(
            username='hank',
            password='testpass123',
            role=User.Role.PROJECT_MANAGER
        )
        self.testuser_dev3 = User.objects.create_user(
            username='bob',
            password='testpass123',
            role=User.Role.PROJECT_MANAGER
        )

        self.ticket = Ticket.objects.create(
            title="Test Ticket 1",
            description="Test Ticket 1 Description",
            project=self.testproject,
            submitter=self.testuser_admin,
            developer=self.testuser_dev1,
            status=Ticket.Status.OPEN,
            type=Ticket.Type.BUG,
            priority=Ticket.Priority.HIGH
        )
        Ticket.objects.create(
            title="Test Ticket 2",
            description="Test Ticket 2 Description",
            project=self.testproject,
            submitter=self.testuser_dev2,
            status=Ticket.Status.OPEN,
            type=Ticket.Type.BUG,
            priority=Ticket.Priority.HIGH
        )
        self.ticket_comment = TicketComment.objects.create(
            commenter=self.testuser_admin,
            message="Just a comment",
            ticket=self.ticket
        )

    def test_ticket_listing(self):
        self.assertEqual(f'{self.ticket.title}', 'Test Ticket 1'),
        self.assertEqual(f'{self.ticket.description}',
                         'Test Ticket 1 Description'),
        self.assertEqual(f'{self.ticket.project}', 'Test Project'),
        self.assertEqual(f'{self.ticket.submitter}', 'kris'),
        self.assertEqual(f'{self.ticket.developer}', 'tom'),
        self.assertEqual(self.ticket.status, Ticket.Status.OPEN),
        self.assertEqual(self.ticket.type, Ticket.Type.BUG),
        self.assertEqual(self.ticket.priority, Ticket.Priority.HIGH),

        # status methods
        self.assertTrue(self.ticket.is_open())
        self.assertFalse(self.ticket.is_closed())
        self.assertFalse(self.ticket.is_in_progress())
        self.assertFalse(self.ticket.info_required())

        # priority methods
        self.assertTrue(self.ticket.priority_is_high())
        self.assertFalse(self.ticket.priority_is_urgent())
        self.assertFalse(self.ticket.priority_is_low())
        self.assertFalse(self.ticket.priority_is_medium())

        # type methods
        self.assertTrue(self.ticket.type_is_bug())
        self.assertFalse(self.ticket.type_is_feature_request())
        self.assertFalse(self.ticket.type_is_other())

        self.assertEqual(Ticket.objects.all().count(), 2)

    def test_ticket_list_view(self):
        # login required
        response = self.client.get(reverse('ticket_list') + '?order=status')
        self.assertEqual(response.status_code, 302)

        # login as admin -- context should contain ticket 1 and ticket 2
        self.client.login(username='kris', password='testpass123')
        response = self.client.get(reverse('ticket_list') + '?order=status')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('Test Ticket 1', response.content.decode())
        self.assertInHTML('Test Ticket 2', response.content.decode())
        self.assertNotContains(response, 'Fantasy Ticket Text')
        self.assertTemplateUsed(response, 'tickets/ticket_list.html')
        self.assertTemplateNotUsed(response, 'tickets/fantasy_list.html')
        self.client.logout()

        # log in as developer 1 --- context should contain ticket 1 as developer1 is assigned to ticket
        self.client.login(username='tom', password='testpass123')
        response = self.client.get(reverse('ticket_list') + '?order=status')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ticket 1')
        self.assertNotContains(response, 'Test Ticket 2')
        self.assertEqual(response.context['tickets'].count(), 1)

        self.client.logout()

        # log in as developer 2 --- context should only contain ticket 2
        self.client.login(username='hank', password='testpass123')
        response = self.client.get(reverse('ticket_list') + '?order=status')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Ticket 2')
        self.assertNotContains(response, 'Test Ticket 1')
        self.assertEqual(response.context['tickets'].count(), 1)

        self.client.logout()

        # log in as developer 3 --- context should not contain any tickets
        self.client.login(username='bob', password='testpass123')
        response = self.client.get(reverse('ticket_list') + '?order=status')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Ticket 2')
        self.assertNotContains(response, 'Test Ticket 1')
        self.assertAlmostEqual(response.context['tickets'].count(), 0)

    def test_ticket_detail_view_user_not_logged_in(self):
        response = self.client.get(self.ticket.get_absolute_url())
        self.assertEqual(response.status_code, 302)

    def test_ticket_detail_view_user_logged_in(self):
        # get request
        self.client.login(username='kris', password='testpass123')
        response = self.client.get(self.ticket.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get('/ticket/12345/')
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Ticket Details')
        self.assertTemplateUsed(response, 'tickets/ticket_detail.html')
        self.assertTemplateNotUsed(response, 'tickets/ticket_list.html')

        # previously, we have added one comment to the ticket:
        self.assertEqual(self.ticket.ticketcomment_set.count(), 1)

        # Post request - valid input should redirect
        response = self.client.post(self.ticket.get_absolute_url(), {
                                    'message': 'Test comment content'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.ticket.get_absolute_url())

        # There should now be two comment in the comment_set to the ticket
        self.assertEqual(self.ticket.ticketcomment_set.count(), 2)
        self.assertEqual(
            self.ticket.ticketcomment_set.last().message, 'Test comment content')

    def test_ticket_update_view(self):
        # login required
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
        # login required
        response = self.client.get(reverse('ticket_create'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='kris', password='testpass123')
        response = self.client.get(reverse('ticket_create'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('New ticket', response.content.decode())
        self.assertTemplateUsed(response, 'tickets/ticket_new.html')

    def test_ticket_delete_view(self):
        # login required
        response = self.client.get(
            reverse('ticket_delete', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='kris', password='testpass123')
        response = self.client.get(
            reverse('ticket_delete', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete')
        self.assertTemplateUsed(response, 'tickets/ticket_delete.html')

    def test_ticket_comment_delete_view(self):
        # login required
        response = self.client.get(
            reverse('ticket_comment_delete', kwargs={'pk': self.ticket_comment.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='kris', password='testpass123')
        response = self.client.get(
            reverse('ticket_comment_delete', kwargs={'pk': self.ticket_comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/comment_delete.html')
        self.assertContains(response, 'Confirm')

        # self.ticket should currently have 1 comments
        self.assertEqual(self.ticket.ticketcomment_set.count(), 1)

        response = self.client.post(
            reverse('ticket_comment_delete', kwargs={'pk': self.ticket_comment.id}))
        self.assertEqual(response.status_code, 302)
        # self.ticket should now have 0 comments
        self.assertEqual(self.ticket.ticketcomment_set.count(), 0)

    def test_ticket_comment_update_view(self):
        # login required
        response = self.client.get(
            reverse('ticket_comment_edit', kwargs={'pk': self.ticket_comment.id}))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='kris', password='testpass123')
        response = self.client.get(
            reverse('ticket_comment_edit', kwargs={'pk': self.ticket_comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/comment_edit.html')
        self.assertContains(response, 'Edit')

        response = self.client.post(
            reverse('ticket_comment_edit', kwargs={'pk': self.ticket_comment.id}), {'message': 'updated message'})
        self.assertEqual(response.status_code, 302)

    # Test view->update creates ticket events...
