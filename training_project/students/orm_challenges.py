from django.db import models
from django.db.models import Count, Avg
from django.utils import timezone
from django.db.models.functions import TruncDate
from .models import (TrainerProfile, Student, AuditLog, UserProfile, MarksUpdateHistory,Feedback,Course)
from django.contrib.auth.models import User

# 13. Trainer student count
def trainer_student_count():
    trainers = TrainerProfile.objects.annotate(
        student_count=Count('courses__students', distinct=True)
    )

    for trainer in trainers:
        print(
            trainer.user.username,
            "→",
            trainer.student_count,
            "students"
        )

# 14. No visible feedback
def students_with_no_visible_feedback():
    students = Student.objects.annotate(
        visible_feedback_count=Count(
            'feedbacks',
            filter=models.Q(feedbacks__is_visible=True)
        )
    ).filter(
        visible_feedback_count=0
    )

    for student in students:
        print(student.name)

# 15. Trainers without feedback
def trainers_without_feedback():
    trainers = TrainerProfile.objects.filter(
        user__given_feedbacks__isnull=True
    )

    for trainer in trainers:
        print(trainer.user.username)

# 16. Latest 5 audit actions 
def latest_five_audit_actions():
    logs = AuditLog.objects.order_by('-created_at')[:5]

    for log in logs:
        print(
            log.created_at,
            "→",
            log.user,
            "→",
            log.action,
            "→",
            log.description
        )

# 17. Failed attempts > 3
def users_with_more_than_three_failed_attempts():
    profiles = UserProfile.objects.filter(
        failed_login_attempts__gt=3
    )

    for profile in profiles:
        print(
            profile.user.username,
            "→",
            profile.failed_login_attempts,
            "failed attempts"
        )

# 18. Marks updated this week
def marks_updated_this_week():
    today = timezone.localdate()

    start_of_week = today - timezone.timedelta(days=today.weekday())

    histories = MarksUpdateHistory.objects.filter(
        updated_at__date__gte=start_of_week
    ).order_by('-updated_at')

    for history in histories:
        print(
            history.updated_at,
            "→",
            history.student.name,
            "→",
            history.previous_marks,
            "to",
            history.new_marks
        )
# 19. Average feedback rating by trainer
def average_feedback_rating_by_trainer():
    trainers = Feedback.objects.filter(
        rating__isnull=False
    ).values(
        'trainer__username'
    ).annotate(
        average_rating=Avg('rating')
    ).order_by(
        'trainer__username'
    )

    for trainer in trainers:
        print(
            trainer['trainer__username'],
            "→",
            trainer['average_rating']
        )

# 20. Courses with average marks below 50   
def courses_with_average_marks_below_50():
    courses = Course.objects.annotate(
        average_marks=Avg('students__marks')
    ).filter(
        average_marks__lt=50
    )

    for course in courses:
        print(
            course.course_name,
            "→",
            course.average_marks
        )

# 21. Inactive users who previously logged in   
def inactive_users_who_previously_logged_in():
    users = User.objects.filter(
        is_active=False,
        last_login__isnull=False
    )

    for user in users:
        print(
            user.username,
            "→ Last login:",
            user.last_login
        )

# 22. Enrolled students with no marks
def enrolled_students_with_no_marks():
    students = Student.objects.filter(
        courses__isnull=False,
        marks=0
    ).distinct()

    for student in students:
        print(
            student.name,
            "→ No marks"
        )