# '''
#     Test cases for the authorise lesson request view
# '''
# from django.test import TestCase
# from django.urls import reverse
# from django.db import IntegrityError
# from django.core.exceptions import PermissionDenied
# from lessons.models import Student, Lesson, LessonRequest
# from lessons.tests.helpers import reverse_with_next
# from django.http import HttpResponseForbidden, HttpResponseBadRequest
#
# class AuthoriseTestCase(TestCase):
#
#     fixtures = [
#         'lessons/tests/fixtures/default_student.json',
#         'lessons/tests/fixtures/default_lesson.json',
#         'lessons/tests/fixtures/default_administrator_user.json',
#     ]
#
#     def setUp(self):
#         self.student = Student.objects.get(username='John.Doe@example.org')
#         self.administrator = Student.objects.get(username="Petra.Pickles@example.org")
#         self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
#         self.lesson_request = LessonRequest.objects.create(
#             student_id = self.student.id,
#             lesson_id = self.lesson.id,
#             is_authorised = False,
#         )
#         self.url = reverse('authorise', kwargs={'nid': self.lesson_request.id})
#
#
#     def test_url_is_valid(self):
#         self.assertEqual(self.url, f'/deal_requests/authorise/1')
#
#
#     def test_redirect_if_not_logged_in(self):
#         redirect_url = reverse_with_next('login', self.url)
#         response = self.client.get(self.url, follow=True)
#         self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
#         self.assertTemplateUsed(response, 'log_in.html')
#
#     def test_authorise_listed_lesson(self):
#         self.client.login(username=self.administrator.username, password='Password123')
#         response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
#         self.assertNotEqual(LessonRequest.objects.count(), 0)
#
#     def test_cannot_authorise_the_same_lesson_twice(self):
#         self.client.login(username=self.administrator.username, password='Password123')
#         response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
#         response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
#         print(response.status_code)
#         self.assertTrue(response.status_code==403)
