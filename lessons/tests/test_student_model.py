"""Tests for Student model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student
import uuid

class StudentModelTest(TestCase):
    def setUp(self):
        self.user=Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            id=uuid.uuid4(),
            password='Password123'
            
        )
    def _create_second_user(self):
        self.user=Student.objects.create(
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.com',
            id=uuid.uuid4(),
            password ='Password123'
        )
        return self.user
    
    def _assert_student_user_is_valid(self):
        try:
            self.user.full_clean()
        except(ValidationError):
            self.fail("Test user should be valid")
            
    def _assert_student_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
    
    def test_valid_student_user(self):
        self._assert_student_user_is_valid()
    
    def test_student_first_name_cannot_be__blank(self):
        self.user.first_name=''
        self._assert_student_user_is_invalid
            
