from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import (
    Student,
    Department,
    Course,
    StudentProfile,
    UserProfile,
    TrainerAssignment,
    AuditLog,
    Feedback,
    MarksHistory,
)

from .utils import create_audit_log


admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(StudentProfile)


# ---------------------------------------------------------
# Custom User Admin
# ---------------------------------------------------------

class CustomUserAdmin(UserAdmin):

    def save_model(self, request, obj, form, change):

        # Check whether an existing user's active status
        # has changed.
        status_changed = False
        old_status = None

        if change:

            old_user = User.objects.get(
                pk=obj.pk
            )

            old_status = old_user.is_active

            if old_status != obj.is_active:
                status_changed = True

        # Save the user normally.
        super().save_model(
            request,
            obj,
            form,
            change
        )

        # Create audit log only when the account status
        # actually changes.
        if status_changed:

            if obj.is_active:

                status = "activated"

            else:

                status = "deactivated"

            create_audit_log(
                user=request.user,
                action=AuditLog.Action.STATUS_CHANGE,
                object_name=f"User: {obj.username}",
                description=(
                    f"User '{obj.username}' account "
                    f"was {status} by "
                    f"'{request.user.username}'."
                ),
                request=request,
            )


# Remove Django's default UserAdmin registration.
admin.site.unregister(User)

# Register User using our custom admin.
admin.site.register(
    User,
    CustomUserAdmin
)


# ---------------------------------------------------------
# User Profile Admin
# ---------------------------------------------------------

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "is_approved",
    )

    list_filter = (
        "role",
        "is_approved",
    )

    search_fields = (
        "user__username",
    )


# ---------------------------------------------------------
# Audit Log Admin
# ---------------------------------------------------------

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "action",
        "object_name",
        "ip_address",
        "timestamp",
    )

    list_filter = (
        "action",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "object_name",
        "description",
    )

    ordering = (
        "-timestamp",
    )


# ---------------------------------------------------------
# Trainer Assignment Admin
# ---------------------------------------------------------

@admin.register(TrainerAssignment)
class TrainerAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "trainer",
        "student",
        "course",
        "assigned_date",
    )

    list_filter = (
        "course",
        "assigned_date",
    )

    search_fields = (
        "trainer__username",
        "student__name",
        "course__course_name",
    )


# ---------------------------------------------------------
# Feedback Admin
# ---------------------------------------------------------

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        "trainer",
        "student",
        "course",
        "rating",
        "is_visible",
        "created_at",
    )

    list_filter = (
        "course",
        "rating",
        "is_visible",
    )

    search_fields = (
        "trainer__username",
        "student__name",
        "feedback",
    )

    ordering = (
        "-created_at",
    )


# ---------------------------------------------------------
# Marks History Admin
# ---------------------------------------------------------

@admin.register(MarksHistory)
class MarksHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course",
        "previous_marks",
        "new_marks",
        "updated_by",
        "updated_at",
    )

    list_filter = (
        "course",
        "updated_at",
    )

    search_fields = (
        "student__name",
        "updated_by__username",
        "reason",
    )

    ordering = (
        "-updated_at",
    )