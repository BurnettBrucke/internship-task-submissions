from django.db import transaction

from ..models import (
    Enrollment,
    MarkHistory,
    TrainerCourse,
)


def trainer_can_update_marks(trainer, enrollment):
    """
    Check whether the trainer is approved and assigned
    to the enrollment's course.
    """

    profile = getattr(trainer, "profile", None)

    if profile is None:
        return False

    if profile.role != profile.Role.TRAINER:
        return False

    if profile.status != profile.Status.APPROVED:
        return False

    return TrainerCourse.objects.filter(
        trainer=trainer,
        course=enrollment.course,
    ).exists()


@transaction.atomic
def update_enrollment_marks(
    enrollment,
    new_marks,
    reason,
    updated_by,
):
    """
    Update enrollment marks and create a permanent mark-history record.

    Keeping this operation in a service means the same business
    operation can later be reused by:
    - Django views
    - REST API endpoints
    - management commands
    - background tasks
    """

    previous_marks = enrollment.marks

    enrollment.marks = new_marks

    enrollment.save(
        update_fields=["marks"]
    )

    history = MarkHistory.objects.create(
        enrollment=enrollment,
        previous_marks=previous_marks,
        new_marks=new_marks,
        updated_by=updated_by,
        reason=reason,
    )

    return enrollment, history


def get_student_marks(student):
    """
    Return all enrollments containing the student's marks.
    """

    return (
        Enrollment.objects
        .filter(student=student)
        .select_related("course")
        .prefetch_related("mark_history__updated_by")
    )


def calculate_average_marks(student):
    """
    Calculate the student's average marks.

    Returns None when the student has no marks.
    """

    from django.db.models import Avg

    return (
        Enrollment.objects
        .filter(
            student=student,
            marks__isnull=False,
        )
        .aggregate(
            average=Avg("marks")
        )["average"]
    )