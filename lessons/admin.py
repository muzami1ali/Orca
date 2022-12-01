from django.contrib import admin
from .models import Student, LessonRequest, Lesson, bankTransfers

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

@admin.register(bankTransfers)
class BankTransferAdmin(admin.ModelAdmin):
    list_display=[
        'invoice', 'first_name', 'last_name', 'Account_Number', 'Sort_Code', 'Amount' ,
    ]
