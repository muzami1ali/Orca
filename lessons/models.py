from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator


class Student(AbstractUser):
    username=models.EmailField(unique=True,verbose_name='Email')
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
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

    def __str__(self):
        return f'{self.lesson_name} - {self.date}'


class LessonRequest(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete = models.CASCADE)
    is_authorised = models.BooleanField(default = False)

class bankTransfers(models.Model):
    invoice = models.CharField(max_length=40,blank=False)
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    Account_Number = models.CharField(max_length=8,blank=False)
    Sort_Code = models.CharField(max_length=6,blank=False)
    Amount = models.PositiveSmallIntegerField(default=0,blank=False)
