from django.test import TestCase
from lessons.models import Student,LessonRequest,BankTransfer,Invoice
from django.urls import reverse
from lessons.models import LessonRequest,Invoice,BankTransfer
class AdminPanelViewTestCase(TestCase):
    fixtures = [
       'lessons/tests/fixtures/admin_user_staff.json',
       'lessons/tests/fixtures/admin_user_staff_other.json',
       'lessons/tests/fixtures/admin_user_superuser.json',
       'lessons/tests/fixtures/admin_user_superuser_other.json'
       
    ]
    def setUp(self):
        self.url=reverse('admin_panel')
        self.staff_user=Student.objects.get(username='John.Doe@example.org')
        self.other_staff_user=Student.objects.get(username='Jane.Doe@example.org')
        self.superuser=Student.objects.get(username='Sherlock.Holmes@example.org')
        self.other_superuser=Student.objects.get(username='James.Moriarty@example.org')
    
    
    def test_only_valid_users_can_access_admin(self):
        self.assertTrue(self.staff_user)
            
       
    