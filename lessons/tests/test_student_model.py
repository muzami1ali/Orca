"""Tests for Student model"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Student
import uuid
    # username=models.BigAutoField(unique=True,editable=False,primary_key=True)
    # first_name=models.CharField(max_length=50,blank=False)
    # last_name=models.CharField(max_length=50,blank=False)
    # email=models.EmailField(unique=True, blank=False)
    # USERNAME_FIELD='email'
    # REQUIRED_FIELDS=[]
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)


class StudentModelTest(TestCase):
    def setUp(self):
        self.user=Student.objects.create_user(
            username='1',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            password='Password123'
            
        )
    def _create_second_user(self):
        user=Student.objects.create_user(
            username='2',
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.com',
            password ='Password123'
        )
        return user
    
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
    
    """First Name tests"""
    def test_student_first_name_cannot_be__blank(self):
        self.user.first_name=''
        self._assert_student_user_is_invalid
    
    def test_student_first_name_may_contain_50_characters(self):
        self.user.first_name='x'*50
        self._assert_student_user_is_valid()
    
    def test_student_first_name_may_not_contain_more_than_50_characters(self):
        self.user.first_name='x'*51
        self._assert_student_user_is_invalid()
        
    """Last Name tests"""   
    def test_student_last_name_cannot_be__blank(self):
        self.user.last_name=''
        self._assert_student_user_is_invalid
    
    def test_student_last_name_may_contain_50_characters(self):
        self.user.last_name='x'*50
        self._assert_student_user_is_valid()
    
    def test_student_last_name_may_not_contain_more_than_50_characters(self):
        self.user.last_name='x'*51
        self._assert_student_user_is_invalid()
        
    """Email tests"""
    def test_email_must_not_be_blank(self): 
        self.user.email=''
        self._assert_student_user_is_invalid() 
              
    def test_email_uniqueness(self):
        second_user=self._create_second_user()
        self.user.email=second_user.email
        self._assert_student_user_is_invalid()
    
    def test_email_must_contain_username(self):
        self.user.email='@example.org'
        self._assert_student_user_is_invalid()
    
    def test_email_must_contain_at_symbol(self):
        self.user.email='johndoe.example.org'
        self._assert_student_user_is_invalid()
    
    def test_email_must_contain_domain_name(self):
        self.user.email='johndoe@.org'
        self._assert_student_user_is_invalid()
        
    def test_email_must_contain_domain(self):
        self.user.email='johndoe@example'
        self._assert_student_user_is_invalid()
        
    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email='johndoe@@example'
        self._assert_student_user_is_invalid()
     
   