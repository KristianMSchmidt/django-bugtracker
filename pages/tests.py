from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model 
from projects.models import Project
from tickets.models import Ticket

class DemoLoginTests(SimpleTestCase):

    def setUp(self):
        """will be run before every test"""
        url = reverse('demo_login')
        self.response = self.client.get(url)

    def test_demo_login_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_demo_login_template(self):
        self.assertTemplateUsed(self.response, 'demo_login.html')

    def test_demo_login_page_contains_correct_html(self):
        self.assertContains(self.response, 'Demo')

    def test_demo_login_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')


class UserListViewTests(TestCase):

    def setUp(self):
        """will be run before every test"""
        url = reverse('user_list')
        self.response = self.client.get(url)

    def test_user_list_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_user_list_view_template(self):
        self.assertTemplateUsed(self.response, 'user_list.html')

    def test_user_list_page_contains_correct_html(self):
        self.assertContains(self.response, 'Personel')

    def test_user_list_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')


class UserDetailView(TestCase):

    def setUp(self):
        """will be run before every test"""
        User = get_user_model()
        self.user = User.objects.create_user(
            username='kristian',
            role=User.Role.ADMIN,
            password='testpass123',
        )
        self.url = reverse('user_detail', kwargs={'username':'kristian'})
        self.response = self.client.get(self.url)

    def test_user_detail_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_user_detail_view_template(self):
        self.assertTemplateUsed(self.response, 'user_details.html')

    def test_user_detail_page_contains_correct_html(self):
        self.assertContains(self.response, 'kristian')
        self.assertContains(self.response, 'Admin')

    def test_user_detail_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_user_detail_view_returns_404_when_user_does_not_exist(self):
        wrong_url = reverse('user_detail', kwargs={'username': 'fantasyuser'})
        no_response = self.client.get(wrong_url)
        self.assertEqual(no_response.status_code, 404)

    def test_user_detail_view_returns_405_on_post_requests(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_user_detail_page_contains_ticket_when_user_is_submitter(self):
        ticket1 = Ticket(
            title='title1',
            description='d1',
            submitter=self.user,
        )
        # ticket is not saved, so currently user is not submitter of ticket
        self.assertNotContains(self.response, 'title1')
        
        # now we save and check that ticket1 is part of response:
        ticket1.save()
        self.response = self.client.get(self.url)
        self.assertContains(self.response, 'title1')

    def test_user_detail_page_contains_ticket_when_user_is_submitter(self):
        ticket2 = Ticket(
            title='title2',
            description='d1',
            developer=self.user,
        )
        # ticket is not saved, so currently user is not developerr of ticket
        self.assertNotContains(self.response, 'title2')

        # now we save and check that ticket1 is part of response:
        ticket2.save()
        self.response = self.client.get(self.url)
        self.assertContains(self.response, 'title2')

    def test_user_detail_page_does_not_contain_ticket_when_user_is_not_submitter_or_developer(self):
        ticket3 = Ticket(
            title='title3',
            description='d1'
        )

        # now we save and check that ticket1 is part of response:
        ticket3.save()
        self.response = self.client.get(self.url)
        self.assertNotContains(self.response, 'title3')


class DashboardViewTests(TestCase):

    def setUp(self):
        """will be run before every test"""
        User = get_user_model()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpass123',
            role=User.Role.ADMIN
        )
        self.client.login(username='admin', password='testpass123')
        self.url = reverse('dashboard')
        self.response = self.client.get(self.url)

    def test_dashboard_view_status_code_logged_in_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_dashboard_view_status_code_logged_out_user(self):
        self.client.logout()
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 302)

    def test_dashboard_list_view_template(self):
        self.assertTemplateUsed(self.response, 'dashboard.html')

    def test_dashboard_list_page_contains_correct_html(self):
        self.assertContains(self.response, '<title>Dashboard')

    def test_dashboard_list_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

