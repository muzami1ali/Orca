import email
from django.test import TestCase
from lessons.forms import SignUpForms
from lessons.models import Student
from django import forms
from django.contrib.auth.hashers import check_password

class SignUpFormTestCase(TestCase):
    def setUp(self):
        self.form_input={
            'first_name':'John',
            'last_name':'Doe',
            'email':'johndoe@example.com',
            'new_password':'Password123',
            'password_confirmation':'Password123'
            
        }
        
    #Form accepts valid input data
    def test_valid_sign_up_form(self):  
        form=SignUpForms(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    
    #Form has necessary fields
    def test_form_has_necessary_fields(self):
        form=SignUpForms()
        self.assertIn("first_name",form.fields)
        self.assertIn("last_name",form.fields)
        self.assertIn("email",form.fields)
        email_field=form.fields['email']
        self.assertTrue(isinstance(email_field,forms.EmailField))
        self.assertIn("new_password",form.fields)
        new_password_widget=form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget,forms.PasswordInput))
        self.assertIn("password_confirmation",form.fields)
        password_confirmation_widget=form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget,forms.PasswordInput))
        
    
    
    #New password has correct format
    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password']='password123'
        self.form_input['password_confirmation']='password123'
        form=SignUpForms(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password']='PASSWORD123'
        self.form_input['password_confirmation']='PASSWORD123'
        form=SignUpForms(data=self.form_input)
        self.assertFalse(form.is_valid())
        
        
    def test_password_must_contains_number(self):
        self.form_input['new_password']='PasswordABC'
        self.form_input['password_confirmation']='PasswordABC'
        form=SignUpForms(data=self.form_input)
        self.assertFalse(form.is_valid())
  
    
    #New password and confirmation password must be identical
    def test_new_password_and_password_are_identical(self):
        self.form_input['password_confirmation']='WrongPassword123'
        form=SignUpForms(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    
    def test_form_must_save_correctly(self):
        form= SignUpForms(data=self.form_input)
        before_count=Student.objects.count()
        form.save()
        after_count=Student.objects.count()
        self.assertEqual(after_count,before_count+1)
        user=Student.objects.get(email='johndoe@example.com')
        self.assertEqual(user.first_name,'John')
        self.assertEqual(user.last_name,'Doe')
        self.assertEqual(user.email,'johndoe@example.com')
        is_password_correct=check_password('Password123',user.password)
        self.assertTrue(is_password_correct)
      