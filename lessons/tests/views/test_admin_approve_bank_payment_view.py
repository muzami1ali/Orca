from django.test import TestCase
from django.urls import reverse
from lessons.models import LessonRequest,Invoice,BankTransfer
from lessons.models import Student, Lesson, LessonRequest
class AdminPanelViewTestCase(TestCase):
       fixtures = [
       'lessons/tests/fixtures/admin_user_staff.json',
       'lessons/tests/fixtures/default_lesson.json',
       'lessons/tests/fixtures/other_bank_transfer.json',

    ]
       def setUp(self):
           self.student = Student.objects.get(username='Charles.Babbage@example.org')
           self.lesson = Lesson.objects.get(lesson_name='PIANO_PRACTICE')
           self.lesson_request = LessonRequest.objects.create(
               student = self.student,
               lesson = self.lesson,
               is_authorised=True
           )
           self.invoice = Invoice.objects.create(
               student = self.student,
               lesson = self.lesson,
               invoice = f'{self.student.id}-{self.lesson_request}',
               is_fulfilled = False
           )
           self.bank_transfer = BankTransfer.objects.get(invoice = "001-02")
           self.url = reverse('approve_payment', kwargs={'BankTransferID': self.bank_transfer.id})

       def test_approve_bank_payment(self):
           self.client.login(username=self.student.username, password='Password123')
           self.assertTrue(BankTransfer.objects.get(id = self.bank_transfer.id).is_approved == False)
           response = self.client.post(self.url, data={'BankTransferID':self.bank_transfer.id})
           self.assertTrue(BankTransfer.objects.get(id = self.bank_transfer.id).is_approved == True)
          # self.assertEqual(self.bank_transfer.status , "paid")
