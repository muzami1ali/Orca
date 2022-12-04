'''
    Test cases for the cance lesson view.
    @author Dean Whitbread
    @version 02/12/2022
'''
from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from lessons.models import Student, Lesson, LessonRequest
from lessons.tests.helpers import reverse_with_next
from django.http import HttpResponseForbidden, HttpResponseBadRequest

class AuthoriseTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_lesson.json',
        'lessons/tests/fixtures/other_student.json',
        'lessons/tests/fixtures/other_lesson.json',
    ]

    def setUp(self):
        self.student = Student.objects.get(username='John.Doe@example.org')
        self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        self.lesson_request = LessonRequest.objects.create(
            student_id = self.student.id,
            lesson_id = self.lesson.id,
            is_authorised = False,
        )

        self.url = ('authorise/' + str(self.lesson_request.id))

    
    def test_url_is_valid(self):
        
        self.assertEqual(self.url, f'authorise/{self.lesson_request.id}')

    
    def test_redirect_if_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 404)
    
    def test_authorise_listed_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
        self.assertNotEqual(LessonRequest.objects.count(), 0)

    def test_cannot_authorise_the_same_lesson_twice(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
        response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id}, follow=True)
        
        self.assertTrue(response.status_code==404)

    