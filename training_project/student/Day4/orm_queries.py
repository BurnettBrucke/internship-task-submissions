from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from django.utils import timezone

from .models import ( # type: ignore
    UserProfile,
    student,
    Course,
    Feedback,
    AuditLog,
    CourseMark,
    MarksHistory,
    LoginAttempt,
)


# Count assigned students for each trainer.
def count_assigned_students_for_each_trainer():
    return User.objects.filter(
        userprofile__role="trainer"
    ).annotate(
        assigned_students=Count(
            "training_courses__students",
            distinct=True
        )
    )


# Find students with no visible feedback
def students_with_no_visible_feedback():
    return student.objects.exclude(
        feedback__is_visible=True
    ).distinct()


# Find trainers who have not submitted feedback.
def trainers_who_have_not_submitted_feedback():
    return User.objects.filter(
        userprofile__role="trainer"
    ).exclude(
        feedback_given__isnull=False
    ).distinct()


# Give five latest audit actions
def five_latest_audit_actions():
    return AuditLog.objects.order_by(
        "-created_at"
    )[:5]


# Find user with more than three failed login attempt
users = User.objects.filter(
    loginattempt__failed_attempts__gt=3
)

# Find the marks updated suring the current week
today = timezone.now()
start_of_week = today - timedelta(days=today.weekday())

marks = MarksHistory.objects.filter( 
    updated_at__gte=start_of_week
)

# Calculate average feedback rating by trainer
from django.db.models import Avg

trainer_ratings = Feedback.objects.values(
    "trainer"
).annotate(
    average_rating=Avg("rating")
)


# Find courses with average marks below 50
courses = Course.objects.annotate(
    average_marks=Avg("students__marks")
).filter(
    average_marks__lt=50
)


# Find inactive users who previously logged in

users = User.objects.filter(
    is_active=False,
    last_login__isnull=False
)

# Find enrolled students with no marks
students = student.objects.filter(
    active=True,
    marks__isnull=True
)