'''Seed command to fill a database'''
''' @author Dean Whitbread '''
''' @version 25/11/2022 '''

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from faker import Faker
from lessons.models import Student, Lesson, LessonRequest
import random


class Command(BaseCommand):
    PASSWORD = "Password123"
    STUDENT_COUNT = 100
    ADMINISTRATOR_COUNT = 1
    REQUIRED_USERS_COUNTER = 4

    LESSON_CHOICES =["PIANO_PRACTICE", "TRUMPET_TRAINING", "MUSIC_THEORY", "PERFORMANCE_PREP"]
    DAYS_OF_THE_WEEK =["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    DURATION_CHOICES = [30, 45, 60]
    TERM_PERIOD = ['TERM1', 'TERM2', 'TERM3', 'TERM4', 'TERM5', 'TERM6']
    DURATION = [30, 60, 120]
    LESSON_COUNT = 50

    LESSON_REQUESTS_COUNT = 49      # John Doe has 1 lesson request = 50 altogether

    '''
        Constants to track the starting db id for Student and Lesson.
    '''
    STUDENT_DB_START_ID = 0
    LESSON_DB_START_ID = 0

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        Faker.seed(20)
        random.seed(15)

    def handle(self, *args, **options):
        try:
            self.seed_user_accounts()
            self.seed_lessons()
            self.seed_lesson_requests()

            print('Database seeding complete.')
        except IntegrityError:
            print('An error occurred. Unseed the database and try again.')


    ''' Methods to seed the database '''
    ''' Seed Accounts '''
    def seed_user_accounts(self):
        print('Seeding John Doe student account...')
        self.create_new_student('John', 'Doe')

        print('Seeding Petra Pickles administrator account...')
        self.create_new_student('Petra', 'Pickles', True)

        print('Seeding Marty Major director account...')
        self.create_new_student('Marty', 'Major', True, True)

        print('Seeding other administrator account...')
        self.create_new_student(self.faker.first_name(), self.faker.last_name(), True)

        counter = 0
        while counter < Command.STUDENT_COUNT:
            counter += 1
            print(f'Seeding other student accounts...{counter}',  end='\r')
            self.create_new_student(self.faker.first_name(), self.faker.last_name())
        Command.STUDENT_DB_START_ID = Student.objects.all().first().id
        print('\n')

    def create_new_student(self, f_name, l_name, staff=False, superuser=False):
        Student.objects.create_user(
            username=f'{f_name.lower()}.{l_name.lower()}@example.org',
            first_name = f_name,
            last_name = l_name,
            password=Command.PASSWORD,
            is_staff = staff,
            is_superuser = superuser,
        )

    ''' Seed Lessons '''
    def seed_lessons(self):
        counter = 0
        while counter < Command.LESSON_COUNT:
            counter += 1
            print(f'Seeding lessons...{counter}',  end='\r')
            self.create_new_lesson()
        Command.LESSON_DB_START_ID = Lesson.objects.all().first().id
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

    ''' Seed Lesson Requests '''
    def seed_lesson_requests(self):
        print(f'Seeding John Doe fufilled requests...1',  end='\r')
        self.create_new_lesson_request(
            Command.STUDENT_DB_START_ID,
            Command.LESSON_DB_START_ID + 1,
            fufilled=True
            )
        print()

        counter = 0
        while counter < Command.LESSON_REQUESTS_COUNT:
            counter += 1
            print(f'Seeding other lesson requests...{counter}',  end='\r')
            self.create_new_lesson_request(
                student_id = random.randrange(
                    Command.STUDENT_DB_START_ID + Command.REQUIRED_USERS_COUNTER,
                    Command.STUDENT_DB_START_ID + Student.objects.count()
                    ),
                lesson_id = random.randrange(
                    Command.LESSON_DB_START_ID + 1,
                    Command.LESSON_DB_START_ID + Lesson.objects.count()
                    )
                )
        print('\n')

    def create_new_lesson_request(self, student_id, lesson_id, fufilled=False):
        if fufilled:
            authorised_value = True
        else:
            authorised_value = random.randrange(0,2)

        self.lesson_requests = LessonRequest.objects.create(
            student = Student.objects.get(id=student_id),
            lesson = Lesson.objects.get(id=lesson_id),
            is_authorised = authorised_value
        )
