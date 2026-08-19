from django.db import transaction
from django.db.models import Avg

from .models import (
    Student,
    Course,
    Department,
    Enrollment,
    Feedback,
    MarksHistory,
    AuditLog,
)


def get_dashboard_statistics():
    """
    Returns common dashboard statistics.
    Marks are calculated from Enrollment.
    """

    average_marks = Enrollment.objects.aggregate(
        Avg("marks")
    )["marks__avg"] or 0

    highest_enrollment = (
        Enrollment.objects
        .filter(marks__isnull=False)
        .select_related("student", "course")
        .order_by("-marks")
        .first()
    )

    recent_students = (
        Student.objects
        .order_by("-joined_date")[:5]
    )

    return {
        "total_students": Student.objects.count(),

        "total_active_students": Student.objects.filter(
            active=True
        ).count(),

        "total_departments": Department.objects.count(),

        "total_courses": Course.objects.count(),

        "average_marks": average_marks,

        "highest_student": (
            highest_enrollment.student
            if highest_enrollment
            else None
        ),

        "recent_students": recent_students,
    }


@transaction.atomic
def update_student_marks(
    enrollment,
    new_marks,
    updated_by,
    reason=""
):
    """
    Updates marks for a specific enrollment,
    creates marks history and audit log.
    """

    # Trainer ownership check
    if (
        hasattr(updated_by, "profile")
        and updated_by.profile.role == "trainer"
    ):

        if enrollment.student.assigned_trainer != updated_by:
            raise PermissionError(
                "You can update marks only for your assigned students."
            )

    previous_marks = enrollment.marks

    # Update marks
    enrollment.marks = new_marks

    # Validate model
    enrollment.full_clean(
        exclude=[
            "student",
            "course",
        ]
    )

    enrollment.save(
        update_fields=["marks"]
    )

    # Store marks history
    history = MarksHistory.objects.create(
        student=enrollment.student,
        enrollment=enrollment,
        previous_marks=(
            previous_marks
            if previous_marks is not None
            else 0
        ),
        new_marks=new_marks,
        updated_by=updated_by,
        reason=reason,
    )

    # Audit log
    AuditLog.objects.create(
        user=updated_by,
        action="MARKS_UPDATE",
        description=(
            f"Updated marks for "
            f"{enrollment.student.name} "
            f"({enrollment.course.course_name}) "
            f"from {previous_marks} to {new_marks}"
        ),
    )

    return history


@transaction.atomic
def create_feedback(
    enrollment,
    trainer,
    rating,
    comments,
    visible_to_student=True
):
    """
    Creates feedback for a specific enrollment.
    """

    # Trainer ownership check
    if (
        hasattr(trainer, "profile")
        and trainer.profile.role == "trainer"
    ):

        if enrollment.student.assigned_trainer != trainer:
            raise PermissionError(
                "You can give feedback only to your assigned students."
            )

    # Create feedback
    feedback = Feedback.objects.create(
        student=enrollment.student,
        trainer=trainer,
        enrollment=enrollment,
        rating=rating,
        comments=comments,
        visible_to_student=visible_to_student,
    )

    # Audit log
    AuditLog.objects.create(
        user=trainer,
        action="FEEDBACK",
        description=(
            f"Feedback added for "
            f"{enrollment.student.name} "
            f"({enrollment.course.course_name})"
        ),
    )

    return feedback