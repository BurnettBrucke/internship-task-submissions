from django.contrib import admin
from .models import student

# Register your models here.



@admin.register(student)
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

    list_filter = ("course", "active")
    search_fields = ("name", "email", "course")