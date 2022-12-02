'''Seed command to fill a database'''
''' @author Dean Whitbread '''
''' @version 25/11/2022 '''

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from faker import Faker
from lessons.models import Student, Lesson
import random


class Command(BaseCommand):
    PASSWORD = "Password123"
    STUDENT_COUNT = 100

    LESSON_CHOICES =["PIANO_PRACTICE", "TRUMPET_TRAINING", "MUSIC_THEORY", "PERFORMANCE_PREP"]
    DAYS_OF_THE_WEEK =["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    DURATION_CHOICES = [30, 45, 60]
    TERM_PERIOD = ['TERM1', 'TERM2', 'TERM3', 'TERM4', 'TERM5', 'TERM6']

    MORE_INFO = ['', 'Please assign tutor, Jason Doe.', 'Please give me evening lessons.']
    LESSON_COUNT = 50


    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        Faker.seed(20)
        random.seed(10)

    def handle(self, *args, **options):
        try:
            self.seed_user_accounts()
            self.seed_lessons()

            print('Database seeding complete.')
        except IntegrityError:
            print('An error occurred. Unseed the database and try again.')


    '''Methods to seed the database'''
    def seed_user_accounts(self):
        # create three accounts (student, administrator, and director)
        print('Seeding John Doe student account...')
        self.create_new_student('John', 'Doe')

        # generate 100 student accounts
        counter = 0
        while counter < Command.STUDENT_COUNT:
            counter += 1
            print(f'Seeding student accounts...{counter}',  end='\r')
            self.create_new_student(self.faker.first_name(), self.faker.last_name())
        print('\n')

    def create_new_student(self, f_name, l_name):
        Student.objects.create_user(
            username=f'{f_name}.{l_name}@example.org',
            first_name = f_name,
            last_name = l_name,
            password=Command.PASSWORD
        )

    def seed_lessons(self):
        counter = 0
        while counter < Command.LESSON_COUNT:
            counter += 1
            print(f'Seeding lessons...{counter}',  end='\r')
            self.create_new_lesson()
        print('\n')

    def create_new_lesson(self):
        self.lesson = Lesson.objects.create(
            lesson_name = Command.LESSON_CHOICES[random.randrange(0, 4)],
            student_availability = Command.DAYS_OF_THE_WEEK[random.randrange(0, 7)],
            number_of_lessons = random.randrange(1, 11),
            interval = random.randrange(1, 3),
            duration = Command.DURATION_CHOICES[random.randrange(0, 3)],
            term_period = Command.TERM_PERIOD[random.randrange(0, 6)],
            additional_information = Command.MORE_INFO[random.randrange(0, 3)]
        )
