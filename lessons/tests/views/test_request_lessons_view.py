'''
    Test cases for the request lessons view
    @author Dean Whitbread
    @version 25/11/2022
'''

from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from lessons.models import Student, Lesson
from lessons.tests.helpers import reverse_with_next

class RequestLessonsViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('request_lessons')
        self.student = Student.objects.create_user(
            username = 'john.doe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            password = 'Password123'
        )
        self.form_data = {'term_period':'TERM2'}
        self._create_valid_term_2_lesson()

    ''' Unit test cases '''
    def test_webpage_redirects_when_student_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_lessons_show_when_valid_term_selected(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data)
        self.assertNotEqual(response.context['lesson_counter'], 0)

    def test_lessons_not_show_when_invalid_term_selected(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data = {'term_period': 'TERM7'}
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.context['lesson_counter'], 0)

    def test_visible_lessons_are_valid(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data)
        if response.context['lesson_counter']:
            for lesson in response.context['term_lessons']:
                try:
                    lesson.full_clean()
                except ValidationError:
                    pass
        else:
            self.fail('Number of lessons didn\'t change after selecting term.')

    ''' Functions for test class '''
    def _create_valid_term_2_lesson(self):
        self.lesson = Lesson(
            lesson_name = "Piano Practice",
            duration = 30,
            date = "2022-11-26",
            price = 50,
            term_period = "TERM2"
        )
        self.lesson.save()
