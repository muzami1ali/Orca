"""Tests for invoice model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student, Invoice, Lesson, LessonRequest
import uuid

class InvoiceModelTest(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_lesson.json',
    ]

    def setUp(self):

        self.student = Student.objects.get(username='John.Doe@example.org')
        self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        self.lesson_requested = LessonRequest.objects.create(
            student = self.student,
            lesson = self.lesson,
            is_authorised = False
        )
        self.invoice = Invoice.objects.create(
            lesson = self.lesson,
            student = self.student,
            invoice = "1-12",
            is_fulfilled = False

        )

    def _create_second_invoice(self):
        invoice=Invoice.objects.create(
            lesson_id = 48,
            student_id = 2,
            invoice = "2-12",
            is_fulfilled = False
        )
        return invoice

    '''Test Cases'''
    def test_invoice_not_null(self):
        self.assertIsNotNone(self.invoice)

    def test_invoice_id(self):
        self.assertEqual(self.invoice.lesson.lesson_name, self.lesson.lesson_name)

    def test_invoice_student_id(self):
        self.assertEqual(self.invoice.student.id, self.student.id)

    def test__invoice(self):
        self.assertEqual(self.invoice.id, 1)


    def test_none_of_invoice(self):
        self.invoice.clean_fields()
        self.assertIsNotNone(self.invoice)

    def test_invoice_not_null(self):
        self.assertIsNotNone(self.invoice)

    def test_invoice_lessons_name(self):
        self.assertEqual(self.invoice.lesson.lesson_name,'PIANO_PRACTICE')

    def test_username(self):
        self.assertEqual(self.invoice.student.username,'John.Doe@example.org')
