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
            "student_availability": "FRI",
            "number_of_lessons": 5,
            "interval": 2,
            "duration": 45,
            "term_period": "TERM2",
            "additional_information": "Please give me tutor, Jason Doe."
            }

    ''' Unit test cases '''

    def test_webpage_redirects_when_student_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_can_book_valid_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_can_book_lesson_without_additional_information(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data = self._blank_additional_information_form_data()
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_cannot_book_invalid_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data = self._incorrect_form_data()
        response = self.client.post(self.url, data=self.form_data)
        self.assertTrue(response.status_code==400)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_cannot_book_same_lesson_twice(self):
        self.client.login(username=self.student.username, password='Password123')
        self.client.post(self.url, data=self.form_data)
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertTrue(response.status_code==400)

    def test_cannot_submit_empty_form(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data = self._empty_form_data()
        response = self.client.post(self.url, data=self.form_data)
        self.assertTrue(response.status_code==400)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_can_book_other_lesson_when_have_booked_lessons(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self._other_lesson_form_data())
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(Lesson.objects.count(), 1)

    ''' Functions for test class '''

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

    def _other_lesson_form_data(self):
        {"lesson_name": "MUSIC_THEORY",
            "student_availability": "MON",
            "number_of_lessons": 7,
            "interval": 1,
            "duration": 30,
            "term_period": "TERM4",
            "additional_information": ""
            }
