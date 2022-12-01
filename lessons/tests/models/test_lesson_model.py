''' Unit tests for the request lessons model'''
''' @author Dean Whitbread'''
''' @version 22-11-2022'''

from django.test import TestCase
from lessons.models import Lesson
from django.core.exceptions import ValidationError

class LessonModelTestCase(TestCase):
    '''Unit tests for the request lessons model'''

    def setUp(self):
        self.lesson = Lesson(
            lesson_name = "PIANO_PRACTICE",
            student_availability = "2022-11-22",
            number_of_lessons = 5,
            interval = 2,
            duration = 45,
            term_period = "TERM2",
            additional_information = "Please give me tutor Jane Doe."
        )

    '''Test Cases'''
    def test_lesson_object_is_valid(self):
        self._lesson_is_valid()

    def test_lesson_name_must_not_be_blank(self):
        self.lesson.lesson_name = ""
        self._lesson_is_invalid()

    def test_lesson_name_contains_no_numbers(self):
        self.lesson.lesson_name = "Pian0 Pra5tic3"
        self._lesson_is_invalid()

    def test_lesson_name_contains_no_special_charatcers(self):
        self.lesson.lesson_name = "P!ano Prati&%e"
        self._lesson_is_invalid()

    def test_lesson_name_exceed_50_character_size_limit(self):
        self.lesson.lesson_name = 'a' * 51
        self._lesson_is_invalid()

    def test_student_availability_format_is_correct(self):
        self.lesson.student_availability = "2022-12-31"
        self._lesson_is_valid()

    def test_student_availability_format_is_incorrect(self):
        self.lesson.student_availability = "31-12-2022"
        self._lesson_is_invalid()

    def test_number_of_lessons_is_invalid(self):
        self.lesson.number_of_lessons = 11
        self._lesson_is_invalid()

    def test_number_of_lessons_is_non_negative(self):
        self.lesson.number_of_lessons = -1
        self._lesson_is_invalid()

    def test_number_of_lessons_contain_no_characters(self):
        self.lesson.number_of_lessons = "1One"
        self._lesson_is_invalid()

    def test_number_of_lessons_contain_no_special_characters(self):
        self.lesson.number_of_lessons = "2!$£@"
        self._lesson_is_invalid()

    def test_different_interval_period_is_valid(self):
        self.lesson.interval = 1
        self._lesson_is_valid()

    def test_interval_period_is_invalid(self):
        self.lesson.interval = 3
        self._lesson_is_invalid()

    def test_interval_period_is_non_negative(self):
        self.lesson.interval = -1
        self._lesson_is_invalid()

    def test_interval_period_contain_no_characters(self):
        self.lesson.interval = "1One"
        self._lesson_is_invalid()

    def test_interval_period_contain_no_special_characters(self):
        self.lesson.interval = "2!$£@"
        self._lesson_is_invalid()

    def test_duration_must_be_non_zero(self):
        self.lesson.duration = 0
        self._lesson_is_invalid()

    def test_duration_must_be_positive(self):
        self.lesson.duration = -10
        self._lesson_is_invalid()

    def test_different_duration_option_is_valid(self):
        self.lesson.duration = 30
        self._lesson_is_valid()

    def test_term_period_is_valid(self):
        self.lesson.term_period = "TERM4"
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

    def test_additional_information_can_be_blank(self):
        self.lesson.additional_information = ""
        self._lesson_is_valid()

    def test_additional_information_cannot_exceed_maximum(self):
        self.lesson.additional_information = "a" * 201
        self._lesson_is_invalid()

    def test_additional_information_can_accept_numbers(self):
        self.lesson.additional_information = "asdfhf23"
        self._lesson_is_valid()

    def test_additional_information_can_accept_special_characters(self):
        self.lesson.additional_information = "asdfhf!@$£"
        self._lesson_is_valid()

    '''Functions for valid/invalid object'''
    def _lesson_is_valid(self):
        try:
            self.lesson.full_clean()
        except ValidationError:
            self.fail('Lesson object is invalid.')

    def _lesson_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()
