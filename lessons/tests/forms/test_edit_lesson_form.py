'''
    Test cases for the edit lesson form.
    @author Dean Whitbread
    @version 27/11/2022
'''
from django.test import TestCase
from lessons.models import Student
from lessons.forms import EditBookedLessonForm
from django.core.exceptions import ValidationError

class EditBookedLessonFormTestCase(TestCase):

    def setUp(self):
        self.form_data = {'first_name':'','last_name':'', 'date':''}
        self.student = Student.objects.create_user(
            username = 'john.doe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            password = 'Password123'
        )
        self.initial_data = {'first_name':self.student.first_name,
            'last_name':self.student.last_name,
            'date':'2023-02-28'
            }

    ''' Test cases for the edit lesson form. '''
    def test_form_intially_loads_inital_values(self):
        self.form = EditBookedLessonForm(initial=self.initial_data)
        self.assertTrue(self.form.is_valid())

    def test_can_save_blank_form(self):
        self._form_is_valid()

    def test_can_change_first_name_only(self):
        self.form_data = {'first_name':'Jane'}
        self._form_is_valid()

    def test_can_change_last_name_only(self):
        self.form_data = {'last_name':'Doey'}
        self._form_is_valid()

    def test_can_change_lesson_date_only(self):
        self.form_data = {'date':'2023-02-28'}
        self._form_is_valid()

    def test_can_change_all_form_fields(self):
        self.form_data = {'first_name':'Jane', 'last_name':'Doey', 'date':'2023-02-28'}
        self._form_is_valid()

    def test_can_change_two_form_fields(self):
        self.form_data = {'first_name':'Jane', 'last_name':'Doey'}
        self._form_is_valid()
        self.form_data = {'first_name':'Jane', 'date':'2023-02-28'}
        self._form_is_valid()
        self.form_data = {'last_name':'Doey', 'date':'2023-02-28'}
        self._form_is_valid()

    def test_first_name_cannot_exceed_size_limit(self):
        self.form_data = {'first_name':'x'*51}
        self._form_is_invalid()

    def test_first_name_cannot_contain_numbers(self):
        self.form_data = {'first_name':'J4n3'}
        self._form_is_invalid()

    def test_first_name_cannot_contain_special_characters(self):
        self.form_data = {'first_name':'J&n£'}
        self._form_is_invalid()

    def test_first_name_cannot_exceed_size_limit(self):
        self.form_data = {'last_name':'x'*51}
        self._form_is_invalid()

    def test_first_name_cannot_contain_numbers(self):
        self.form_data = {'last_name':'J4n3'}
        self._form_is_invalid()

    def test_first_name_cannot_contain_special_characters(self):
        self.form_data = {'last_name':'J&n£'}
        self._form_is_invalid()

    def test_cannot_save_with_incorrect_date_format(self):
        self.form_data = {'date':'23-02-28'}
        self._form_is_invalid()

    ''' Functions for test class '''
    def _form_is_valid(self):
        form = EditBookedLessonForm(data=self.form_data, initial=self.initial_data)
        self.assertTrue(form.is_valid())

    def _form_is_invalid(self):
        form = EditBookedLessonForm(data=self.form_data, initial=self.initial_data)
        self.assertFalse(form.is_valid())
