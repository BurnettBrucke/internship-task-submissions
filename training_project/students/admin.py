from django.contrib import admin
from .models import (Course , Department , Student , StudentProfile , UserProfile , Enrollment , TrainerCourse , MarkHistory , Feedback , AuditLog)

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
        "department",
        "joined_date",
        "active",
    )


#    def display_courses(self, obj):
#        return ", ".join(course.course_name for course in obj.courses.all())
#
#    display_courses.short_description = "Courses"


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("student", 
                    "phone", 
                    "address", 
                    "date_of_birth")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "requested_course",
        "status",
        "created_at"
    )
    list_filter = (
        "role",
        "status",
        "requested_course",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "marks",
    )


@admin.register(TrainerCourse)
class TrainerCourseAdmin(admin.ModelAdmin):
    list_display = (
        "trainer",
        "course",
        "assigned_at",
    )

@admin.register(MarkHistory)
class MarkHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "enrollment",
        "previous_marks",
        "new_marks",
        "updated_by",
        "updated_at",
    )

    readonly_fields = (
        "enrollment",
        "previous_marks",
        "new_marks",
        "updated_by",
        "reason",
        "updated_at",
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "trainer",
        "course",
        "rating",
        "visible",
        "created_at",
    )

    list_filter = (
        "rating",
        "visible",
        "course",
    )

    search_fields = (
        "student__name",
        "trainer__username",
        "trainer__email",
        "comment",
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "timestamp",
        "user",
        "action",
        "description",
        "ip_address",
    )

    list_filter = (
        "action",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "user__email",
        "description",
        "ip_address",
    )

    readonly_fields = (
        "user",
        "action",
        "description",
        "ip_address",
        "timestamp",
        "content_type",
        "object_id",
    )

    ordering = ("-timestamp",)