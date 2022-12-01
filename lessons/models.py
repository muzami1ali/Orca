from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator


class Student(AbstractUser):
    username=models.EmailField(unique=True,verbose_name='Email')
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


class Lesson(models.Model):
    LESSON_CHOICES =[
        ("PIANO_PRACTICE", "Piano Practice"),
        ("TRUMPET_TRAINING", "Trumpet Training"),
        ("MUSIC_THEORY", "Music Theory"),
        ("PERFORMANCE_PREP", "Performance Preparation")
    ]
    lesson_name = models.CharField(max_length = 50, choices = LESSON_CHOICES, default = "MUSIC_THEORY")

    student_availability = models.DateField(auto_now=False, auto_now_add=False)

    number_of_lessons = models.PositiveSmallIntegerField(
        default = 1,
        validators = [
            MinValueValidator(1, message="Must complete at least one lesson."),
            MaxValueValidator(10, message="Maximum number of lessons exceeded. Messons per term is 10")
            ]
        )

    interval = models.PositiveSmallIntegerField(
        default = 1,
        validators = [
            MinValueValidator(1, message="Interval period between lessons must be at least 1 week."),
            MaxValueValidator(2, message="Maximum interval period between lessons of 2 weeks not selected.")
            ]
        )

    DURATION_CHOICES = [(30, 30), (45, 45), (60, 60)]
    duration = models.PositiveSmallIntegerField(
        choices = DURATION_CHOICES, default = 30,
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

    additional_information = models.CharField(
        max_length=200,
        validators=[MaxLengthValidator(200)],
        blank=True
        )

    def __str__(self):
        return f'{self.lesson_name} - {self.student_availability}'


class LessonRequest(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete = models.CASCADE)
    is_authorised = models.BooleanField(default = False)
