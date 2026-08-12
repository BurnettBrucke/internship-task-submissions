from django.db import transaction
from django.db.models import Avg

from .models import Student, Course, Department, Feedback, MarksHistory, AuditLog


def get_dashboard_statistics():
    """
    Returns common dashboard statistics.
    """

    average_marks = Student.objects.aggregate(
        Avg("marks")
    )["marks__avg"]

    highest_student = Student.objects.order_by(
        "-marks"
    ).first()

    recent_students = Student.objects.order_by(
        "-joined_date"
    )[:5]

    return {
        "total_students": Student.objects.count(),
        "total_active_students": Student.objects.filter(
            active=True
        ).count(),
        "total_departments": Department.objects.count(),
        "total_courses": Course.objects.count(),
        "average_marks": average_marks,
        "highest_student": highest_student,
        "recent_students": recent_students,
    }


@transaction.atomic
def update_student_marks(student, new_marks, updated_by, reason=""):
    """
    Updates student marks and creates marks history and audit log.
    """

    previous_marks = student.marks

    student.marks = new_marks
    student.save()

    history = MarksHistory.objects.create(
        student=student,
        previous_marks=previous_marks,
        new_marks=new_marks,
        updated_by=updated_by,
        reason=reason
    )

    AuditLog.objects.create(
        user=updated_by,
        action="MARKS_UPDATED",
        description=(
            f"Updated marks of {student.name} "
            f"from {previous_marks} to {new_marks}"
        )
    )

    return history


@transaction.atomic
def create_feedback(
    student,
    trainer,
    rating,
    comments,
    visible_to_student=True
):
    """
    Creates feedback for a student.
    """

    feedback = Feedback.objects.create(
        student=student,
        trainer=trainer,
        rating=rating,
        comments=comments,
        visible_to_student=visible_to_student
    )

    AuditLog.objects.create(
        user=trainer,
        action="FEEDBACK_CREATED",
        description=f"Feedback added for {student.name}"
    )

    return feedback