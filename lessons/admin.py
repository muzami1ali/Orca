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
        'id', 'lesson_name', 'date', 'duration', 'price', 'term_period',
    ]

@admin.register(LessonRequest)
class LessonRequestAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in LessonRequest._meta.get_fields()
