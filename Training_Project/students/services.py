from django.core.exceptions import PermissionDenied
from django.db.models import Avg

from .models import (
    Course,
    CourseMark,
    Department,
    Feedback,
    MarksHistory,
    Student,
)
from django.contrib.auth.models import User


def update_student_marks(
    *,
    student,
    course,
    trainer,
    new_marks,
    reason,
):
    """
    Create or update a student's marks for a course.

    This keeps marks-related business logic outside the view so the
    same logic can later be reused by APIs or other workflows.
    """

    # Trainer must be assigned to this course
    if not course.trainer.filter(id=trainer.id).exists():
        raise PermissionDenied

    # Student must be enrolled in this course
    if not student.courses.filter(id=course.id).exists():
        raise PermissionDenied

    # Get existing marks record
    course_mark = CourseMark.objects.filter(
        student=student,
        course=course
    ).first()

    # Keep previous marks for history
    previous_marks = (
        course_mark.marks if course_mark else 0
    )

    # Create or update CourseMark
    if course_mark:
        course_mark.marks = new_marks
        course_mark.updated_by = trainer
        course_mark.save()
    else:
        course_mark = CourseMark.objects.create(
            student=student,
            course=course,
            marks=new_marks,
            updated_by=trainer
        )

    # Store marks history
    MarksHistory.objects.create(
        student=student,
        course=course,
        previous_marks=previous_marks,
        new_marks=new_marks,
        updated_by=trainer,
        reason=reason
    )

    return course_mark, previous_marks

def create_student_feedback(*, student, course, trainer, feedback_data, request):
    if not course.trainer.filter(id=trainer.id).exists():
        raise PermissionDenied

    if not student.courses.filter(id=course.id).exists():
        raise PermissionDenied

    feedback = Feedback.objects.create(
        student=student,
        trainer=trainer,
        course=course,
        **feedback_data
    )

    return feedback

def get_admin_dashboard_data():
    total_students = Student.objects.count()

    total_active_students = Student.objects.filter(
        active=True
    ).count()

    total_departments = Department.objects.count()
    total_courses = Course.objects.count()

    total_trainers = User.objects.filter(
        profile__role='trainer'
    ).count()

    average_marks = Student.objects.aggregate(
        average=Avg('marks')
    )['average']

    highest_student = Student.objects.order_by(
        '-marks'
    ).first()

    recent_students = Student.objects.order_by(
        '-joined_date'
    )[:5]

    return {
        'total_students': total_students,
        'total_active_students': total_active_students,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'total_trainers': total_trainers,
        'average_marks': average_marks,
        'highest_student': highest_student,
        'recent_students': recent_students,
    }