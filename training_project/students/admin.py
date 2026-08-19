from django.contrib import admin

from .models import (
    Student,
    Department,
    Course,
    Enrollment,
    StudentProfile,
    UserProfile,
    AuditLog,
    Feedback,
    MarksHistory,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )

    search_fields = (
        "name",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_name",
        "code",
        "duration",
        "active",
    )

    search_fields = (
        "course_name",
        "code",
    )

    list_filter = (
        "active",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "department",
        "assigned_trainer",
        "age",
        "active",
    )

    search_fields = (
        "name",
        "email",
    )

    list_filter = (
        "department",
        "active",
    )

    readonly_fields = (
        "joined_date",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "enrollment_date",
        "status",
        "marks",
    )

    search_fields = (
        "student__name",
        "student__email",
        "course__course_name",
        "course__code",
    )

    list_filter = (
        "status",
        "course",
    )

    readonly_fields = (
        "enrollment_date",
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "phone",
        "date_of_birth",
    )

    search_fields = (
        "student__name",
        "student__email",
        "phone",
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "is_approved",
        "account_created",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    list_filter = (
        "role",
        "is_approved",
    )

    readonly_fields = (
        "account_created",
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "action",
        "ip_address",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "description",
        "ip_address",
    )

    list_filter = (
        "action",
        "timestamp",
    )

    readonly_fields = (
        "timestamp",
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "trainer",
        "enrollment",
        "rating",
        "visible_to_student",
        "created_at",
    )

    search_fields = (
        "student__name",
        "student__email",
        "trainer__username",
    )

    list_filter = (
        "rating",
        "visible_to_student",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(MarksHistory)
class MarksHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "enrollment",
        "previous_marks",
        "new_marks",
        "updated_by",
        "updated_at",
    )

    search_fields = (
        "student__name",
        "student__email",
        "updated_by__username",
        "reason",
    )

    list_filter = (
        "updated_at",
    )

    readonly_fields = (
        "updated_at",
    )