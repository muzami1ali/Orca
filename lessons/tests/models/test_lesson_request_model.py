"""Tests for lesson request model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student,Lesson, LessonRequest
import uuid


class LessonRequestModelTest(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_student.json',
        'lessons/tests/fixtures/default_lesson.json',
    ]

    def test_main_case(self):
        self.student = Student.objects.get(username='John.Doe@example.org')
        self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
        #lesson_request=LessonRequest(student = student, lesson = lesson, is_authorised = False)
        #lesson_request.save()

        #record = LessonRequest.objects.get(id=1)
        #self.assertEqual(record.student.username, "@johndoe")
