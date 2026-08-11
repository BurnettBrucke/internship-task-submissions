"""ORM challenges 13-22 from the Day 4 workbook, implemented as small,
independently testable functions. Surfaced to admins on the Reports page
(students/views.py:reports_view) and exercised directly in
students/tests.py so their correctness doesn't depend on the view.
"""
from datetime import timedelta

from django.db.models import Avg, Count, Q
from django.utils import timezone

from .models import AuditLog, Course, Feedback, MarksHistory, Student, UserProfile


def trainer_student_counts():
    """13. Count assigned students for each trainer."""
    return (
        UserProfile.objects.filter(role=UserProfile.ROLE_TRAINER)
        .annotate(student_count=Count('user__trainer_courses__students', distinct=True))
        .order_by('-student_count')
    )


def students_with_no_visible_feedback():
    """14. Find students with no visible feedback."""
    return Student.objects.exclude(
        feedbacks__is_visible_to_student=True
    ).distinct()


def trainers_without_feedback():
    """15. Find trainers who have not submitted feedback."""
    return UserProfile.objects.filter(role=UserProfile.ROLE_TRAINER).exclude(
        user__given_feedbacks__isnull=False
    ).distinct()


def latest_audit_actions(limit=5):
    """16. Get the five latest audit actions."""
    return AuditLog.objects.select_related('user').order_by('-timestamp')[:limit]


def users_with_excess_failed_logins(threshold=3):
    """17. Find users with more than `threshold` failed login attempts."""
    return (
        AuditLog.objects.filter(action_type=AuditLog.ACTION_LOGIN_FAILED)
        .values('username')
        .annotate(failure_count=Count('id'))
        .filter(failure_count__gt=threshold)
        .order_by('-failure_count')
    )


def marks_updated_this_week():
    """18. Find marks updated during the current week (Mon-Sun)."""
    today = timezone.localdate()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)
    return MarksHistory.objects.filter(
        updated_at__date__gte=start_of_week, updated_at__date__lt=end_of_week
    )


def average_rating_by_trainer():
    """19. Calculate average feedback rating by trainer."""
    return (
        UserProfile.objects.filter(role=UserProfile.ROLE_TRAINER)
        .annotate(average_rating=Avg('user__given_feedbacks__rating'))
        .order_by('-average_rating')
    )


def courses_below_average_marks(threshold=50):
    """20. Find courses with average marks below `threshold`."""
    return (
        Course.objects.annotate(avg_marks=Avg('students__marks'))
        .filter(avg_marks__lt=threshold, avg_marks__isnull=False)
        .order_by('avg_marks')
    )


def inactive_users_who_previously_logged_in():
    """21. Find inactive users who previously logged in."""
    from django.contrib.auth.models import User
    return User.objects.filter(is_active=False, last_login__isnull=False)


def enrolled_students_with_no_marks():
    """22. Find enrolled students with no marks.

    The Student.marks field is required (not nullable) in this schema, so
    "no marks recorded" is modeled as marks == 0 with no MarksHistory entry
    yet -- i.e. the default/never-graded state.
    """
    return Student.objects.filter(courses__isnull=False).filter(
        Q(marks=0) & Q(marks_history__isnull=True)
    ).distinct()
