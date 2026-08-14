from django.db import transaction

from .models import AuditLog, MarksHistory
from .utils import create_audit_log


@transaction.atomic
def update_student_marks(
    *,
    student,
    course,
    updated_by,
    new_marks,
    reason,
    request,
):
    """
    Update a student's marks and create the corresponding
    marks history and audit log.

    Keeping this operation in a service makes the business logic
    reusable from Django views and future API endpoints.
    """

    previous_marks = student.marks

    student.marks = new_marks
    student.save(
        update_fields=["marks"]
    )

    marks_history = MarksHistory.objects.create(
        student=student,
        course=course,
        previous_marks=previous_marks,
        new_marks=new_marks,
        updated_by=updated_by,
        reason=reason,
    )

    create_audit_log(
        user=updated_by,
        action=AuditLog.Action.MARKS_UPDATE,
        object_name="Marks",
        description=(
            f"Updated marks for {student.name} "
            f"in {course.course_name} "
            f"from {previous_marks} to {new_marks}."
        ),
        request=request,
    )

    return marks_history