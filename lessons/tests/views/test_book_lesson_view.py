'''
    Test cases for the book lesson view - when a lesson gets booked.
    @author Dean Whitbread
    @version 26/11/2022
'''
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Lesson, LessonRequest
this wasn't in main so i commented it out because it gave exceptions

from lessons.tests.helpers import reverse_with_next
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class BookLessonViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_lesson.json',
        'lessons/tests/fixtures/other_student.json',
        'lessons/tests/fixtures/other_lesson.json',
    ]
    def setUp(self):
        self.student = Student.objects.get(username='John.Doe@example.org')
        self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        self.url = reverse('request_lessons', kwargs={'LessonID': self.lesson.id})

    ''' Test cases for the book lesson view - when a lesson gets booked. '''

    def test_url_is_valid(self):
        self.assertEqual(self.url, f'/booking/request/{self.lesson.id}')

    def test_redirect_if_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_can_book_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        counter_before = LessonRequest.objects.count()
        response = self.client.post(self.url, data={'LessonID':self.lesson.id})
        counter_after = LessonRequest.objects.count()
        self.assertEqual(counter_before + 1, counter_after)

    def test_cannot_book_the_same_lesson_twice(self):
        self.client.login(username=self.student.username, password='Password123')
        with self.assertRaises(IntegrityError):
            response = self.client.post(self.url, data={'LessonID':self.lesson.id})
            response = self.client.post(self.url, data={'LessonID':self.lesson.id}, follow=True)
            redirect_url = reverse_with_next('request_lessons', self.url)
            self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    ''' Functions for test class '''
