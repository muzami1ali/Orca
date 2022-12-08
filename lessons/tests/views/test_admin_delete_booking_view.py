from django.test import TestCase
from django.urls import reverse
from lessons.models import LessonRequest,Invoice,BankTransfer
from lessons.models import Student, Lesson, LessonRequest
from lessons.tests.helpers import reverse_with_next
class AdminPanelViewTestCase(TestCase):
       fixtures = [
       'lessons/tests/fixtures/admin_user_staff.json',
       'lessons/tests/fixtures/default_lesson.json',
       'lessons/tests/fixtures/default_student.json',

    ]
       def setUp(self):
           self.student = Student.objects.get(username='John.Doe@example.org')
           self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
           self.lesson_request = LessonRequest.objects.create(
               student = self.student,
               lesson = self.lesson,
               is_authorised=True
           )
           self.admin = Student.objects.get(username='Charles.Babbage@example.org')

           self.url = reverse('delete_booking', kwargs={'LessonRequestID': self.lesson_request.id})

       def test_delete_booking(self):
           self.client.login(username=self.admin.username, password='Password123')
           self.assertEqual(LessonRequest.objects.count(), 1)
           response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
           self.assertEqual(LessonRequest.objects.count(), 0)
           self.assertEqual(Invoice.objects.count(),0)

       def test_delete_booking_authorised_is_false(self):
           self.client.login(username=self.admin.username, password='Password123')
           self.lesson_request.is_authorised = False
           self.assertEqual(LessonRequest.objects.count(), 1)
           response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
           self.assertEqual(LessonRequest.objects.count(), 0)
