'''
    Test cases for the request lessons view
    @author Dean Whitbread
    @version 25/11/2022
'''

from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from lessons.models import Student, Lesson
from lessons.forms import StudentLessonRequest

class RequestLessonsViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('request_lessons')
        self.student = Student.objects.create_user(
            username = 'john.doe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            password = 'Password123'
        )
        self.form_data = {'TERM2':'Term 2'}
        self._create_valid_term_2_lesson()


    ''' Unit test cases '''
    def test_webpage_redirects_when_not_logged_in(self):
        if not self._authenticate_student():
            redirect_url = reverse('log_in')
            response = self.client.post(self.url, self.form_data, follow=True)
            self.assertRedirects(response, redirect_url,
                status_code=302, target_status_code=200, fetch_redirect_response=True
            )

    def test_lessons_show_when_valid_term_selected(self):
        self._authenticate_student()
        lessons_count = 0
        response = self.client.post(self.url, self.form_data, follow=True)
        term_2_lessons = response.context['term_lessons']

        lessons_count = len(term_2_lessons)

        self.assertEqual(lessons_count, 1)
        #lessons_count_after = Lesson.objects.count()
        #self.assertNotEqual(lessons_count_before, lessons_count_after)

    def test_lessons_not_show_when_invalid_term_selected(self):
        self._authenticate_student()
        #lessons_count_before = Lesson.objects.count()
        self.form_data = {'TERM7': 'Term 7'}
        response = self.client.post(self.url, self.form_data, follow=True)
        #lessons_count_after = Lesson.objects.count()
        #self.assertNotEqual(lessons_count_before, lessons_count_after)

    def test_visible_lessons_are_valid(self):
        self._authenticate_student()
        #lesson_count_before = Lesson.objects.count()
        response = self.client.get(self.url, self.form_data, follow=True)
        #lesson_count_after = Lesson.objects.count()
        if lesson_count_before != lesson_count_after:
            for lesson in Lesson.objects.all():
                try:
                    lesson.full_clean()
                except ValidationError:
                    pass
        else:
            self.fail('Number of lessons didn\'t change.')

    ''' Functions for test class '''
    def _authenticate_student(self):
        if not self.client.login(username=self.student.username, password='Password123'):
            self.fail('Account is unauthenticated.')

    def _create_valid_term_2_lesson(self):
        self.lesson = Lesson(
            lesson_name = "Piano Practice",
            duration = 30,
            date = "2022-11-26",
            price = 50,
            term_period = "TERM2"
        )
        self.lesson.save()
