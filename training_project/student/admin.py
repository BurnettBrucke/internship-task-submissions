from django.contrib import admin
from .models import (
    Student, Department, Course, StudentProfile,
    UserProfile, AuditLog, Feedback, MarksHistory,
)


# ──────────────────────────────────────────────────────────────────────────────
# Department Admin
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'description']
    search_fields = ['name']


# ──────────────────────────────────────────────────────────────────────────────
# Course Admin
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['name', 'code', 'duration', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['name', 'code']


# ──────────────────────────────────────────────────────────────────────────────
# Student Admin — Day 2 Task 4
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display      = ['name', 'email', 'age', 'course', 'marks',
                         'is_active', 'department', 'trainer', 'joined_date']
    list_filter       = ['is_active', 'department']
    search_fields     = ['name', 'email']
    filter_horizontal = ['enrolled_courses']
    readonly_fields   = ['joined_date']


# ──────────────────────────────────────────────────────────────────────────────
# StudentProfile Admin — Day 3 Task 2
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['student', 'phone', 'address', 'date_of_birth']


# ──────────────────────────────────────────────────────────────────────────────
# UserProfile Admin — Day 4 Task 1
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'role', 'is_approved']
    list_filter   = ['role', 'is_approved']
    search_fields = ['user__username', 'user__email']
    # Allow admin to quickly toggle approval from the list view
    list_editable = ['is_approved']


# ──────────────────────────────────────────────────────────────────────────────
# AuditLog Admin — Day 4 Task 3
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display  = ['timestamp', 'user', 'action_type', 'description', 'ip_address']
    list_filter   = ['action_type']
    search_fields = ['user__username', 'description']
    readonly_fields = ['timestamp', 'user', 'action_type', 'description', 'ip_address']
    # Audit logs should never be editable from the admin panel
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False


# ──────────────────────────────────────────────────────────────────────────────
# Feedback Admin — Day 4 Task 3
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display  = ['trainer', 'student', 'course', 'rating', 'is_visible', 'created_at']
    list_filter   = ['is_visible', 'rating']
    search_fields = ['trainer__username', 'student__name']
    list_editable = ['is_visible']


# ──────────────────────────────────────────────────────────────────────────────
# MarksHistory Admin — Day 4 Task 3
# ──────────────────────────────────────────────────────────────────────────────
@admin.register(MarksHistory)
class MarksHistoryAdmin(admin.ModelAdmin):
    list_display  = ['student', 'updated_by', 'old_marks', 'new_marks', 'reason', 'updated_at']
    readonly_fields = ['student', 'updated_by', 'old_marks', 'new_marks', 'reason', 'updated_at']
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
