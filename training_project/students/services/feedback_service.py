from django.db import transaction

from ..models import (
    Feedback,
    Enrollment,
    TrainerCourse,
)


def trainer_can_manage_feedback(trainer, enrollment):
    """
    Check whether a trainer is allowed to create feedback
    for the selected enrollment.
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
def create_feedback(
    enrollment,
    trainer,
    rating,
    comment,
    visible=True,
):
    """
    Create feedback for a student/course enrollment.

    The trainer, student and course are derived from the
    enrollment instead of being trusted from request data.
    """

    feedback = Feedback.objects.create(
        student=enrollment.student,
        course=enrollment.course,
        trainer=trainer,
        rating=rating,
        comment=comment,
        visible=visible,
    )

    return feedback


@transaction.atomic
def update_feedback(
    feedback,
    rating,
    comment,
    visible=None,
):
    """
    Update existing feedback.
    """

    feedback.rating = rating
    feedback.comment = comment

    if visible is not None:
        feedback.visible = visible

    feedback.save()

    return feedback


def trainer_owns_feedback(feedback, trainer):
    """
    Check whether the supplied trainer owns the feedback.
    """

    return feedback.trainer_id == trainer.id


def get_student_feedback(student):
    """
    Return visible feedback for a student.
    """

    return (
        Feedback.objects
        .filter(
            student=student,
            visible=True,
        )
        .select_related(
            "course",
            "trainer",
        )
        .order_by("-created_at")
    )


def get_trainer_feedback(trainer):
    """
    Return feedback created by a trainer.
    """

    return (
        Feedback.objects
        .filter(trainer=trainer)
        .select_related(
            "student",
            "course",
        )
        .order_by("-created_at")
    )