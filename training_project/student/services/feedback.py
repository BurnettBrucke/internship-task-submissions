
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from ..models import Feedback, Course, student


def get_course_for_feedback(course_id, user):
    """
    Get a course only if it belongs to the logged-in trainer.

    Keeping this permission check in the service layer allows
    the same rule to be reused later by an API.
    """

    course = get_object_or_404(
        Course,
        pk=course_id
    )

    if course.trainer_id != user.id:
        raise PermissionDenied(
            "You are not assigned to this course."
        )

    return course


def get_assigned_student_for_feedback(course, student_id):
    """
    Get a student only when the student is enrolled in the course.

    This prevents a trainer from creating feedback for a student
    who is not assigned to the selected course.
    """

    return get_object_or_404(
        course.students,
        pk=student_id
    )


def create_feedback(
    user,
    course,
    assigned_student,
    form,
):
    """
    Create feedback for a student in a course.

    The trainer is taken from the logged-in user instead of
    trusting trainer information from the form.
    """

    feedback = form.save(
        commit=False
    )

    feedback.course = course
    feedback.student = assigned_student
    feedback.trainer = user

    feedback.save()

    return feedback

# feedback_edit()
def get_feedback_for_edit(
    feedback_id,
    user,
):
    """
    Get feedback only if it belongs to the logged-in trainer.

    This prevents a trainer from editing another trainer's feedback.
    """

    feedback = get_object_or_404(
        Feedback,
        pk=feedback_id
    )

    if feedback.trainer_id != user.id:
        raise PermissionDenied(
            "You can only edit your own feedback."
        )

    return feedback


def update_feedback(
    feedback,
    form,
):
    """
    Update an existing feedback record.

    Permission checking is performed before this function is called.
    """

    return form.save(
        commit=True
    )


def get_feedback_for_user(user):
    """
    Get feedback that the logged-in user is authorized to see.

    Students can see only their own visible feedback.
    Trainers can see feedback created by themselves.
    Admins can see all feedback.
    """

    role = user.userprofile.role

    feedback_queryset = (
        Feedback.objects
        .select_related(
            "course",
            "student",
            "trainer",
        )
        .order_by("-created_at")
    )

    if role == "student":

        student_profile = get_object_or_404(
            student,
            user=user
        )

        feedback_queryset = feedback_queryset.filter(
            student=student_profile,
            is_visible=True
        )

    elif role == "trainer":

        feedback_queryset = feedback_queryset.filter(
            trainer=user
        )

    elif role == "admin":

        pass

    else:

        raise PermissionDenied(
            "You are not authorized to view feedback."
        )

    return feedback_queryset

