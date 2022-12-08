'''
Test cases for the contact us view.
@author Dean Whitbread
@version 07/12/2022
'''
from django.test import TestCase
from django.urls import reverse
from lessons.tests.helpers import reverse_with_next
from lessons.models import Student

class ContactUsFormTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
    ]

    def setUp(self):
        self.url = reverse('contact-us')
        self.student = Student.objects.get(username='John.Doe@example.org')

    def test_url_is_valid(self):
        self.assertEqual(self.url, f'/contact-us/')

    def test_contact_us_page_form_renders(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'contact.html')
