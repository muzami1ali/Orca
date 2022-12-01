from django.contrib import admin
from .models import Student, LessonRequest, Lesson

@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
   list_display=[
       'id','username','first_name','last_name','is_active','password',
   ]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'lesson_name', 'student_availability', 'number_of_lessons',
         'interval', 'duration', 'term_period', 'additional_information'
    ]
