from django.contrib import admin
from .models import Student, LessonRequest, Lesson, bankTransfers


    
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
   def has_delete_permission(self, request,object=None):
       return False
     
   def has_change_permission(self, request,object=None):
       if request.user.is_staff==True or request.user.is_superuser==True:
           return  True
       return False
   
       
   def has_add_permission(self, request):
       if request.user.is_superuser==True:
           return True
       return False
       
    
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
        'id', 'student_id', 'student', 'lesson_id', 'lesson',
    ]
    def has_delete_permission(self, request,object=None):
       return False
     
    def has_change_permission(self, request,object=None):
       if request.user.is_staff==True or request.user.is_superuser==True:
           return  True
       return False
   
       
    def has_add_permission(self, request):
       if request.user.is_superuser==True:
           return True
       return False
      
    
@admin.register(LessonRequest)
class LessonRequestAdmin(admin.ModelAdmin):
    list_display=[
     'get_student_id','student','lesson','is_authorised',
    ]
    def has_add_permission(self, request) :
        return False

    @admin.display(ordering='id',description='Student ID')
    def get_student_id(self,obj):
        return obj.student.id
    