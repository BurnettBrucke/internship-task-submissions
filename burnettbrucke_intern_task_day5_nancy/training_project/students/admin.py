from django.contrib import admin

from .models import (
    AuditLog,
    Course,
    Department,
    Feedback,
    Student,
    StudentProfile,
    UserProfile,
)


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'duration_weeks', 'is_active', 'trainer')
    list_filter = ('is_active', 'trainer')
    search_fields = ('name', 'code')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'department', 'marks', 'joined_date', 'is_active', 'user')
    list_filter = ('is_active', 'department', 'courses')
    search_fields = ('name', 'email')
    filter_horizontal = ('courses',)
    inlines = [StudentProfileInline]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'phone', 'date_of_birth')
    search_fields = ('student__name', 'phone')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """This is where an Administrator promotes an account to Trainer or
    Administrator -- role changes are never exposed on the public
    registration form."""
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'trainer', 'is_visible_to_student', 'created_at')
    list_filter = ('is_visible_to_student', 'course')
    search_fields = ('student__name', 'comment')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action')
    list_filter = ('user',)
    readonly_fields = ('timestamp',)
