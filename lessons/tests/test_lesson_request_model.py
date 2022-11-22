"""Tests for lesson request model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student
import uuid


class LessonRequestModelTest(TestCase):
    def setUp(self):
        self.user=Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            id=uuid.uuid4(),
            password='Password123'

        )
    def _create_second_user(self):
        self.user=Student.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.com',
            id=uuid.uuid4(),
            password ='Password123'
        )
        return self.user

    def _assert_lesson_request_is_valid(self):
        try:
            self.user.full_clean()
        except(ValidationError):
            self.fail("Lesson request should be valid")

    def _assert_lesson_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_valid_student_user(self):
        self._assert_student_user_is_valid()

    """Number of lessons tests"""
    def test_number_of_lessons_cannot_be_blank(self):
        self.user.number_of_lessons=''
        self._assert_lesson_request_is_invalid

    def test_number_of_lessons_cannot_be_negative(self):
        self.user.number_of_lessons= -1
        self._assert_lesson_request_is_invalid()

    #cannot have more lessons than days of the week??
