"""Tests of the bank transfer view."""
from django.test import TestCase
from django.urls import reverse
from lessons.forms import BankTransferForm
from lessons.tests.helpers import reverse_with_next
from lessons.models import BankTransfer, Student

class BankTransferViewTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
    ]

    def setUp(self):
        self.url = reverse('bank_transfer')
        self.student = Student.objects.get(username='John.Doe@example.org')
        self.form_input = {
            "invoice": "001-01",
            "first_name":"John",
            "last_name": "Doe",
            "account_number": "12345678",
            "sort_code": "123456",
            "amount": "50"
        }

    def test_sign_up_url(self):
        self.assertEqual(self.url,'/booking/bank_transfer/')

    def test_get_bank_transfer(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BankTransferForm))
        self.assertFalse(form.is_bound)

    def test_webpage_redirects_when_student_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_unsuccessful_bank_transfer(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_input['amount'] = -60
        before_count = BankTransfer.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = BankTransfer.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BankTransferForm))
        self.assertTrue(form.is_bound)
        self.assertEqual(after_count, before_count)

    def test_successful_bank_transfer(self):
        self.client.login(username=self.student.username, password='Password123')
        before_count = BankTransfer.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = BankTransfer.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('bank_transfer')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'bank_transfer.html')
        bank_transfer = BankTransfer.objects.get(invoice='001-01')
        self.assertEqual(bank_transfer.first_name, 'John')
        self.assertEqual(bank_transfer.last_name, 'Doe')
        self.assertEqual(bank_transfer.account_number, '12345678')
        self.assertEqual(bank_transfer.sort_code, '123456')
        self.assertEqual(bank_transfer.amount, 50)
