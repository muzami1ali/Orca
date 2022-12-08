from django.test import TestCase
from django.urls import reverse
from lessons.models import LessonRequest,Invoice,BankTransfer
from lessons.models import Student, Lesson, LessonRequest
class AdminPanelViewTestCase(TestCase):
       fixtures = [
       'lessons/tests/fixtures/admin_user_staff.json',
       'lessons/tests/fixtures/default_lesson.json',

    ]
       def setUp(self):
           self.student = Student.objects.get(username='Charles.Babbage@example.org')
           self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
           self.lesson_request = LessonRequest.objects.create(
               student = self.student,
               lesson = self.lesson,
               is_authorised=False
           )

           self.url = reverse('approve_lesson', kwargs={'LessonRequestID': self.lesson_request.id})

       def test_approve_lesson(self):
           self.client.login(username=self.student.username, password='Password123')
           self.assertTrue(LessonRequest.objects.get(id = self.lesson_request.id).is_authorised== False)
           response = self.client.post(self.url, data={'LessonRequestID':self.lesson_request.id})
           self.assertTrue(LessonRequest.objects.get(id = self.lesson_request.id).is_authorised== True)
