''' Unit tests for the Bank Transfer model'''

from django.test import TestCase
from lessons.models import BankTransfer
from django.core.exceptions import ValidationError

class BankTransferModelTestCase(TestCase):

    fixtures= [
        'lessons/tests/fixtures/default_bank_transfer.json'
    ]

    def setUp(self):
        self.BankTransfer = BankTransfer.objects.get(invoice="001-01")
    
    def _create_second_bank_transfer(self):
        bank_transfer = BankTransfer.objects.create(
            invoice="001-02",
            first_name="John",
            last_name= "Doe",
            account_number= "12345678",
            sort_code="123456",
            amount= "50",
        )
        return bank_transfer

    def _assert_bank_transfer_is_valid(self):
        try:
            self.BankTransfer.full_clean()
        except ValidationError:
            self.fail('Bank Transfer object is invalid.')

    def _assert_bank_transfer_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.BankTransfer.full_clean()

    def test_valid_bank_transfer(self):
        self._assert_bank_transfer_is_valid()

    """Unit test for invoice field"""
    def test_invoice_field_must_not_be_blank(self):
        self.BankTransfer.invoice = ""
        self._assert_bank_transfer_is_invalid()

    def test_invoice_field_cannot_contain_alphabets(self):
        self.BankTransfer.invoice = "abcdefg"
        self._assert_bank_transfer_is_invalid()
    
    def test_invoice_field_may_contain_40_characters(self):
        self.BankTransfer.invoice= '1'*20 + '-' + '1'*19
        self._assert_bank_transfer_is_valid()

    def test_invoice_field_may_not_contain_more_than_40_characters(self):
        self.BankTransfer.invoice='1'*41
        self._assert_bank_transfer_is_invalid()

    # def test_invoice_field_uniqueness(self):
    #     second_bank_transfer=self._create_second_bank_transfer()
    #     self.BankTransfer.invoice=second_bank_transfer.invoice
    #     self._assert_bank_transfer_is_invalid()

    """Unit test for first name field"""
    def test_first_name_must_not_be_blank(self):
        self.BankTransfer.first_name = ""
        self._assert_bank_transfer_is_invalid()

    def test_first_name_field_may_contain_50_characters(self):
        self.BankTransfer.first_name='x'*50
        self._assert_bank_transfer_is_valid()

    def test_first_name_field_name_may_not_contain_more_than_50_characters(self):
        self.BankTransfer.first_name='x'*51
        self._assert_bank_transfer_is_invalid()
    
    """Unit test for last name field"""
    def test_last_name_must_not_be_blank(self):
        self.BankTransfer.last_name = ""
        self._assert_bank_transfer_is_invalid()

    def test_last_name_field_may_contain_50_characters(self):
        self.BankTransfer.last_name='x'*50
        self._assert_bank_transfer_is_valid()

    def test_last_name_field_may_not_contain_more_than_50_characters(self):
        self.BankTransfer.last_name='x'*51
        self._assert_bank_transfer_is_invalid()

    """Unit test for Account Number field"""
    def test_account_number_field_must_not_be_blank(self):
        self.BankTransfer.account_number = ""
        self._assert_bank_transfer_is_invalid()
    
    def test_account_number_field_may_contain_8_characters(self):
        self.BankTransfer.account_number='1'*8
        self._assert_bank_transfer_is_valid()

    def test_account_number_field_may_not_contain_more_than_8_characters(self):
        self.BankTransfer.account_number='1'*9
        self._assert_bank_transfer_is_invalid()

    def test_account_number_field_cannot_contain_less_than_8_characters(self):
        self.BankTransfer.account_number='1'*7
        self._assert_bank_transfer_is_invalid()

    def test_account_number_field_cannot_contain_alphabets(self):
        self.BankTransfer.account_number='abcdefgh'
        self._assert_bank_transfer_is_invalid()

    """Unit test for Sort Code field"""
    def test_sort_code_field_must_not_be_blank(self):
        self.BankTransfer.sort_code = ""
        self._assert_bank_transfer_is_invalid()

    def test_sort_code_field_may_contain_6_characters(self):
        self.BankTransfer.sort_code='1'*6
        self._assert_bank_transfer_is_valid()

    def test_sort_code_field_may_not_contain_more_than_6_characters(self):
        self.BankTransfer.sort_code='1'*7
        self._assert_bank_transfer_is_invalid()

    def test_sort_code_field_cannot_contain_less_than_6_characters(self):
        self.BankTransfer.sort_code='1'*5
        self._assert_bank_transfer_is_invalid()

    def test_sort_code_field_cannot_contain_alphabets(self):
        self.BankTransfer.sort_code='abcdef'
        self._assert_bank_transfer_is_invalid()

    """Unit test for amount field"""
    def test_amount_field_must_not_be_blank(self):
        self.BankTransfer.amount = ""
        self._assert_bank_transfer_is_invalid()

    def test_amount_field_cannot_be_negative(self):
        self.BankTransfer.amount = "-60"
        self._assert_bank_transfer_is_invalid()
    
    