"""Unit tests for Bank Transfer form."""

from django import forms
from django.test import TestCase
from lessons.forms import BankTransferForm
from lessons.models import BankTransfer

class BankTransferFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            "invoice": "001-01", 
            "first_name":"John",
            "last_name": "Doe",
            "account_number": "12345678",
            "sort_code": "123456",
            "amount": "50"
        }
    
    def test_valid_bank_transfer_form(self):
        form = BankTransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    """Unit test for invoice field"""
    def test_bank_transfer_form_rejects_blank_invoice_field(self):
        self.form_input['invoice'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_alphabets_in_invoice_field(self):
        self.form_input['invoice'] = 'abcdefgh'
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_blank_first_name_field(self):
        self.form_input['first_name'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_blank_last_name_field(self):
        self.form_input['last_name'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_blank_account_number_field(self):
        self.form_input['account_number'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_alphabets_in_account_number_field(self):
        self.form_input['account_number'] = 'abcdefgh'
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_blank_sort_code_field(self):
        self.form_input['sort_code'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_alphabets_in_sort_code_field(self):
        self.form_input['sort_code'] = 'abcdef'
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_blank_amount_field(self):
        self.form_input['amount'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_rejects_negative_amount_field(self):
        self.form_input['amount'] = -60
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_bank_transfer_form_has_necessary_fields(self):
        form = BankTransferForm()
        self.assertIn('invoice', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('account_number', form.fields)
        self.assertIn('sort_code', form.fields)
        self.assertIn('amount', form.fields)

    def test_bank_transfer_form_must_save_correctly(self):
        form = BankTransferForm(data=self.form_input)
        before_count = BankTransfer.objects.count()
        form.save()
        after_count = BankTransfer.objects.count()
        self.assertEqual(after_count, before_count+1)
        bank_transfer = BankTransfer.objects.get(invoice='001-01')
        self.assertEqual(bank_transfer.first_name, 'John')
        self.assertEqual(bank_transfer.last_name, 'Doe')
        self.assertEqual(bank_transfer.account_number, '12345678')
        self.assertEqual(bank_transfer.sort_code, '123456')
        self.assertEqual(bank_transfer.amount, 50)

        