from django.contrib import admin
from .models import UserProfile, student,department,StudentProfile,Course

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
    )

    list_filter = (
        "role",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

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


@admin.register(department)
class DepartmentAdmin(admin.ModelAdmin):
    pass
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    pass
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

   