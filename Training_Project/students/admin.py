from django.contrib import admin
from .models import AuditLog
from .models import (
    Student,
    Department,
    StudentProfile,
    Course,
    UserProfile,
    CourseMark,
    MarksHistory,
    Feedback,
)


admin.site.register(Student)

admin.site.register(Department)

admin.site.register(StudentProfile)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'code', 'duration', 'display_trainers', 'active')

    def display_trainers(self, obj):
        return ", ".join(
            trainer.username for trainer in obj.trainer.all()
        )

    display_trainers.short_description = "Trainer"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'role')

    list_filter = ('role',)

    search_fields = ('user__username', 'user__email')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'description')
    ordering = ('-timestamp',)

@admin.register(CourseMark)
class CourseMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks', 'updated_by', 'updated_at')
    list_filter = ('course', 'updated_by')
    search_fields = ('student__name', 'course__course_name', 'updated_by__username')
    ordering = ('-updated_at',)


@admin.register(MarksHistory)
class MarksHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'previous_marks',
        'new_marks',
        'updated_by',
        'reason',
        'updated_at',
    )
    list_filter = ('course', 'updated_by')
    search_fields = (
        'student__name',
        'course__course_name',
        'updated_by__username',
        'reason',
    )
    ordering = ('-updated_at',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'trainer',
        'course',
        'rating',
        'is_visible',
        'created_at',
        'updated_at',
    )
    list_filter = ('course', 'trainer', 'rating', 'is_visible')
    search_fields = (
        'student__name',
        'trainer__username',
        'course__course_name',
        'comment',
    )
    ordering = ('-created_at',)