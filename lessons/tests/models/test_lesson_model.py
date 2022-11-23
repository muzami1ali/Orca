'''Unit tests for the request lessons model'''
from django.test import TestCase
from lessons.models import Lesson
from django.core.exceptions import ValidationError

class LessonModelTestCase(TestCase):
    '''Unit tests for the request lessons model'''

    def setUp(self):
        self.lesson = Lesson(
            lesson_name = "Piano Practice",
            duration = 30,
            date = "2022-11-22",
            price = 50,
            term_period = "TERM1"
        )

    '''Test Cases'''
    def test_lesson_name_must_not_be_blank(self):
        self.lesson.lesson_name = ""
        self._lesson_is_invalid()

    def test_lesson_name_contains_no_numbers(self):
        self.lesson.lesson_name = "Pian0 Pra5tic3"
        self._lesson_is_invalid()

    def test_lesson_name_contains_no_special_charatcers(self):
        self.lesson.lesson_name = "P!ano Prati&%e"
        self._lesson_is_invalid()

    def test_lesson_name_can_have_max_characters(self):
        self.lesson.lesson_name = 'a' * 50
        self._lesson_is_valid()

    def test_lesson_name_exceed_50_character_size_limit(self):
        self.lesson.lesson_name = 'a' * 51
        self._lesson_is_invalid()

    def test_duration_must_be_non_zero(self):
        self.lesson.duration = 0
        self._lesson_is_invalid()

    def test_duration_must_be_positive(self):
        self.lesson.duration = -10
        self._lesson_is_invalid()

    def test_data_format_is_correct(self):
        self._lesson_is_valid()

    def test_date_format_is_incorrect(self):
        self.lesson.date = "31-12-2022"
        self._lesson_is_invalid()

    def test_price_is_non_zero(self):
        self.lesson.price = -1
        self._lesson_is_invalid()

    def test_price_is_non_negative(self):
        self.lesson.price = -1
        self._lesson_is_invalid()

    def test_price_is_positive(self):
        self._lesson_is_valid()

    def test_term_period_is_valid(self):
        self._lesson_is_valid()

    def test_term_period_is_invalid(self):
        self.lesson.term_period = "TERM7"
        self._lesson_is_invalid()

    def test_term_period_is_not_blank(self):
        self.lesson.term_period = ""
        self._lesson_is_invalid()

    def test_term_period_cannot_contain_special_characters(self):
        self.lesson.term_period = "T£RM!"
        self._lesson_is_invalid()

    '''Functions for valid/invalid object'''
    def _lesson_is_valid(self):
        try:
            self.lesson.full_clean()
        except ValidationError:
            self.fail('Lesson object is invalid.')

    def _lesson_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()
