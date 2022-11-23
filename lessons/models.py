from django.db import models
from django.contrib.auth.models import AbstractUser








#Student model
class Student(AbstractUser):
    username=models.EmailField(unique=True,verbose_name='Email')
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    
    
    



