from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "age",
        "course",
        "marks",
        "joined_date",
        "active",
    )
    list_filter = (
        "course",
        "active"       
    )
    search_fields = (
        "name",
        "email",
    )