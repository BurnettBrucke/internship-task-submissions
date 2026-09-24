
from django.contrib.auth.models import User

from student.models import (
    student,
    UserProfile,
    Course,
    CourseMark,
    Feedback,
)


# ============================================================
# Admin Dashboard
# ============================================================

def get_admin_dashboard_data():

    total_users = User.objects.count()

    total_students = student.objects.count()

    total_trainers = UserProfile.objects.filter(
        role__iexact="trainer"
    ).count()

    courses = Course.objects.all()

    total_courses = courses.count()

    recent_users = User.objects.order_by("-date_joined")[:5]

    recent_students = student.objects.order_by("-id")[:5]

    pending_trainers = UserProfile.objects.filter(
        role="trainer",
        is_approved=False
    )

    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_trainers": total_trainers,
        "total_courses": total_courses,
        "recent_users": recent_users,
        "recent_students": recent_students,
        "courses": courses,
        "pending_trainers": pending_trainers,
    }


# ============================================================
# Trainer Dashboard
# ============================================================

def get_trainer_dashboard_data(trainer):

    courses = (
        Course.objects
        .filter(trainer=trainer)
        .prefetch_related("students")
    )

    assigned_students = (
        student.objects
        .filter(courses__trainer=trainer)
        .distinct()
    )

    return {
        "courses": courses,
        "assigned_students": assigned_students,
        "assigned_courses_count": courses.count(),
        "assigned_students_count": assigned_students.count(),
    }


# ============================================================
# Student Dashboard
# ============================================================

def get_student_dashboard_data(student_obj):

    marks = student_obj.marks

    if marks is None:
        marks = 0

    profile_completion = 100

    if not student_obj.email:
        profile_completion -= 20

    if not student_obj.age:
        profile_completion -= 20

    course_marks = (
        CourseMark.objects
        .filter(student=student_obj)
        .select_related(
            "course",
            "updated_by",
        )
    )

    feedback = (
        Feedback.objects
        .filter(
            student=student_obj,
            is_visible=True,
        )
        .select_related(
            "course",
            "trainer",
        )
    )

    return {
        "student": student_obj,
        "course_marks": course_marks,
        "feedback": feedback,
        "profile_completion": profile_completion,
        "marks": marks,
    }

