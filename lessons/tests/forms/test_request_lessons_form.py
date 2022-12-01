''' Unit Test Cases for students requesting lessons list'''
''' @author Dean Whitbread'''
''' @version 22-11-2022'''

from django.test import TestCase
from lessons.forms import LessonRequestForm
from django.core.exceptions import ValidationError

class StudentLessonRequestFormTestCase(TestCase):
    ''' Unit Test Cases for students requesting lessons list'''

    def setUp(self):
        self.form_data = {'term_period': 'TERM2'}

    

    def test_term_selection_is_valid(self):
        self._form_is_valid()

    def test_term_selection_is_invalid(self):
        self.form_data = {'term_period': 'TERM7'}
        self._form_is_invalid()

    def test_term_selection_cannot_be_blank(self):
        self.form_data = {'term_period': ''}
        self._form_is_invalid()

    '''Functions to verify form's validness'''
    def _form_is_valid(self):
        self.form = LessonRequestForm(data=self.form_data)
        self.assertTrue(self.form.is_valid())

    def _form_is_invalid(self):
        self.form = LessonRequestForm(data=self.form_data)
        self.assertFalse(self.form.is_valid())
