from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse_lazy
from News.accounts.models import NewsUser


class LoginViewTest(TestCase):

    def test_login_view(self):
        response = self.client.get(reverse_lazy("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign up")


class RegisterViewTest(TestCase):

    def test_register_view(self):
        response = self.client.get(reverse_lazy("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")
        self.assertContains(response, "Log in")


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client.force_login(NewsUser.objects.get_or_create(email='testuser')[0])

    def test_logout_view(self):
        response = self.client.get(reverse_lazy("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Logout")
        self.assertContains(response, "Home")
