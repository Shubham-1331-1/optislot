from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ['username', 'usn', 'get_full_name', 'cgpa', 'date_joined', 'is_staff']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'usn', 'first_name', 'last_name']
    ordering = ['-cgpa', 'date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Student Info', {'fields': ('usn', 'cgpa')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Student Info', {'fields': ('usn', 'cgpa', 'first_name', 'last_name', 'email')}),
    )
