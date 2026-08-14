from django.core.exceptions import PermissionDenied

from .models import TrainerAssignment


def trainer_can_access_student_course(
    trainer,
    student,
    course,
):
    """
    Check whether a trainer is assigned to a student
    for the specified course.

    Returns True when the assignment exists.
    Raises PermissionDenied otherwise.
    """

    assignment_exists = TrainerAssignment.objects.filter(
        trainer=trainer,
        student=student,
        course=course,
    ).exists()

    if not assignment_exists:
        raise PermissionDenied(
            "You are not assigned to this student for this course."
        )

    return True