'''
    Test cases for the book lesson view - when a lesson gets booked.
    @author Dean Whitbread
    @version 26/11/2022
'''
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Lesson, LessonRequest
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
        self.url = reverse('request_lessons')

    ''' Test cases for the book lesson view - when a lesson gets booked. '''

    def test_url_is_valid(self):
        self.assertEqual(f'{self.url}{self.lesson.id}', f'/booking/request/1')

    def test_redirect_if_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_can_book_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data={'LessonID':self.lesson.id})
        self.assertEqual(Lesson.objects.count(), 2)

    def test_cannot_book_the_same_lesson_twice(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data={'LessonID':self.lesson.id})
        response = self.client.post(self.url, data={'LessonID':self.lesson.id}, follow=True)
        self.assertTrue(response.status_code==400)
        
    ''' Functions for test class '''
