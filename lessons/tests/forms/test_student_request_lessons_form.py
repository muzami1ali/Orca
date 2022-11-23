''' Unit Test Cases for students requesting lessons list'''
''' @author Dean Whitbread'''
''' @version 22-11-2022'''

from django.test import TestCase
from lessons.forms import LessonRequest
from django.core.exceptions import ValidationError

class StudentLessonRequestFormTestCase(TestCase):
    ''' Unit Test Cases for students requesting lessons list'''

    def setUp(self):
        self.form_data = {'date': '2022-11-25'}

    def test_lesson_date_selected_is_valid(self):
        self._form_is_valid()

    def test_lesson_date_selected_is_invalid(self):
        self.form_data['date'] = '22-11-25'
        self._form_is_invalid()

    def test_lesson_date_field_is_not_blank(self):
        self.form_data['date'] = ''
        self._form_is_invalid()


    '''Functions to verify form's validness'''
    def _form_is_valid(self):
        self.form = LessonRequest(data=self.form_data)
        self.assertTrue(self.form.is_valid())

    def _form_is_invalid(self):
        self.form = LessonRequest(data=self.form_data)
        self.assertFalse(self.form.is_valid())
