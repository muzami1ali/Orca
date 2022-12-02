'''Seed command to fill a database'''
''' @author Dean Whitbread '''
''' @version 25/11/2022 '''

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from faker import Faker
from lessons.models import Student, Lesson
from datetime import datetime
import random


class Command(BaseCommand):
    PASSWORD = "Password123"
    STUDENT_COUNT = 100

    LESSON_NAMES = ['Piano Practice', 'Trumpet Techniques', 'Guitar Guidance']
    TERM_PERIOD = ['TERM1', 'TERM2', 'TERM3', 'TERM4', 'TERM5', 'TERM6']
    DURATION = [30, 60, 120]
    LESSON_COUNT = 100


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
        self.lesson = Lesson(
            lesson_name = Command.LESSON_NAMES[random.randrange(0, 3)],
            duration = Command.DURATION[random.randrange(0, 3)],
            date = self.faker.date_between_dates(date_start=datetime(2022,9,1), date_end=datetime(2023,7,21)),
            price = 50,
            term_period = Command.TERM_PERIOD[random.randrange(0, 6)]
        )
        self.lesson.save()
