from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'course', 'marks', 'joined_date', 'is_active')
    list_filter = ('is_active', 'course')
    search_fields = ('name', 'email', 'course')
