from django.contrib.contenttypes.models import ContentType

from .models import AuditLog


def get_client_ip(request):
    """
    Return the client's IP address from the request.
    """

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def create_audit_log(
    request,
    action,
    description,
    affected_object=None,
    user=None,
):
    """
    Create an audit log entry for a user action.
    """

    if user is None:
        user = request.user if request.user.is_authenticated else None

    content_type = None
    object_id = None

    if affected_object is not None:

        content_type = ContentType.objects.get_for_model(
            affected_object
        )

        object_id = affected_object.pk

    return AuditLog.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=get_client_ip(request),
        content_type=content_type,
        object_id=object_id,
    )

def audit_login(request, user):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.LOGIN,
        description="User logged in successfully.",
        user=user,
    ) 

def audit_logout(request, user):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.LOGOUT,
        description="User logged out.",
        user=user,
    )

def audit_failed_login(
    request,
    user=None,
    attempt_number=None,
):

    if user is None:

        description = (
            "Failed login attempt for unknown account."
        )

    elif attempt_number is not None:

        description = (
            f"Failed login attempt "
            f"({attempt_number}/5)."
        )

    else:

        description = "Failed login attempt."

    return create_audit_log(
        request=request,
        action=AuditLog.Action.FAILED_LOGIN,
        description=description,
        user=user,
    )

def audit_account_blocked(request, user):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.FAILED_LOGIN,
        description=(
            "Account blocked after reaching "
            "5 failed login attempts."
        ),
        user=user,
    )

def audit_blocked_login(request, user):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.FAILED_LOGIN,
        description=(
            "Login attempt rejected because "
            "the account is blocked."
        ),
        user=user,
    )

def audit_student_created(request, student):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.CREATE,
        description=(
            f"Student '{student.name}' was created."
        ),
        affected_object=student,
    )

def audit_student_updated(request, student):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.UPDATE,
        description=(
            f"Student '{student.name}' was updated."
        ),
        affected_object=student,
    )

def audit_student_deleted(
    request,
    student_name,
    student_id,
):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.DELETE,
        description=(
            f"Student '{student_name}' "
            f"(ID: {student_id}) was deleted."
        ),
    )

def audit_course_created(request, course):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.CREATE,
        description=(
            f"Course '{course.course_name}' was created."
        ),
        affected_object=course,
    )

def audit_course_updated(request, course):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.UPDATE,
        description=(
            f"Course '{course.course_name}' was updated."
        ),
        affected_object=course,
    )

def audit_course_status_changed(
    request,
    course,
):

    status = (
        "activated"
        if course.active_status
        else "deactivated"
    )

    return create_audit_log(
        request=request,
        action=AuditLog.Action.UPDATE,
        description=(
            f"Course '{course.course_name}' "
            f"was {status}."
        ),
        affected_object=course,
    )

def audit_trainer_deleted(request, trainer_username, trainer_id):
    return create_audit_log(
        request=request,
        action=AuditLog.Action.DELETE,
        description=(
            f"Trainer '{trainer_username}' "
            f"(ID: {trainer_id}) was deleted."
        ),
    )


def audit_trainer_approved(
    request,
    profile,
    course,
):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.ACCOUNT_STATUS_CHANGE,
        description=(
            f"Trainer '{profile.user.username}' "
            f"was approved for course "
            f"'{course.course_name}'."
        ),
        affected_object=profile,
    )

def audit_trainer_rejected(
    request,
    profile,
):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.ACCOUNT_STATUS_CHANGE,
        description=(
            f"Trainer '{profile.user.username}' "
            f"was rejected."
        ),
        affected_object=profile,
    )

def audit_user_activated(request, profile):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.ACCOUNT_STATUS_CHANGE,
        description=(
            f"User '{profile.user.username}' "
            f"was activated."
        ),
        affected_object=profile,
    )
def audit_user_deactivated(request, profile):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.ACCOUNT_STATUS_CHANGE,
        description=(
            f"User '{profile.user.username}' "
            f"was deactivated."
        ),
        affected_object=profile,
    )

def audit_marks_updated(
    request,
    enrollment,
    previous_marks,
    new_marks,
    reason,
):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.MARKS_UPDATE,
        description=(
            f"Marks updated for "
            f"'{enrollment.student.name}' "
            f"in '{enrollment.course.course_name}': "
            f"{previous_marks} → {new_marks}. "
            f"Reason: {reason}"
        ),
        affected_object=enrollment,
    )

def audit_feedback_created(
    request,
    feedback,
):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.FEEDBACK_CREATE,
        description=(
            f"Feedback created for "
            f"'{feedback.student.name}' "
            f"for course "
            f"'{feedback.course.course_name}'. "
            f"Rating: {feedback.rating}/5."
        ),
        affected_object=feedback,
    )

def audit_feedback_updated(
    request,
    feedback,
):

    return create_audit_log(
        request=request,
        action=AuditLog.Action.UPDATE,
        description=(
            f"Feedback for "
            f"'{feedback.student.name}' "
            f"in '{feedback.course.course_name}' "
            f"was updated."
        ),
        affected_object=feedback,
    )