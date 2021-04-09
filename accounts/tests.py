from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve  
from .forms import CustomUserCreationForm  
from .views import SignupPageView  

class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='kris',
            email='kris@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'kris')
        self.assertEqual(user.email, 'kris@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    

class SignupPageTests(TestCase):  

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__,
            SignupPageView.as_view().__name__
        )


class ChangeOrResetPasswordTests(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            username='kris',
            email='kris@email.com',
            password='testpass123'
        )
        self.client.login(username='kris', password='testpass123')

    def test_password_change_view_for_logged_in_user(self):
        url = reverse('password_change')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')
        self.assertContains(response, 'Password change')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

    def test_password_change_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('login') + '?next=/accounts/password_change/')
        response = self.client.get(
            reverse('login') + '?next=/accounts/password_change/')
        self.assertContains(response, 'Log In')

    def test_password_reset_view(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, 'registration/password_reset_form.html')
        self.assertContains(self.response, 'Forgot your password')
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')


class UpdateProfileTests(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            username='kris',
            email='kris@email.com',
            password='testpass123'
        )

    def test_profile_view_logged_in_user(self):
        self.client.login(username='kris', password='testpass123')
        url = reverse('profile')

         # get request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/profile.html')
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'kris@email.com')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

        # Post request
        response = self.client.post(
            url, {'email': 'new@mail.com', 'username': 'newname'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        
        # We can log in with new username
        self.client.logout()
        self.client.login(username='newname', password='testpass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # We can't log in with old username
        self.client.logout()
        self.client.login(username='kris', password='testpass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)




    def test_profile_view_logged_out_user(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=/accounts/profile/')

