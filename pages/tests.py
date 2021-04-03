from django.test import SimpleTestCase
from django.urls import reverse, resolve  # new
from .views import DemoLoginView  # new


class DemoLoginViewTests(SimpleTestCase):

    def setUp(self):
        """will be run before every test"""
        url = reverse('demo_login')
        self.response = self.client.get(url)

    def test_demologinpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_demologinpage_template(self):
        self.assertTemplateUsed(self.response, 'demo_login.html')

    def test_demologinpage_contains_correct_html(self):
        self.assertContains(self.response, 'Demo Login')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_homepageview(self):  # new
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            DemoLoginView.as_view().__name__
        )
