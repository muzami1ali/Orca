'''Seed command to fill a database'''
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from faker import Faker
from lessons.models import Student

class Command(BaseCommand):
    PASSWORD = "Password123"
    STUDENT_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        Faker.seed(20)

    def handle(self, *args, **options):
        self.create_all_users()

    def create_student_user(self, unique_id):
        first_name=self.faker.first_name(),
        last_name=self.faker.last_name(),
        email = self.generate_email(first_name, last_name)
        Student.objects.create_user(
            username=email,
            first_name = first_name,
            last_name = last_name,
            email=email,
            id=self.generate_id_number(unique_id),
            password=Command.PASSWORD
        )

    def generate_email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email

    def generate_id_number(self, unique_id):
        unique_id += 1
        return unique_id

    def create_all_users(self):
        # create three accounts
        Student.objects.create_user(
            username='john.doe@example.org',
            first_name = 'John',
            last_name = 'Doe',
            email='john.doe@example.org',
            id=1,
            password=Command.PASSWORD
        )

        # generate 100 students
        unique_id = 3
        student_user_count = 0
        while student_user_count < Command.STUDENT_COUNT:
            print(f'Seeding student user {student_user_count}',  end='\r')
            try:
                self.create_student_user(unique_id)
            except (IntegrityError):
                continue
            student_user_count += 1

        print('User seeding complete')
