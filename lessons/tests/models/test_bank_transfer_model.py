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
    
    def _create_second_bank_transfer(self):
        bank_transfer = bankTransfer.objects.create(
            invoice="00102",
            first_name="John",
            last_name= "Doe",
            Account_Number= "12345678",
            Sort_Code="123456",
            Amount= "50",
        )
        return bank_transfer

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

    """Unit test for invoice field"""
    def test_invoice_field_must_not_be_blank(self):
        self.bankTransfer.invoice = ""
        self._assert_bank_transfer_is_invalid()

    def test_invoice_field_cannot_contain_alphabets(self):
        self.bankTransfer.invoice = "abcdefg"
        self._assert_bank_transfer_is_invalid()
    
    def test_invoice_field_may_contain_40_characters(self):
        self.bankTransfer.invoice='1'*40
        self._assert_bank_transfer_is_valid()

    def test_invoice_field_may_not_contain_more_than_40_characters(self):
        self.bankTransfer.invoice='1'*41
        self._assert_bank_transfer_is_invalid()

    def test_invoice_field_uniqueness(self):
        second_bank_transfer=self._create_second_bank_transfer()
        self.bankTransfer.invoice=second_bank_transfer.invoice
        self._assert_bank_transfer_is_invalid()

    """Unit test for first name field"""
    def test_first_name_must_not_be_blank(self):
        self.bankTransfer.first_name = ""
        self._assert_bank_transfer_is_invalid()

    def test_first_name_field_may_contain_50_characters(self):
        self.bankTransfer.first_name='x'*50
        self._assert_bank_transfer_is_valid()

    def test_first_name_field_name_may_not_contain_more_than_50_characters(self):
        self.bankTransfer.first_name='x'*51
        self._assert_bank_transfer_is_invalid()
    
    """Unit test for last name field"""
    def test_last_name_must_not_be_blank(self):
        self.bankTransfer.last_name = ""
        self._assert_bank_transfer_is_invalid()

    def test_last_name_field_may_contain_50_characters(self):
        self.bankTransfer.last_name='x'*50
        self._assert_bank_transfer_is_valid()

    def test_last_name_field_may_not_contain_more_than_50_characters(self):
        self.bankTransfer.last_name='x'*51
        self._assert_bank_transfer_is_invalid()

    """Unit test for Account Number field"""
    def test_Account_Number_field_must_not_be_blank(self):
        self.bankTransfer.Account_Number = ""
        self._assert_bank_transfer_is_invalid()
    
    def test_Account_Number_field_may_contain_8_characters(self):
        self.bankTransfer.Account_Number='1'*8
        self._assert_bank_transfer_is_valid()

    def test_Account_Number_field_may_not_contain_more_than_8_characters(self):
        self.bankTransfer.Account_Number='1'*9
        self._assert_bank_transfer_is_invalid()

    def test_Account_Number_field_cannot_contain_less_than_8_characters(self):
        self.bankTransfer.Account_Number='1'*7
        self._assert_bank_transfer_is_invalid()

    def test_Account_Number_field_cannot_contain_alphabets(self):
        self.bankTransfer.Account_Number='abcdefgh'
        self._assert_bank_transfer_is_invalid()

    """Unit test for Sort Code field"""
    def test_Sort_Code_field_must_not_be_blank(self):
        self.bankTransfer.Sort_Code = ""
        self._assert_bank_transfer_is_invalid()

    def test_Sort_Code_field_may_contain_6_characters(self):
        self.bankTransfer.Sort_Code='1'*6
        self._assert_bank_transfer_is_valid()

    def test_Sort_Code_field_may_not_contain_more_than_6_characters(self):
        self.bankTransfer.Sort_Code='1'*7
        self._assert_bank_transfer_is_invalid()

    def test_Sort_Code_field_cannot_contain_less_than_6_characters(self):
        self.bankTransfer.Sort_Code='1'*5
        self._assert_bank_transfer_is_invalid()

    def test_Sort_Code_field_cannot_contain_alphabets(self):
        self.bankTransfer.Sort_Code='abcdef'
        self._assert_bank_transfer_is_invalid()

    """Unit test for Amount field"""
    def test_Amount_field_must_not_be_blank(self):
        self.bankTransfer.Amount = ""
        self._assert_bank_transfer_is_invalid()
    
    