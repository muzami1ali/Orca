'''
    Test cases for the edit lesson view.
    @author Dean Whitbread
    @version 08/12/2022
'''
from django.test import TestCase
from django.urls import reverse
from lessons.models import Invoice, Student, Lesson, LessonRequest
from lessons.tests.helpers import reverse_with_next

class InvoiceViewTestClass(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_lesson.json',
    ]

    def setUp(self):
        self.student = Student.objects.get(username='John.Doe@example.org')
        self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        self.lesson_request = LessonRequest.objects.create(
            student = self.student,
            lesson = self.lesson,
            is_authorised=True
        )
        self.invoice = Invoice.objects.create(
            student = self.student,
            lesson = self.lesson,
            invoice = f'{self.student.id}-{self.lesson_request}',
            is_fulfilled = False
        )
        self.url = reverse('invoice')


    ''' Unit tests for Invoice view  '''
    def test_url(self):
        self.assertEqual(self.url, '/booking/invoice/')

    def test_unauthorised_login_redirect_user(self):
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse_with_next('login', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_no_invoice_shows_when_invoice_is_fulfilled(self):
        self.client.login(username=self.student.username, password='Password123')
        self.invoice.is_fulfilled = True
        response = self.client.get(self.url)
        self.assertTrue(response.status_code==200)
        self.assertEqual(response.context['totalPrice'], 0)

    def test_unfulfilled_invoice_show(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTrue(response.status_code==200)
        self.assertEqual(response.context['totalPrice'], 50)
