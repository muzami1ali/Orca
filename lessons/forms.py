from django import forms
from .models import Student
from django.core.validators import RegexValidator




class SignUpForms(forms.ModelForm):
    class Meta:
        model=Student
        fields=['username','first_name','last_name']

    

    
    new_password=forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message="Password must contain an uppercase letter, lowercase letter and a number"
            )
          ]
        )  
   
    password_confirmation=forms.CharField(label="Password confirmation",widget=forms.PasswordInput())


    
    
    def clean(self):
        super().clean()
        new_password=self.cleaned_data.get('new_password')
        password_confirmation=self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation','Confirmation does not match password')
 
    
    def save(self):
          super().save(commit=False)
          student=Student.objects.create_user(
                self.cleaned_data.get('username'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                password=self.cleaned_data.get('new_password'),
            )
          return student