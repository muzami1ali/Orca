'''
    Test cases for the student request status view.
    @author Dean Whitbread
    @version 02/12/2022
'''
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Lesson, LessonRequest
from lessons.tests.helpers import reverse_with_next

class RequestStatusTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_lesson.json',
    ]

    def setUp(self):
        self.student = Student.objects.get(username='John.Doe@example.org')
        self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        self.lesson_requested = LessonRequest.objects.create(
            student = self.student,
            lesson = self.lesson,
            is_authorised = False
        )
        self.form_data = {"student": self.student.username}
        self.url = reverse('request_status')

    ''' Test cases for the student request status view. '''
    def test_url_is_valid(self):
        self.assertEqual(self.url, f'/booking/status/')

    def test_unauthenticated_user_redirected_to_login(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_requested_lessons_show_in_webpage(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(self.url, data=self.form_data)
        self.assertEqual(response.context['lesson_counter'], 1)

    def test_no_lessons_show_when_no_lessons_have_been_booked(self):
        self._create_other_user()
        self.client.login(username=self.other_user.username, password='Password123')
        response = self.client.get(self.url, data=self.form_data)
        self.assertEqual(response.context['lesson_counter'], 0)

    def test_additional_booked_lessons_show_in_webpage(self):
        self.client.login(username=self.student.username, password='Password123')
        self. _create_other_lesson_request()
        response = self.client.get(self.url, data=self.form_data)
        self.assertEqual(LessonRequest.objects.count(), 2)
        self.assertEqual(response.context['lesson_counter'], 2)


    ''' Functions for test class '''
    def _create_other_user(self):
        self.other_user = Student.objects.create_user(
            username = 'jane.doe@example.org',
            first_name = 'Jane',
            last_name = 'Doe',
            password = 'Password123'
        )

    def _create_other_lesson(self):
        self.other_lesson = Lesson.objects.create(
            lesson_name = "PERFORMANCE_PREP",
            student_availability = "SAT",
            number_of_lessons = 2,
            interval = 1,
            duration = 60,
            term_period = "TERM5",
            additional_information = ""
        )

    def _create_other_lesson_request(self):
        self._create_other_lesson()
        self.other_lesson_request = LessonRequest.objects.create(
            student = self.student,
            lesson = self.other_lesson,
            is_authorised = False
        )
