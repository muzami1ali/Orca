"""Tests for lesson request model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student, Lesson, LessonRequest
from django.db import IntegrityError


class LessonRequestModelTest(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_lesson.json',
    ]

    def setUp(self):
        self.student = Student.objects.get(username='John.Doe@example.org')
        self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        self.authorised = False

    def test_lesson_request_model_is_vald(self):
        self._create_new_lesson_request()
        self._model_is_valid()

    def test_missing_student_is_invalid(self):
        self.student = None
        try:
            self._create_new_lesson_request()
            self._model_is_invalid()
        except IntegrityError:
            pass

    def test_missing_lesson_is_invalid(self):
        self.lesson = None
        try:
            self._create_new_lesson_request()
            self._model_is_invalid()
        except IntegrityError:
            pass

    def test_is_authorised_set_to_true_is_valid(self):
        self.authorised = True
        self._create_new_lesson_request()
        self._model_is_valid()

    ''' Functions for the test class '''

    def _model_is_valid(self):
        try:
            self.lesson_request.full_clean()
        except ValidationError:
            self.fail('Lesson object is invalid.')

    def _model_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson_request.full_clean()

    def _create_new_lesson_request(self):
        self.lesson_request = LessonRequest.objects.create(
            student=self.student,
            lesson=self.lesson,
            is_authorised=self.authorised
        )
