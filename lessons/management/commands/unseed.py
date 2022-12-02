from django.core.management.base import BaseCommand, CommandError
from lessons.models import Student, Lesson

class Command(BaseCommand):
    def handle(self, *args, **options):
        Student.objects.filter(is_staff=False, is_superuser=False).delete()
        self._delete_all_lessons()
        print("Database unseeded.")

    def _delete_all_lessons(self):
        for lesson in Lesson.objects.all():
            lesson.delete()
