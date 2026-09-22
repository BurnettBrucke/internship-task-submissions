from django.db.models import Avg, Count

from ..models import (
    Student,
    Course,
    Enrollment,
    Feedback,
    MarkHistory,
    User,
    UserProfile,
)


def get_admin_dashboard_data():
    """
    Build the data required by the admin dashboard.

    The view should only call this service and pass the returned
    context to the template.

    This separation also makes the same dashboard calculations
    reusable by a future API endpoint.
    """

    students = (
        Student.objects
        .select_related("department")
        .prefetch_related("enrollments__course")
        .annotate(
            course_count=Count(
                "enrollments__course",
                distinct=True,
            )
        )
        .order_by("name")
    )

    trainers = (
        User.objects
        .filter(
            profile__role=UserProfile.Role.TRAINER
        )
        .select_related(
            "profile",
            "profile__requested_course",
        )
    )

    courses = Course.objects.all()

    total_students = students.count()
    total_trainers = trainers.count()
    total_courses = courses.count()

    pending_trainers = trainers.filter(
        profile__status=UserProfile.Status.PENDING
    ).count()

    active_courses = courses.filter(
        active_status=True
    ).count()

    users = (
        User.objects
        .filter(
            profile__isnull=False,
            is_superuser=False,
        )
        .select_related("profile")
        .order_by("-date_joined")
    )

    return {
        "students": students,
        "trainers": trainers,
        "courses": courses,
        "total_students": total_students,
        "total_trainers": total_trainers,
        "total_courses": total_courses,
        "active_courses": active_courses,
        "pending_trainers": pending_trainers,
        "users": users,
    }


def get_trainer_dashboard_data(trainer):
    """
    Build dashboard data for a trainer.
    """

    assigned_courses = (
        Course.objects
        .filter(
            trainer_assignments__trainer=trainer,
            active_status=True,
        )
        .distinct()
        .order_by("course_name")
    )

    assigned_enrollments = (
        Enrollment.objects
        .filter(
            course__in=assigned_courses,
            student__active=True,
        )
        .select_related(
            "student",
            "course",
        )
        .order_by("student__name")
    )

    total_courses = assigned_courses.count()

    total_students = (
        Student.objects
        .filter(
            enrollments__course__in=assigned_courses,
            active=True,
        )
        .distinct()
        .count()
    )

    feedback_given = (
        Feedback.objects
        .filter(trainer=trainer)
        .select_related(
            "student",
            "course",
        )
        .order_by("-created_at")
    )

    return {
        "assigned_courses": assigned_courses,
        "assigned_enrollments": assigned_enrollments,
        "total_courses": total_courses,
        "total_students": total_students,
        "feedback_given": feedback_given,
    }


def get_student_dashboard_data(student):
    """
    Build dashboard data for a student.
    """

    enrollments = (
        Enrollment.objects
        .filter(student=student)
        .select_related("course")
        .prefetch_related("mark_history__updated_by")
    )

    total_courses = enrollments.count()

    average_marks = (
        enrollments
        .filter(marks__isnull=False)
        .aggregate(
            average=Avg("marks")
        )["average"]
    )

    feedback = (
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

    return {
        "student": student,
        "enrollments": enrollments,
        "total_courses": total_courses,
        "average_marks": average_marks,
        "feedback": feedback,
    }


def get_trainer_detail_data(trainer):
    """
    Build the detailed trainer-management data used by the admin.
    """

    assigned_courses = (
        Course.objects
        .filter(
            trainer_assignments__trainer=trainer
        )
        .distinct()
        .order_by("course_name")
    )

    assigned_enrollments = (
        Enrollment.objects
        .filter(
            course__trainer_assignments__trainer=trainer
        )
        .select_related(
            "student",
            "course",
        )
        .distinct()
        .order_by(
            "student__name",
            "course__course_name",
        )
    )

    assigned_students = (
        Student.objects
        .filter(
            enrollments__course__trainer_assignments__trainer=trainer
        )
        .distinct()
        .order_by("name")
    )

    feedback_given = (
        Feedback.objects
        .filter(trainer=trainer)
        .select_related(
            "student",
            "course",
        )
        .order_by("-created_at")
    )

    marks_history = (
        MarkHistory.objects
        .filter(updated_by=trainer)
        .select_related(
            "enrollment__student",
            "enrollment__course",
        )
        .order_by("-updated_at")
    )

    available_courses = (
        Course.objects
        .filter(active_status=True)
        .exclude(
            trainer_assignments__trainer=trainer
        )
        .distinct()
        .order_by("course_name")
    )

    total_courses = assigned_courses.count()
    total_students = assigned_students.count()
    total_feedback = feedback_given.count()
    total_marks_updates = marks_history.count()

    average_rating = feedback_given.aggregate(
        average=Avg("rating")
    )["average"]

    return {
        "trainer": trainer,
        "profile": trainer.profile,

        "assigned_courses": assigned_courses,
        "assigned_enrollments": assigned_enrollments,
        "assigned_students": assigned_students,

        "feedback_given": feedback_given,
        "marks_history": marks_history,

        "total_courses": total_courses,
        "total_students": total_students,
        "total_feedback": total_feedback,
        "total_marks_updates": total_marks_updates,

        "average_rating": average_rating,
        "available_courses": available_courses,
    }