from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from ..forms import CustomUserCreationForm
from ..views import SignupPageView


class CustomUserTests(TestCase):

    def test_create_user(self):
        """ Custom User Model can be saved """
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
        """ Super user can be created """
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
