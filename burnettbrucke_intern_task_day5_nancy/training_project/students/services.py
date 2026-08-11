"""Service layer: business logic that doesn't belong inside a view function.

Why pull this out of views.py?
- Views should stay focused on request-handling (auth, parsing input, picking
  a template/response) -- not on deciding *how* a marks change gets recorded.
- These functions take plain Python/model arguments, not an HttpRequest, so
  they're trivially reusable from anywhere else that needs the same
  behaviour later -- a management command, a Celery task, or (per the Day 5
  API-prep task) a future DRF/FastAPI endpoint that needs to "update marks"
  without going through a Django view or template at all.
- They're easier to unit-test in isolation, without needing a test client
  or a rendered response.

Each function below raises `django.core.exceptions.ValidationError` or
`PermissionDenied` on bad input/ownership violations, rather than returning
magic values -- callers (views today, an API view tomorrow) translate that
into whatever response shape makes sense for their layer.
"""
from django.core.exceptions import PermissionDenied, ValidationError

from .models import AuditLog, Feedback, MarksHistory, Student, log_action


def trainer_teaches_student(trainer_user, student):
    """True if `trainer_user` teaches at least one course `student` takes."""
    return student.courses.filter(trainer=trainer_user).exists()


def update_student_marks(*, student, trainer_user, new_marks, reason, request=None):
    """Apply a marks change for `student`, made by `trainer_user`.

    Encapsulates the three things that must always happen together:
    1. Ownership check (trainer must actually teach this student)
    2. The marks bounds check (0-100)
    3. Writing a MarksHistory row + an AuditLog entry alongside the save

    Returns the updated Student. Raises PermissionDenied / ValidationError
    on failure; never silently drops the history/audit step.
    """
    if not trainer_teaches_student(trainer_user, student):
        raise PermissionDenied("You may only update marks for your own students.")

    if new_marks is None or new_marks < 0 or new_marks > 100:
        raise ValidationError("Marks must be between 0 and 100.")

    if not reason or not reason.strip():
        raise ValidationError("A reason is required for every marks change.")

    old_marks = Student.objects.get(pk=student.pk).marks
    course = student.courses.filter(trainer=trainer_user).first()

    student.marks = new_marks
    student.save(update_fields=["marks"])

    MarksHistory.objects.create(
        student=student, course=course, old_marks=old_marks, new_marks=new_marks,
        updated_by=trainer_user, reason=reason.strip(),
    )
    log_action(
        trainer_user,
        f"Updated marks for '{student.name}': {old_marks} -> {new_marks} ({reason.strip()}).",
        action_type=AuditLog.ACTION_MARKS_UPDATE,
        object_repr=f"Student: {student.name}",
        request=request,
    )
    return student


def create_feedback(*, student, trainer_user, course, rating, comment, is_visible_to_student=True, request=None):
    """Create a Feedback row after checking ownership and rating bounds."""
    if not trainer_teaches_student(trainer_user, student):
        raise PermissionDenied("You may only leave feedback for your own students.")

    if course.trainer_id != trainer_user.id:
        raise PermissionDenied("You may only leave feedback on courses you teach.")

    if rating is None or rating < 1 or rating > 5:
        raise ValidationError("Rating must be between 1 and 5.")

    feedback = Feedback.objects.create(
        student=student, course=course, trainer=trainer_user,
        rating=rating, comment=comment, is_visible_to_student=is_visible_to_student,
    )
    log_action(
        trainer_user, f"Left feedback for '{student.name}' on {course.code}.",
        action_type=AuditLog.ACTION_FEEDBACK, object_repr=f"Student: {student.name}", request=request,
    )
    return feedback


def visible_feedback_for(student, viewer_role, viewer_user=None):
    """Return the Feedback queryset a given role is allowed to see for
    `student` -- centralizes the visibility rule used in several views/
    dashboards so it can't drift between them."""
    from .models import UserProfile  # local import avoids a circular import at module load time

    feedback = student.feedbacks.select_related('course', 'trainer')
    if viewer_role == UserProfile.ROLE_STUDENT:
        return feedback.filter(is_visible_to_student=True)
    if viewer_role == UserProfile.ROLE_TRAINER and viewer_user is not None:
        return feedback.filter(course__trainer=viewer_user)
    return feedback  # admin: everything, including drafts


def dashboard_totals():
    """Shared aggregate numbers used by the admin dashboard and the
    dashboard-totals tests -- pulled out so both use exactly one code path
    (previously this logic lived only inline in the view)."""
    from django.db.models import Avg, Max

    from .models import Course, Department

    students = Student.objects.all()
    stats = students.aggregate(average_marks=Avg('marks'), highest_marks=Max('marks'))
    return {
        "total_students": students.count(),
        "active_students": students.filter(is_active=True).count(),
        "total_departments": Department.objects.count(),
        "total_courses": Course.objects.count(),
        "average_marks": stats["average_marks"],
        "highest_marks": stats["highest_marks"],
        "top_student": students.order_by('-marks').first(),
    }
