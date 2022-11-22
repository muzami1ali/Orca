from django.db import models
from django.contrib.auth.models import AbstractUser


#Custom UserManager


#Student model
class Student(AbstractUser):
    username=models.BigAutoField(unique=True, editable=False,primary_key=True)
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    email=models.EmailField(unique=True, blank=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    
    
    



