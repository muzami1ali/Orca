from django.contrib import admin
from .models import Student, LessonRequest, Lesson, BankTransfer,Invoice

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

@admin.register(BankTransfer)
class BankTransferAdmin(admin.ModelAdmin):
    list_display=[
        'invoice', 'first_name', 'last_name', 'account_number', 'sort_code', 'amount' , 'approved'
    ]

@admin.register(LessonRequest)
class LessonRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'student_id', 'student', 'lesson_id', 'lesson',
    ]


@admin.register(Invoice)
class Invoice(admin.ModelAdmin):
    list_display=[
        'id', 'student', 'lesson'
    ]

