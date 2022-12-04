from django.contrib import admin
from .models import Student, LessonRequest, Lesson, bankTransfers,Invoice, InvoiceNumber



@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
   search_fields = ("username__startswith", )
   def get_queryset(self, request):
       qs=super().get_queryset(request)
       if request.user.is_staff:
           return qs
       elif request.user.is_superuser:
           return qs
       return qs.filter(author=request.user)
    
    
   list_display=[
       'id','username','first_name','last_name','is_active','password','is_staff','is_superuser',
   ]
   

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    search_fields=('term_period__endswith',)
    list_display = [
        'id', 'lesson_name', 'student_availability', 'number_of_lessons',
         'interval', 'duration', 'term_period', 'additional_information'
    ]

@admin.register(bankTransfers)
class BankTransferAdmin(admin.ModelAdmin):
    list_display=[
        'invoice', 'first_name', 'last_name', 'Account_Number', 'Sort_Code', 'Amount' ,
    ]
   

@admin.register(LessonRequest)
class LessonRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'student_id', 'student', 'lesson_id', 'lesson','is_authorised',
    ]
    
    actions=['enable_selected','disable_selected']
    def enable_selected(self,request,queryset):
        queryset.update(is_authorised=True)
    def disable_selected(self,request,queryset):
        queryset.update(is_authorised=False)
    enable_selected.short_description="Authorise the lessons"
    disable_selected.short_description="Revoke the lesson's authorisation"
   
        


@admin.register(Invoice)
class Invoice(admin.ModelAdmin):
    list_display=[
        'refNumber', 'student', 'lesson'
    ]

@admin.register(InvoiceNumber)
class InvoiceNumber(admin.ModelAdmin):
    list_display=[
        
    ]

