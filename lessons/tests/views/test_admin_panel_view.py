from django.test import TestCase
from lessons.models import Student,LessonRequest,BankTransfer,Invoice
from django.urls import reverse
from lessons.tests.helpers import reverse_with_next
from lessons.models import LessonRequest,Invoice,BankTransfer
class AdminPanelViewTestCase(TestCase):
    fixtures = [
       'lessons/tests/fixtures/admin_user_staff.json',
       'lessons/tests/fixtures/admin_user_staff_other.json',
       'lessons/tests/fixtures/admin_user_superuser.json',
       'lessons/tests/fixtures/admin_user_superuser_other.json',
       'lessons/tests/fixtures/default_student.json',
       'lessons/tests/fixtures/default_lesson.json'
       
    ]
    def setUp(self):
        self.url=reverse('admin_panel')
        self.student=Student.objects.get(username='John.Doe@example.org')
        self.staff_user=Student.objects.get(username='Charles.Babbage@example.org')
        self.other_staff_user=Student.objects.get(username='Alan.Turing@example.org')
        self.superuser=Student.objects.get(username='Sherlock.Holmes@example.org')
        self.other_superuser=Student.objects.get(username='James.Moriarty@example.org')
    
    
    def test_only_valid_users_can_access_admin(self):
        self.assertTrue(self.staff_user.is_staff)
        self.assertTrue(self.other_staff_user.is_staff)
        self.assertTrue(self.superuser.is_superuser and self.superuser.is_staff)
        self.assertTrue(self.other_superuser.is_superuser and self.other_superuser.is_staff)
        self.assertFalse(self.student.is_superuser or self.student.is_staff or( self.student.is_superuser and self.student.is_staff))
            
      
    def test_url_is_valid(self):
         self.assertEqual(self.url, f'/dashboard/admin/')
    
    def test_student_cannot_access_admin_panel(self):
            redirect_url = reverse_with_next('login', self.url)
            response = self.client.get(self.url, follow=True)
            self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
            self.assertTemplateUsed(response, 'log_in.html')
            
    def test_admin_cannot_be_superuser_alone(self):
        self.assertFalse(self.superuser.is_superuser and self.superuser.is_staff==False)
    