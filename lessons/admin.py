from django.contrib import admin
from .models import Student
@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
   list_display=[
       'username','first_name','last_name','email','is_active','password','id',
   ]
