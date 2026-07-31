from django.contrib import admin
from .models import Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'course', 'marks', 'joined_date', 'active_status')
    list_filter = ('active_status', 'course', 'joined_date')
    search_fields = ('name', 'email', 'course')
