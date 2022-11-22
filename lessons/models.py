from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid

#Student model
class Student(AbstractUser):
    username= models.CharField(
        default='@nu11',
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    email=models.EmailField(unique=True, blank=False)
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    # USERNAME_FIELD='id'
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    



