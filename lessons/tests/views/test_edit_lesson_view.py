'''
    Test cases for the edit lesson view.
    @author Dean Whitbread
    @version 02/12/2022
'''
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student, Lesson, LessonRequest
from lessons.tests.helpers import reverse_with_next
from lessons.forms import LessonRequestForm
from django.db import IntegrityError

class EditLessonViewTestCase(TestCase):

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
        self.url = reverse('edit_lesson', kwargs={'LessonRequestID': self.lesson_request.id})
        self.form_data = Lesson.objects.filter(id=self.lesson_request.lesson_id).values().get()

    ''' Test cases for the edit lesson view. '''
    ''' POST Tests '''
    def test_url_is_valid(self):
        self.assertEqual(self.url, f'/booking/status/edit/{self.lesson_request.id}/')

    def test_redirect_if_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url, follow=True)
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_redirect_to_request_status_page_after_post(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.redirect_url = reverse('request_status')
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'request_status.html')

    def test_database_size_does_not_change_after_post_without_edits(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertTrue(LessonRequest.objects.count(), 1)
        self.assertTrue(Lesson.objects.count(), 1)
        self.assertTrue(response.status_code==200)

    def test_database_size_does_not_change_after_post_with_with_edits(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data['lesson_name'] = "MUSIC_THEORY"
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertTrue(response.status_code==200)
        self.assertTrue(LessonRequest.objects.count(), 1)
        self.assertTrue(Lesson.objects.count(), 1)

    def test_can_save_lesson_details_without_edits(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertTrue(response.status_code==200)

    def test_can_save_lesson_details_with_edits(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data['lesson_name'] = "MUSIC_THEORY"
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertTrue(response.status_code==200)

    def test_can_save_lesson_details_with_multiple_edits(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data['lesson_name'] = "MUSIC_THEORY"
        self.form_data['additional_information'] = ""
        self.form_data['number_of_lessons'] = 2
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertTrue(response.status_code==200)

    def test_updated_lesson_is_updated_in_database(self):
        self.client.login(username=self.student.username, password='Password123')
        self.form_data['lesson_name'] = "MUSIC_THEORY"
        response = self.client.post(self.url, data=self.form_data, follow=True)
        updated_lesson = LessonRequest.objects.get(id=self.lesson_request.id).lesson
        lesson_object = Lesson.objects.get(lesson_name="MUSIC_THEORY")
        self.assertEqual("MUSIC_THEORY", updated_lesson.lesson_name)
        self.assertEqual(lesson_object.id, updated_lesson.id)

    def test_cannot_edit_lesson_not_saved_in_database(self):
        self.client.login(username=self.student.username, password='Password123')
        self.url = reverse('edit_lesson', kwargs={'LessonRequestID': 100})
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertFalse(response.status_code == 200)

    def test_cannot_edit_other_students_lesson_request(self):
        self.client.login(username=self.student.username, password='Password123')
        self._create_other_lesson_request()
        self.other_url = reverse('edit_lesson', kwargs={'LessonRequestID': self.other_lesson_request.id})
        response = self.client.post(self.other_url, data=self.other_form_data, follow=True)
        self.assertFalse(response.status_code == 200)

    def test_cannot_edit_form_that_is_authorised(self):
        self.client.login(username=self.student.username, password='Password123')
        LessonRequest.objects.filter(id=self.lesson_request.id).update(is_authorised=True)
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertFalse(response.status_code==200)

    ''' GET Tests '''
    def test_edit_webpage_form_shows_initial_lesson_data_on_get(self):
        self.client.login(username=self.student.username, password='Password123')
        response = self.client.get(self.url, data=self.form_data, follow=True)
        self.assertTrue(response.status_code==200)
        self.assertNotEqual(response.context['form'].initial['lesson_name'], '')
        self.assertNotEqual(response.context['form'].initial['student_availability'], '')
        self.assertNotEqual(response.context['form'].initial['number_of_lessons'], '')
        self.assertNotEqual(response.context['form'].initial['interval'], '')
        self.assertNotEqual(response.context['form'].initial['duration'], '')
        self.assertNotEqual(response.context['form'].initial['term_period'], '')
        self.assertNotEqual(response.context['form'].initial['additional_information'], '')

    def test_cannot_show_other_students_lesson_request(self):
        self.client.login(username=self.student.username, password='Password123')
        self._create_other_lesson_request()
        self.other_url = reverse('edit_lesson', kwargs={'LessonRequestID': self.other_lesson_request.id})
        response = self.client.get(self.other_url, data=self.other_form_data, follow=True)
        self.assertFalse(response.status_code == 200)


    ''' Functions for test class '''
    def _create_other_lesson_request(self):
        self.other_student = Student.objects.get(username='Jane.Doe@example.org')
        self.other_lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        self.other_lesson_request = LessonRequest.objects.create(
            student_id = self.other_student.id,
            lesson_id = self.other_lesson.id,
            is_authorised = False,
        )
        self.other_form_data = Lesson.objects.filter(id=self.other_lesson_request.lesson_id).values().get()
