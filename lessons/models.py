from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import MinValueValidator, RegexValidator

class Student(AbstractUser):
    username=models.BigAutoField(unique=True, editable=False,primary_key=True)
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    email=models.EmailField(unique=True, blank=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


class Lesson(models.Model):
    lesson_name = models.CharField(
            max_length=50,
            validators = [RegexValidator(r'^[a-zA-Z ]+$')]
        )
    duration = models.PositiveSmallIntegerField(
        default = 30,
        validators = [MinValueValidator(30, message="Minimum value of 30 minutes not set.")]
        )
    date = models.DateField(auto_now=False, auto_now_add=False)
    price = models.PositiveSmallIntegerField(
        default = 30,
        validators = [MinValueValidator(1, message="Price field must be set to a value greater than zero.")]
        )

    TERM_PERIOD_CHOICES =[
        ("TERM1", "Term 1"),
        ("TERM2", "Term 2"),
        ("TERM3", "Term 3"),
        ("TERM4", "Term 4"),
        ("TERM5", "Term 5"),
        ("TERM6", "Term 6")
    ]
    term_period = models.CharField(max_length = 6, choices = TERM_PERIOD_CHOICES, default = "TERM1")


class LessonRequest(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete = models.CASCADE)
    is_authorised = models.BooleanField(default = False)
