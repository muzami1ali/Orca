"""Tests of the log in view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from lessons.forms import LogInForm
from lessons.models import Student
from lessons.tests.helpers import LogInTester


class LogInViewTestCase(TestCase,LogInTester):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_administrator_user.json',
        'lessons/tests/fixtures/default_director_user.json',
    ]

    """Tests of the log in view."""
    def setUp(self):
        self.url = reverse('login')
        self.user = Student.objects.get(username='John.Doe@example.org')

    def test_log_in_url(self):
        self.assertEqual(self.url,'/login/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccesful_log_in(self):
        form_input = { 'username': self.user.username, 'password': 'WrongPassword123' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_username(self):
        form_input = { 'username': '', 'password': 'Password123' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_password(self):
        form_input = { 'username': self.user.username, 'password': '' }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_succesful_log_in(self):
        form_input = { 'username': self.user.username, 'password': 'Password123' }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('request_lessons')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'request_lessons.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    ''' Test staff and superusers redirected at login '''
    def test_that_administrator_redirected_to_admin_panel(self):
        self.administrator = Student.objects.get(username='Petra.Pickles@example.org')
        form_input = { 'username': self.administrator.username, 'password': 'Password123' }
        response = self.client.post(self.url, form_input, follow=True)
        response_url = reverse('admin_panel')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_panel.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)


    def test_that_director_redirected_to_admin_panel(self):
        self.director = Student.objects.get(username='Marty.Major@example.org')
        form_input = { 'username': self.director.username, 'password': 'Password123' }
        response = self.client.post(self.url, form_input, follow=True)
        response_url = reverse('admin_panel')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin_panel.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
