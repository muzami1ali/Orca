"""Tests for lesson request model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student,Lesson, LessonRequest


class LessonRequestModelTest(TestCase):

    def test_main_case(self):
        lesson = Lesson(
            lesson_name = "Piano Practice",
            duration = 30,
            date = "2022-11-22",
            price = 50
        )
        lesson.save()
        student=Student.objects.create_user(
            username='@johndoe',
            first_name='John',
            last_name='Doe',
            password='Password123'
        )
        student.save()
        lesson_request=LessonRequest(student = student, lesson = lesson, is_authorised = False)
        lesson_request.save()

        record = LessonRequest.objects.get(id=1)
        self.assertEqual(record.student.username, "@johndoe")
        self.assertEqual(record.lesson.lesson_name, "Piano Practice")
