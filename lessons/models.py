from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
#from datetime import timedelta
from django.core.validators import MinValueValidator, RegexValidator


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

class Lesson(models.Model):
    lesson_name = models.CharField(
            # look into 'choices' field option during refactor
            max_length=50,
            validators = [RegexValidator(r'^[a-zA-Z ]+$')]
        )
    duration = models.PositiveSmallIntegerField(
        default = 30,
        validators = [
            MinValueValidator(30, message="Minimum value of 30 minutes not set.")
        ])
    date = models.DateField(auto_now=False, auto_now_add=False)
    price = models.PositiveSmallIntegerField(
        default = 30,
        validators = [
            MinValueValidator(1, message="Price field must be set to a value greater than zero.")
        ])
