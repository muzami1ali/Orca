# '''
#     Test cases for the deal request view
# '''
# from django.test import TestCase
# from django.urls import reverse
# from django.db import IntegrityError
# from django.core.exceptions import PermissionDenied
# from lessons.models import Student, Lesson, LessonRequest
# from lessons.tests.helpers import reverse_with_next
# from django.http import HttpResponseForbidden, HttpResponseBadRequest
#
# class DealRequestTestCase(TestCase):
#
#     fixtures = [
#         'lessons/tests/fixtures/default_student.json',
#         'lessons/tests/fixtures/default_lesson.json',
#         'lessons/tests/fixtures/other_student.json',
#         'lessons/tests/fixtures/other_lesson.json',
#     ]
#
#     def setUp(self):
#         self.student = Student.objects.get(username='John.Doe@example.org')
#         self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
#         self.lesson_request = LessonRequest.objects.create(
#             student_id = self.student.id,
#             lesson_id = self.lesson.id,
#             is_authorised = False,
#         )
#
#         self.url = ('authorise/' + str(self.lesson_request.id))
#
#
#     def test_lesson_request_is_valid(self):
#
#         self.assertIsNotNone(self.lesson_request)
#
#
#     def test_lesson_request_count(self):
#         self.assertEqual(LessonRequest.objects.all().count(), 1)
#
#     def test_lesson_request_authorise(self):
#         self.assertEqual(LessonRequest.objects.filter(is_authorised = False).all().count(), 1)
#
#     def test_lesson_request_decline(self):
#         self.assertEqual(LessonRequest.objects.filter(is_authorised = True).count(), 0)
#
# 
