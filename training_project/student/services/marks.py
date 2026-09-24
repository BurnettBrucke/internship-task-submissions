from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from ..models import Course, CourseMark, MarksHistory, student
from .audit import create_audit_log



def get_course_for_trainer(course_id, user):
    """
    Get a course only if it belongs to the logged-in trainer.

    This keeps course ownership validation in the service layer so
    future API endpoints can reuse the same security rule.
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


def get_course_mark(course, assigned_student, user):
    """
    Get or create the CourseMark for a course and student.

    This logic can be reused by HTML views or future API endpoints.
    """

    course_mark, created = CourseMark.objects.get_or_create(
        course=course,
        student=assigned_student,
        defaults={
            "marks": assigned_student.marks,
            "updated_by": user,
        },
    )

    return course_mark


def get_assigned_student(course, student_id):
    """
    Get a student only when the student is enrolled in the course.

    This prevents marks operations on students who are not assigned
    to the selected course.
    """

    return get_object_or_404(
        course.students,
        pk=student_id
    )



def update_course_marks(
    user,
    request,
    course,
    assigned_student,
    form,
):
    """
    Update course marks and create the corresponding history record.

    The transaction ensures that the marks update and history record
    are treated as one database operation.

    Keeping this logic in a service allows the same operation to be
    reused later by an API without duplicating business rules.
    """

    course_mark, created = CourseMark.objects.get_or_create(
        course=course,
        student=assigned_student,
        defaults={
            "marks": assigned_student.marks,
            "updated_by": user,
        },
    )

    old_marks = course_mark.marks
    new_marks = form.cleaned_data["marks"]
    reason = form.cleaned_data.get("reason", "")

    with transaction.atomic():

        course_mark.marks = new_marks
        course_mark.updated_by = user
        course_mark.save()

        MarksHistory.objects.create(
            course_mark=course_mark,
            old_marks=old_marks,
            new_marks=new_marks,
            reason=reason,
            updated_by=user,
        )
        create_audit_log(
            request=None,
            user=user,
            action_type="UPDATE",
            description=(
                f"Updated marks for "
                f"{assigned_student.name} in "
                f"{course.course_name}: "
                f"{old_marks} -> {new_marks}. "
                f"Reason: {reason}"
            ),
            affected_object=course_mark,
        )

    return course_mark


def get_marks_history(course, assigned_student):

    """
    Get the marks and history for a specific course and student.

    The service only retrieves records associated with the supplied
    course and student.
    """

    course_mark = CourseMark.objects.filter(
        course=course,
        student=assigned_student
    ).first()

    if course_mark:
        history = (
            MarksHistory.objects
            .filter(course_mark=course_mark)
            .select_related("updated_by")
        )
    else:
        history = MarksHistory.objects.none()

    return course_mark, history


def get_marks_history_for_user(user, course_id, student_id):
    """
    Get marks history after checking whether the logged-in user
    is allowed to view the selected student's marks.

    Keeping authorization and database logic here allows the same
    rules to be reused later by an API.
    """

    user_role = user.userprofile.role

    course = Course.objects.get(
        pk=course_id
    )

    assigned_student = course.students.get(
        pk=student_id
    )

    # Student can only view their own marks.
    if user_role == "student":

        if assigned_student.user_id != user.id:
            raise PermissionDenied(
                "You are not authorized to view these marks."
            )

    # Trainer can only view marks for their assigned course.
    elif user_role == "trainer":

        if course.trainer_id != user.id:
            raise PermissionDenied(
                "You are not assigned to this course."
            )

    # Only admin, assigned trainer and owning student are allowed.
    elif user_role != "admin":

        raise PermissionDenied(
            "You are not authorized to view marks history."
        )

    course_mark = CourseMark.objects.filter(
        course=course,
        student=assigned_student
    ).first()

    if course_mark:

        history = (
            MarksHistory.objects
            .filter(course_mark=course_mark)
            .select_related("updated_by")
        )

    else:

        history = MarksHistory.objects.none()

    return (
        course,
        assigned_student,
        course_mark,
        history,
    )