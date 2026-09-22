from ..models import (
    Enrollment,
    UserProfile,
    TrainerCourse,
)


def get_user_profile(user):
    """
    Return the UserProfile associated with a user.
    """

    return getattr(user, "profile", None)


def is_admin(user):
    """
    Check whether the user has the admin role.
    """

    profile = get_user_profile(user)

    return (
        profile is not None
        and profile.role == UserProfile.Role.ADMIN
    )


def is_trainer(user):
    """
    Check whether the user has the trainer role.
    """

    profile = get_user_profile(user)

    return (
        profile is not None
        and profile.role == UserProfile.Role.TRAINER
    )


def is_student(user):
    """
    Check whether the user has the student role.
    """

    profile = get_user_profile(user)

    return (
        profile is not None
        and profile.role == UserProfile.Role.STUDENT
    )


def is_approved_trainer(user):
    """
    Check whether the user is an approved trainer.
    """

    profile = get_user_profile(user)

    return (
        profile is not None
        and profile.role == UserProfile.Role.TRAINER
        and profile.status == UserProfile.Status.APPROVED
    )


def trainer_assigned_to_course(trainer, course):
    """
    Check whether a trainer is assigned to a course.
    """

    return TrainerCourse.objects.filter(
        trainer=trainer,
        course=course,
    ).exists()


def trainer_can_access_enrollment(trainer, enrollment):
    """
    Check whether an approved trainer is assigned to
    the enrollment's course.
    """

    if not is_approved_trainer(trainer):
        return False

    return trainer_assigned_to_course(
        trainer,
        enrollment.course,
    )


def student_owns_record(user, student):
    """
    Check whether a student account belongs to the
    requested student record.
    """

    return (
        is_student(user)
        and student.user_id == user.id
    )