"""Tests for Student model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student, Invoice, Lesson
import uuid

class InvoiceModelTest(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            lesson_id = 49,
            student_id = 2
        )
        

    def _create_second_invoice(self):
        invoice=Invoice.objects.create(
            lesson_id = 48,
            student_id = 2
        )
        return invoice

    def _assert_invoice_user_is_valid(self):
        try:
            self.invoice.full_clean()
        except(ValidationError):
            self.fail("Test invoice should be valid")

    def _assert_invoice_invoice_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invoice.full_clean()

    