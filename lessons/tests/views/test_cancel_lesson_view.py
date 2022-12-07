'''
    Test cases for the cancel lesson view.
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

class CancelLessonViewTestCase(TestCase):

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
        self.url = reverse('cancel_lesson', kwargs={'LessonRequestID': self.lesson_request.id})

    ''' Test cases for the cancel lesson view. '''
    def test_url_is_valid(self):
        self.assertEqual(self.url, f'/booking/status/cancel/{self.lesson_request.id}/')

    def test_redirect_if_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_can_cancel_listed_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
        self.assertEqual(LessonRequest.objects.count(), 0)

    def test_cannot_cancel_the_same_lesson_twice(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
        response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id}, follow=True)
        self.assertTrue(response.status_code==400)

    def test_cannot_cancel_lesson_belonging_to_other_student(self):
        self.client.login(username=self.student.username, password='Password123')
        self._create_other_lesson_request()
        self.other_url = f'/booking/status/cancel/{self.other_lesson_request.id}/'
        response = self.client.post(self.other_url, follow=True)
        self.assertTrue(response.status_code==403)

    def test_cannot_cancel_form_that_is_authorised(self):
        self.client.login(username=self.student.username, password='Password123')
        LessonRequest.objects.filter(id=self.lesson_request.id).update(is_authorised=True)
        response = self.client.post(self.url, follow=True)
        self.assertFalse(response.status_code==200)

    def test_cannot_cancel_non_existent_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data={'LessonRequestID': 1000})
        self.assertEqual(LessonRequest.objects.count(), 1)
        self.assertTrue(response.status_code!=200)


    ''' Functions for test class '''
    def _create_other_lesson_request(self):
        self.other_student = Student.objects.get(username='Jane.Doe@example.org')
        self.other_lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        self.other_lesson_request = LessonRequest.objects.create(
            student_id = self.other_student.id,
            lesson_id = self.other_lesson.id,
            is_authorised = False,
        )
