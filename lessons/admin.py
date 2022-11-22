from django.contrib import admin
from .models import Student
@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""

    list_display = [
        'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser' #'id',
    ]