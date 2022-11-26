from django.core.management.base import BaseCommand, CommandError
from lessons.models import Student, Lesson

class Command(BaseCommand):
    def handle(self, *args, **options):
        Student.objects.filter(is_staff=False, is_superuser=False).delete()
        self._delete_all_lessons()

    def _delete_all_lessons(self):
        for i in range(1, 7):
            Lesson.objects.filter(term_period=f'TERM{i}').delete()
