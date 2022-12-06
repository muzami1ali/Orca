from django.core.management.base import BaseCommand, CommandError
from lessons.models import Student, Lesson

class Command(BaseCommand):
    def handle(self, *args, **options):
        Student.objects.all().delete()
        Lesson.objects.all().delete()
        
        print("Database unseeded.")
