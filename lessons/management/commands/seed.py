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
        self.seed_database()

    def seed_database(self):
        try:
            self.seed_user_accounts()
            print('Database seeding complete.')
        except IntegrityError:
            print('An error occurred. Unseed the database and then try again.')

    def seed_user_accounts(self):
        # create three accounts (student, administrator, and director)
        self.create_new_student('John', 'Doe')
        print('Seeding John Doe student account...')

        # generate 99 student accounts (100 in total with John Doe)
        counter = 0
        while counter < Command.STUDENT_COUNT:
            print(f'Seeding student accounts...{counter}',  end='\r')
            self.create_new_student(self.faker.first_name(), self.faker.last_name())
            counter += 1

    def create_new_student(self, f_name, l_name):
        Student.objects.create_user(
            username=f'{f_name}.{l_name}@example.org',
            first_name = f_name,
            last_name = l_name,
            password=Command.PASSWORD
        )
