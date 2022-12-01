''' Unit Test Cases for students requesting lessons list'''
''' @author Dean Whitbread'''
''' @version 01-12-2022'''

from django.test import TestCase
from lessons.forms import LessonRequestForm
from django.core.exceptions import ValidationError
from django import forms

class StudentLessonRequestFormTestCase(TestCase):

    def setUp(self):
        self.form_data = {"lesson_name": "PIANO_PRACTICE",
            "student_availability": "FRI",
            "number_of_lessons": 5,
            "interval": 2,
            "duration": 45,
            "term_period": "TERM2",
            "additional_information": "Please give me tutor, Jason Doe."
            }

    ''' Unit Test Cases for students requesting lessons list'''

    def test_request_lesson_form_is_valid(self):
        self._form_is_valid()

    def test_request_lesson_form_is_invalid(self):
        self.form_data = self._incorrect_form_data()
        self._form_is_invalid()

    def test_all_fields_cannot_be_blank(self):
        self.form_data = self._empty_form_data()
        self._form_is_invalid()

    def test_additional_infomation_can_be_blank(self):
        self.form_data = self._blank_additional_information_form_data()
        self._form_is_valid()

    def test_lesson_name_is_a_choice_field(self):
        form = LessonRequestForm()
        lesson_name = form.fields['lesson_name']
        self.assertTrue(isinstance(lesson_name, forms.TypedChoiceField))

    def test_student_availability_is_a_choice_field(self):
        form = LessonRequestForm()
        student_availability = form.fields['student_availability']
        self.assertTrue(isinstance(student_availability, forms.TypedChoiceField))

    def test_duration_is_a_choice_field(self):
        form = LessonRequestForm()
        duration = form.fields['duration']
        self.assertTrue(isinstance(duration, forms.TypedChoiceField))

    def test_term_period_is_a_choice_field(self):
        form = LessonRequestForm()
        term_period = form.fields['term_period']
        self.assertTrue(isinstance(term_period, forms.TypedChoiceField))

    '''Functions to verify form's validness'''
    def _form_is_valid(self):
        self.form = LessonRequestForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())

    def _form_is_invalid(self):
        self.form = LessonRequestForm(data=self.form_data)
        self.assertFalse(self.form.is_valid())

    def _blank_additional_information_form_data(self):
        return {"lesson_name": "PIANO_PRACTICE",
            "student_availability": "FRI",
            "number_of_lessons": 5,
            "interval": 2,
            "duration": 45,
            "term_period": "TERM2",
            "additional_information": ""
            }

    def _incorrect_form_data(self):
        return {"lesson_name": "PIANO_PRACTICE",
            "student_availability": "FRI",
            "number_of_lessons": 5,
            "interval": 5,              # max interval is 2
            "duration": 45,
            "term_period": "TERM2",
            "additional_information": "Please give me tutor, Jason Doe."
            }

    def _empty_form_data(self):
        return {"lesson_name": "",
            "student_availability": "",
            "number_of_lessons": 0,
            "interval": 0,
            "duration": 0,
            "term_period": "",
            "additional_information": ""
            }
