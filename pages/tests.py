from django.test import SimpleTestCase
from django.urls import reverse

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
