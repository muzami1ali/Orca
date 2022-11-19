from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid

#Student model
class Student(AbstractBaseUser):
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    email=models.EmailField(unique=True, blank=False)
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    USERNAME_FIELD='id'

    
    
    
    



