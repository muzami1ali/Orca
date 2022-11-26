from django.contrib import admin
from .models import Student, LessonRequest

@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
   list_display=[
       'id','username','first_name','last_name','is_active','password',
   ]

@admin.register(LessonRequest)
class LessonRequestAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in LessonRequest._meta.get_fields()
    ]
