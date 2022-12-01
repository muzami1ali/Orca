'''
    Test cases for the request lessons view
    @author Dean Whitbread
    @version 01/11/2022
'''

from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from lessons.models import Student, Lesson
from lessons.tests.helpers import reverse_with_next
from django.db import IntegrityError

class RequestLessonsViewTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
    ]

    def setUp(self):
        self.url = reverse('request_lessons')
        self.student = Student.objects.get(username='John.Doe@example.org')
        self.form_data = {"lesson_name": "PIANO_PRACTICE",
            "student_availability": "2022-11-22",
            "number_of_lessons": 5,
            "interval": 2,
            "duration": 45,
            "term_period": "TERM2",
            "additional_information": "Please give me tutor, Jason Doe."
            }

    ''' Unit test cases '''
    def test_webpage_redirects_when_student_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_can_book_valid_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data)
        self.assertTrue(response)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_can_book_lesson_without_additional_information(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data = self._blank_additional_information_form_data()
        response = self.client.post(self.url, data=self.form_data)
        self.assertTrue(response)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_cannot_book_invalid_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data = self._incorrect_form_data()
        with self.assertRaises(ValueError):
            response = self.client.post(self.url, data=self.form_data)
            self.assertNotEqual(Lesson.objects.count(), 2)

    def test_cannot_book_same_lesson_twice(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data = self._incorrect_form_data()
        with self.assertRaises(ValueError):
            response = self.client.post(self.url, data=self.form_data)
            response = self.client.post(self.url, data=self.form_data)
            self.assertNotEqual(Lesson.objects.count(), 2)

    ''' Functions for test class '''
    def _blank_additional_information_form_data(self):
        return {"lesson_name": "PIANO_PRACTICE",
            "student_availability": "2022-11-22",
            "number_of_lessons": 5,
            "interval": 2,
            "duration": 45,
            "term_period": "TERM2",
            "additional_information": ""
            }

    def _incorrect_form_data(self):
        return {"lesson_name": "PIANO_PRACTICE",
            "student_availability": "22-11-2022",       # date is incorrect
            "number_of_lessons": 5,
            "interval": 2,
            "duration": 45,
            "term_period": "TERM2",
            "additional_information": "Please give me tutor, Jason Doe."
            }
