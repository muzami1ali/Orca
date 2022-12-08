from django.test import TestCase
from django.urls import reverse
from lessons.models import LessonRequest,Invoice,BankTransfer
class AdminPanelViewTestCase(TestCase):
       fixtures = [
       'lessons/tests/fixtures/admin_user_staff.json'

    ]
       def setUp(self):
           self.url=reverse('admin_panel')
