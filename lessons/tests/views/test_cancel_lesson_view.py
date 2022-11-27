'''
    Test cases for the cance lesson view.
    @author Dean Whitbread
    @version 27/11/2022
'''
from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from lessons.models import Student, Lesson, LessonRequest
from lessons.tests.helpers import reverse_with_next

class CancelLessonViewTestCase(TestCase):

    def setUp(self):
        self.student = Student.objects.create_user(
            username = 'john.doe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            password = 'Password123'
        )
        self.lesson = Lesson.objects.create(
            lesson_name = "Piano Practice",
            duration = 30,
            date = "2022-11-26",
            price = 50,
            term_period = "TERM2"
        )
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
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_can_cancel_listed_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        counter_before = LessonRequest.objects.count()
        response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
        counter_after = LessonRequest.objects.count()
        self.assertEqual(counter_before - 1, counter_after)

    def test_cannot_cancel_the_same_lesson_twice(self):
        self.client.login(username=self.student.username, password='Password123')
        with self.assertRaises(IntegrityError):
            response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
            response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id}, follow=True)
            redirect_url = reverse_with_next('request_status', self.url)
            self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_cannot_cancel_unlisted_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        with self.assertRaises(PermissionDenied):
            response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
            response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id}, follow=True)
            redirect_url = reverse_with_next('request_status', self.url)
            self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    ''' Functions for test class '''
    def _other_user(self):
        self.other_student = Student.objects.create_user(
            username = 'jane.doe@example.org',
            first_name = 'Jane',
            last_name = 'Doe',
            password = 'Password123'
        )

    def _other_lesson(self):
        self.other_lesson = Lesson.objects.create(
            lesson_name = "Trumpet Training",
            duration = 90,
            date = "2023-01-15",
            price = 50,
            term_period = "TERM5"
        )

    def _other_lesson_request(self):
        self.other_lesson_request = LessonRequest.objects.create(
            student_id = self.other_student.id,
            lesson_id = self.other_lesson.id,
            is_authorised = False,
        )
