"""Tests for lesson request model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student,Lesson, LessonRequest
import uuid


class LessonRequestModelTest(TestCase):
    def setUp(self):
        self.student=Student.objects.create_user(
            username = 'john.doe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            password = 'Password123'
        )
        self.lesson = Lesson(
            lesson_name = "Piano Practice",
            duration = 30,
            date = "2022-11-22",
            price = 50
        )
        self.lesson_request=LessonRequest(student =self.student,lesson = self.lesson, is_authorised = False)



    def test_lesson_request_has_valid_student(self):
        self.assertEqual(self.lesson_request.student.username, "john.doe@example.org")
        self.assertEqual(self.lesson_request.student.first_name, "John")
        self.assertEqual(self.lesson_request.student.last_name, "Doe")

    def test_lesson_request_has_valid_lesson(self):
        self.assertEqual(self.lesson_request.lesson.lesson_name, "Piano Practice")
        self.assertEqual(self.lesson_request.lesson.duration, 30)
        self.assertEqual(self.lesson_request.lesson.date, "2022-11-22")
