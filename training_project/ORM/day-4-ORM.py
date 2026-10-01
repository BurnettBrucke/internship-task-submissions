# ============================================================
# DAY 4 - DJANGO ORM QUERIES
# Queries 13 - 22
# ============================================================

# ------------------------------------------------------------
# Django setup
# ------------------------------------------------------------

import os
import sys
import django


# Add the training_project directory to Python path
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)


# Tell Django which settings file to use
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "training_project.settings"
)


# Initialize Django
django.setup()


# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.utils import timezone

from students.models import (
    UserProfile,
    Student,
    Course,
    Enrollment,
    TrainerCourse,
    MarkHistory,
    Feedback,
    AuditLog,
)


# ============================================================
# 13. Count assigned students for each trainer
# ============================================================

query_13 = (
    User.objects
    .filter(
        profile__role=UserProfile.Role.TRAINER
    )
    .annotate(
        assigned_students=Count(
            "trainer_courses__course__enrollments__student",
            distinct=True
        )
    )
    .values(
        "username",
        "email",
        "assigned_students"
    )
)

print("\n13. Assigned students for each trainer:")
print(list(query_13))


# ============================================================
# 14. Find students with no visible feedback
# ============================================================

query_14 = (
    Student.objects
    .filter(
        Q(feedback__isnull=True) |
        ~Q(feedback__visible=True)
    )
    .distinct()
)

print("\n14. Students with no visible feedback:")

for student in query_14:
    print(
        student.name,
        "-",
        student.email
    )


# ============================================================
# 15. Find trainers who have not submitted feedback
# ============================================================

query_15 = (
    User.objects
    .filter(
        profile__role=UserProfile.Role.TRAINER
    )
    .filter(
        given_feedback__isnull=True
    )
    .distinct()
)

print("\n15. Trainers who have not submitted feedback:")

for trainer in query_15:
    print(
        trainer.username,
        "-",
        trainer.email
    )


# ============================================================
# 16. Get the five latest audit actions
# ============================================================

query_16 = (
    AuditLog.objects
    .select_related("user")
    .order_by("-timestamp")[:5]
)

print("\n16. Five latest audit actions:")

for log in query_16:

    username = (
        log.user.username
        if log.user
        else "System"
    )

    print(
        log.timestamp,
        "-",
        username,
        "-",
        log.get_action_display(),
        "-",
        log.description
    )


# ============================================================
# 17. Find users with more than three failed login attempts
# ============================================================

query_17 = (
    UserProfile.objects
    .filter(
        failed_login_attempts__gt=3
    )
    .select_related("user")
)

print("\n17. Users with more than three failed login attempts:")

for profile in query_17:

    print(
        profile.user.username,
        "-",
        profile.user.email,
        "- Attempts:",
        profile.failed_login_attempts
    )


# ============================================================
# 18. Find marks updated during the current week
# ============================================================

now = timezone.now()


# Monday = first day of the week
start_of_week = (
    now - timedelta(
        days=now.weekday()
    )
).replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0
)


# Beginning of next week
start_of_next_week = (
    start_of_week +
    timedelta(days=7)
)


query_18 = (
    MarkHistory.objects
    .filter(
        updated_at__gte=start_of_week,
        updated_at__lt=start_of_next_week
    )
    .select_related(
        "enrollment",
        "enrollment__student",
        "enrollment__course",
        "updated_by"
    )
    .order_by("-updated_at")
)

print("\n18. Marks updated during the current week:")

for history in query_18:

    print(
        history.enrollment.student.name,
        "-",
        history.enrollment.course.course_name,
        "-",
        history.previous_marks,
        "->",
        history.new_marks,
        "-",
        history.updated_at
    )


# ============================================================
# 19. Calculate average feedback rating by trainer
# ============================================================

query_19 = (
    User.objects
    .filter(
        profile__role=UserProfile.Role.TRAINER
    )
    .annotate(
        average_rating=Avg(
            "given_feedback__rating"
        )
    )
    .values(
        "username",
        "email",
        "average_rating"
    )
)

print("\n19. Average feedback rating by trainer:")

for trainer in query_19:

    print(
        trainer["username"],
        "-",
        trainer["average_rating"]
    )


# ============================================================
# 20. Find courses with average marks below 50
# ============================================================

query_20 = (
    Course.objects
    .annotate(
        average_marks=Avg(
            "enrollments__marks",
            filter=Q(
                enrollments__marks__isnull=False
            )
        )
    )
    .filter(
        average_marks__lt=50
    )
    .values(
        "course_name",
        "code",
        "average_marks"
    )
)

print("\n20. Courses with average marks below 50:")

for course in query_20:

    print(
        course["course_name"],
        "-",
        course["code"],
        "- Average:",
        course["average_marks"]
    )


# ============================================================
# 21. Find inactive users who previously logged in
# ============================================================

query_21 = (
    User.objects
    .filter(
        is_active=False,
        audit_logs__action=AuditLog.Action.LOGIN
    )
    .distinct()
    .values(
        "username",
        "email"
    )
)

print("\n21. Inactive users who previously logged in:")

for user in query_21:

    print(
        user["username"],
        "-",
        user["email"]
    )


# ============================================================
# 22. Find enrolled students with no marks
# ============================================================

query_22 = (
    Enrollment.objects
    .filter(
        marks__isnull=True
    )
    .select_related(
        "student",
        "course"
    )
    .values(
        "student__name",
        "student__email",
        "course__course_name",
        "course__code"
    )
)

print("\n22. Enrolled students with no marks:")

for enrollment in query_22:

    print(
        enrollment["student__name"],
        "-",
        enrollment["student__email"],
        "-",
        enrollment["course__course_name"],
        "-",
        enrollment["course__code"]
    )


# ============================================================
# END
# ============================================================

print("\nAll ORM queries 13-22 executed successfully.")