from django.contrib import admin
from .models import Course , Department , Student , StudentProfile

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_name",
                    "code",
                    "duration",
                    "active_status")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description"
    )
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "age",
        "marks",
        "department",
        "joined_date",
        "active",
    )


    def display_courses(self, obj):
        return ", ".join(course.course_name for course in obj.courses.all())

    display_courses.short_description = "Courses"


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("student", "phone", "address", "date_of_birth")