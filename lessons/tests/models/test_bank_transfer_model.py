''' Unit tests for the Bank Transfer model'''

from django.test import TestCase
from lessons.models import bankTransfer
from django.core.exceptions import ValidationError

class BankTransferModelTestCase(TestCase):

    fixtures= [
        'lessons/tests/fixtures/default_bankTransfer.json'
    ]

    def setUp(self):
        self.bankTransfer = bankTransfer.objects.get(invoice="00101")

    def _assert_bank_transfer_is_valid(self):
        try:
            self.bankTransfer.full_clean()
        except ValidationError:
            self.fail('Bank Transfer object is invalid.')

    def _assert_bank_transfer_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.bankTransfer.full_clean()

    def test_valid_bank_transfer(self):
        self._assert_bank_transfer_is_valid()

    def test_invoice_field_must_not_be_blank(self):
        self.bankTransfer.invoice = ""
        self._assert_bank_transfer_is_invalid()

    def test_first_name_must_not_be_blank(self):
        self.bankTransfer.first_name = ""
        self._assert_bank_transfer_is_invalid()
    
    def test_last_name_must_not_be_blank(self):
        self.bankTransfer.last_name = ""
        self._assert_bank_transfer_is_invalid()

    def test_Account_Number_field_must_not_be_blank(self):
        self.bankTransfer.Account_Number = ""
        self._assert_bank_transfer_is_invalid()

    def test_Sort_Code_field_must_not_be_blank(self):
        self.bankTransfer.Sort_Code = ""
        self._assert_bank_transfer_is_invalid()

    def test_Amount_field_must_not_be_blank(self):
        self.bankTransfer.Amount = ""
        self._assert_bank_transfer_is_invalid()
    
    