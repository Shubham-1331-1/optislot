from django.contrib import admin
from .models import Allotment


@admin.register(Allotment)
class AllotmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'elective', 'allotted_at']
    list_filter = ['elective']
    search_fields = ['student__usn', 'student__username', 'elective__code']
    readonly_fields = ['allotted_at']
