'''
    Test cases for the student request status view.
    @author Dean Whitbread
    @version 26/11/2022
'''
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Lesson, LessonRequest
from lessons.tests.helpers import reverse_with_next

class RequestStatusTestCase(TestCase):

    def setUp(self):
        self.url = reverse('request_status')
        self.student = Student.objects.create_user(
            username = 'john.doe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            password = 'Password123'
        )
        self.lesson = Lesson(
            lesson_name = "Piano Practice",
            duration = 30,
            date = "2022-11-26",
            price = 50,
            term_period = "TERM2"
        )
        self.lesson.save()
        self.lesson_requested = LessonRequest(
            student = self.student,
            lesson = self.lesson,
            is_authorised = False
        )
        self.lesson_requested.save()
        self.form_data = { "username": self.student.username}

    ''' Test cases for the student request status view. '''
    def test_unauthenticated_user_redirected_to_login(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_requested_lessons_show_in_webpage(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data)
        self.assertNotEqual(response.context['lesson_counter'], 0)

    def test_no_lessons_show_when_no_lessons_have_been_booked(self):
        self.client.login(username=self._other_user.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.context['lesson_counter'], 0)

    def test_can_edit_lesson_details(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data)
        requested_lessons = response.context['requested_lessons']

        self.fail("Test not yet setup.")


    def test_can_delete_lesson(self):
        self.client.login(username=self.student.username, password='Password123')
        self.fail("Test not yet setup.")

    ''' Functions for test class '''
    def _other_user(self):
        self.other_user = Student.objects.create_user(
            username = 'jane.doe@example.org',
            first_name = 'Jane',
            last_name = 'Doe',
            password = 'Password123'
        )
        return self.other_user
