"""Tests for the log out view"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student
from lessons.tests.helpers import LogInTester
# import uuid

class LogOutViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('log_out')
        self.user = Student.objects.create_user(
            username = "@johndoe",
            first_name='John',
            last_name='Doe',
            # email='johndoe@example.com',
            # id=uuid.uuid4(),
            password='Password123'

        )

    def test_log_out_url(self):
        self.assertEqual(self.url,'/log_out/')

    def test_get_log_out(self):
        self.client.login(username='@johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertFalse(self._is_logged_in())
