from django.contrib import admin
from .models import Student, LessonRequest, Lesson

@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
   def get_queryset(self, request):
       qs=super().get_queryset(request)
       if request.user.is_staff:
           return qs
       elif request.user.is_superuser:
           return qs
       return qs.filter(author=request.user)
    
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
    list_display=[
        'student','lesson','is_authorised',
    ]