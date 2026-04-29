from django.contrib import admin
from .models import Elective, Choice


@admin.register(Elective)
class ElectiveAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'total_seats', 'available_seats', 'fill_percentage', 'status']
    search_fields = ['name', 'code']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['student', 'elective', 'priority', 'submitted_at']
    list_filter = ['priority', 'elective']
    search_fields = ['student__usn', 'student__username']
