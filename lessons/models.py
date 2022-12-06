from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.http import HttpRequest
import uuid

class Student(AbstractUser):
    username=models.EmailField(unique=True,verbose_name='Email')
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    def generate_invoice_number(self):
      random_uuid=str(uuid.uuid4())
      
      return f'{self.id}-{random_uuid}'


class Lesson(models.Model):
    LESSON_CHOICES =[
        ("PIANO_PRACTICE", "Piano Practice"),
        ("TRUMPET_TRAINING", "Trumpet Training"),
        ("MUSIC_THEORY", "Music Theory"),
        ("PERFORMANCE_PREP", "Performance Preparation")
    ]
    lesson_name = models.CharField(max_length = 50, choices = LESSON_CHOICES, default = "MUSIC_THEORY")

    DAYS_OF_THE_WEEK =[
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
        ("SUN", "Sunday")
    ]
    student_availability = models.CharField(max_length = 9, choices = DAYS_OF_THE_WEEK, default = "MON")

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
        blank=True,
        null=True
        )

    def __str__(self):
        return f'{self.lesson_name} - {self.student_availability}'

    def equal_to(self, HttpRequest):
        return (self.lesson_name.__eq__(HttpRequest.POST.get('lesson_name')) and
         self.student_availability.__eq__(HttpRequest.POST.get('student_availability')) and
         self.number_of_lessons.__eq__(HttpRequest.POST.get('number_of_lessons')) and
         self.interval.__eq__(HttpRequest.POST.get('interval')) and
         self.duration.__eq__(HttpRequest.POST.get('duration')) and
         self.term_period.__eq__(HttpRequest.POST.get('term_period')))


class LessonRequest(models.Model):
    student= models.ForeignKey(Student,on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete = models.CASCADE)
    is_authorised = models.BooleanField(default = False)

class BankTransfer(models.Model):
    invoice = models.CharField(
        # unique=True,
        max_length=40,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[0-9]*-[0-9]*$',
            message='invoice can only contain numbers'
        )]
    )
    first_name=models.CharField(max_length=50,blank=False)
    last_name=models.CharField(max_length=50,blank=False)
    account_number = models.CharField(
        max_length=8,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[0-9]{8,}',
            message='Account Number can only contain eight numbers'
        )]
    )
    sort_code = models.CharField(
        max_length=6,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[0-9]{6,}',
            message='Sort Code can only contain six numbers'
        )]
    )
    amount = models.PositiveSmallIntegerField(
        default=0,
        blank=False, 
        validators=[MinValueValidator(
            limit_value=0, 
            message="Amount cannot be negative"
        )]
    )

class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete = models.CASCADE)
    invoice = models.CharField(
        # unique=True,
        max_length=40,
        blank=False,
        validators=[RegexValidator(
            regex=r'^[0-9]*-[0-9]*$',
            message='invoice can only contain numbers'
        )]
    )

    
