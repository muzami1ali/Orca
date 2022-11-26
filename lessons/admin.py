from django.contrib import admin
from .models import Student, Lesson

@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
   list_display=[
       'id','username','first_name','last_name','is_active','password',
   ]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Lesson._meta.get_fields()
    ]
