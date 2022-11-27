'''
    Test cases for the edit lesson view.
    @author Dean Whitbread
    @version 27/11/2022
'''
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Lesson, LessonRequest
from lessons.tests.helpers import reverse_with_next

class EditLessonViewTestCase(TestCase):

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
        self.url = reverse('edit_lesson', kwargs={'LessonRequestID': self.lesson_request.id})

    ''' Test cases for the edit lesson view. '''
    def test_url_is_valid(self):
        self.assertEqual(self.url, f'/edit/{self.lesson_request.id}/')

    def test_redirect_if_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    ''' Functions for test class '''
