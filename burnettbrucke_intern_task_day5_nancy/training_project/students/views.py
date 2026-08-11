from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from . import reports, services
from .decorators import get_role, role_required
from .forms import (
    FeedbackForm,
    RegisterForm,
    StudentForm,
    TrainerMarksForm,
    TrainerRegisterForm,
    UserProfileForm,
)
from .models import (
    AuditLog,
    Course,
    Department,
    Feedback,
    MarksHistory,
    Student,
    UserProfile,
    log_action,
)

PAGE_SIZE = 10


def home(request):
    company = "Bug Network Private Limited"
    return render(request, "home.html", {"company": company})


def about(request):
    return HttpResponse("<h1>About Page</h1><p>This is About Page.</p>")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def register_view(request):
    """Public sign-up. Always creates a Student-role account (see
    RegisterForm docstring) -- there is no role field on this form, so a
    visitor cannot grant themselves Administrator/Trainer access."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            log_action(
                user, f"User '{user.username}' registered as a student.",
                action_type=AuditLog.ACTION_CREATE, object_repr=f"User: {user.username}", request=request,
            )
            messages.success(request, "Account created. Welcome!")
            return redirect("post_login_redirect")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form, "role_label": "Student"})


def trainer_register_view(request):
    """Separate sign-up path for trainers. The account is created
    immediately (so the person can see the 'pending approval' message and
    isn't left wondering whether anything happened) but is locked out of
    the trainer dashboard and all trainer actions until an Administrator
    approves it."""
    if request.method == "POST":
        form = TrainerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            log_action(
                user, f"User '{user.username}' registered as a trainer (pending approval).",
                action_type=AuditLog.ACTION_CREATE, object_repr=f"User: {user.username}", request=request,
            )
            messages.info(request, "Account created. A trainer account must be approved by an administrator before you can access the trainer dashboard.")
            return redirect("post_login_redirect")
    else:
        form = TrainerRegisterForm()
    return render(request, "registration/register.html", {"form": form, "role_label": "Trainer"})


@login_required
def post_login_redirect(request):
    """LOGIN_REDIRECT_URL points here. Sends each user to the dashboard
    that matches their role, so nobody has to remember/guess a URL."""
    role = get_role(request.user)
    if role == UserProfile.ROLE_ADMIN:
        return redirect("admin_dashboard")
    if role == UserProfile.ROLE_TRAINER:
        return redirect("trainer_dashboard")
    return redirect("student_dashboard")


# ---------------------------------------------------------------------------
# Dashboards (Bootstrap cards / tables / badges / progress bars live in the
# templates; this view layer only decides *who* may see *what data*.)
# ---------------------------------------------------------------------------

@role_required(UserProfile.ROLE_ADMIN)
def admin_dashboard(request):
    totals = services.dashboard_totals()
    recent_students = Student.objects.order_by('-joined_date', '-id')[:5]
    recent_users = UserProfile.objects.select_related('user').order_by('-user__date_joined')[:5]
    recent_logs = AuditLog.objects.select_related('user')[:8]
    pending_trainers = UserProfile.objects.filter(role=UserProfile.ROLE_TRAINER, is_approved=False)

    context = {
        **totals,
        "total_trainers": UserProfile.objects.filter(role=UserProfile.ROLE_TRAINER).count(),
        "recent_students": recent_students,
        "recent_users": recent_users,
        "recent_logs": recent_logs,
        "pending_trainers": pending_trainers,
    }
    return render(request, "dashboards/admin_dashboard.html", context)


@role_required(UserProfile.ROLE_TRAINER)
def trainer_dashboard(request):
    if request.user.profile.is_pending_approval:
        return render(request, "dashboards/pending_approval.html", status=200)

    # .annotate(Count(...)) below computes each course's student count in
    # the same single query that fetches the courses, instead of the
    # template calling `course.students.count` once per row in a loop
    # (previously N+1: 1 query for the courses + 1 more per course).
    courses = Course.objects.filter(trainer=request.user).annotate(student_count=Count('students'))
    student_ids = Student.objects.filter(courses__in=courses).values_list('id', flat=True).distinct()
    students = Student.objects.filter(id__in=student_ids)
    recent_feedback = Feedback.objects.filter(trainer=request.user).select_related('student', 'course')[:5]

    context = {
        "courses": courses,
        "total_courses": courses.count(),
        "total_students": students.count(),
        "average_marks": students.aggregate(avg=Avg('marks'))['avg'],
        "students": students,
        "recent_feedback": recent_feedback,
    }
    return render(request, "dashboards/trainer_dashboard.html", context)


@role_required(UserProfile.ROLE_STUDENT)
def student_dashboard(request):
    student = Student.objects.filter(user=request.user).select_related('department').prefetch_related(
        'courses'
    ).first()
    feedbacks = []
    if student:
        feedbacks = Feedback.objects.filter(
            student=student, is_visible_to_student=True
        ).select_related('course', 'trainer')

    context = {
        "student": student,
        "feedbacks": feedbacks,
        "profile_completion": request.user.profile.completion_percentage,
    }
    return render(request, "dashboards/student_dashboard.html", context)


# ---------------------------------------------------------------------------
# Student CRUD -- Administrators manage everything; Trainers get read access
# plus marks/feedback for their own courses; Students may only view their
# own record (ownership is enforced here, not just hidden in the template).
# ---------------------------------------------------------------------------

@role_required(UserProfile.ROLE_ADMIN, UserProfile.ROLE_TRAINER)
def student_list(request):
    students = (
        Student.objects.select_related('department')
        .prefetch_related('courses')
        .all()
    )

    role = get_role(request.user)
    if role == UserProfile.ROLE_TRAINER:
        if request.user.profile.is_pending_approval:
            raise PermissionDenied("Your trainer account is pending administrator approval.")
        # Ownership filter: a trainer only ever sees students enrolled in
        # a course they teach -- changing ?department= or similar in the
        # URL cannot surface anyone else's students.
        students = students.filter(courses__trainer=request.user).distinct()

    # --- filtering ---
    department_id = request.GET.get('department', '')
    course_id = request.GET.get('course', '')
    status = request.GET.get('status', '')
    result = request.GET.get('result', '')
    query = request.GET.get('q', '').strip()

    if department_id:
        students = students.filter(department_id=department_id)
    if course_id:
        students = students.filter(courses__id=course_id)
    if status == 'active':
        students = students.filter(is_active=True)
    elif status == 'inactive':
        students = students.filter(is_active=False)
    if result == 'pass':
        students = students.filter(marks__gte=40)
    elif result == 'fail':
        students = students.filter(marks__lt=40)
    if query:
        students = students.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(courses__name__icontains=query)
        )

    students = students.distinct()

    paginator = Paginator(students, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get('page'))

    courses_qs = Course.objects.all()
    if role == UserProfile.ROLE_TRAINER:
        courses_qs = courses_qs.filter(trainer=request.user)

    context = {
        "students": page_obj,
        "page_obj": page_obj,
        "total_students": students.count(),
        "active_students": students.filter(is_active=True).count(),
        "departments": Department.objects.all(),
        "courses": courses_qs,
        "selected_department": department_id,
        "selected_course": course_id,
        "selected_status": status,
        "selected_result": result,
        "query": query,
        "role": role,
    }
    return render(request, "students/student_list.html", context)


def _can_view_student(request, student):
    role = get_role(request.user)
    if role == UserProfile.ROLE_ADMIN:
        return True
    if role == UserProfile.ROLE_TRAINER:
        if request.user.profile.is_pending_approval:
            return False
        return student.courses.filter(trainer=request.user).exists()
    if role == UserProfile.ROLE_STUDENT:
        return student.user_id == request.user.id
    return False


@login_required
def student_detail(request, pk):
    student = get_object_or_404(
        Student.objects.select_related('department', 'profile', 'user').prefetch_related('courses'),
        pk=pk,
    )

    # Ownership check performed here in the view -- not just by hiding a
    # link -- so visiting /students/<other-id>/ directly is blocked too.
    if not _can_view_student(request, student):
        raise PermissionDenied("You do not have permission to view this student record.")

    role = get_role(request.user)
    feedbacks = services.visible_feedback_for(student, viewer_role=role, viewer_user=request.user)

    latest_marks_update = student.marks_history.select_related('updated_by').first()

    context = {
        "student": student,
        "feedbacks": feedbacks,
        "role": role,
        "can_edit": role == UserProfile.ROLE_ADMIN,
        "can_update_marks": role == UserProfile.ROLE_TRAINER
        and not request.user.profile.is_pending_approval
        and student.courses.filter(trainer=request.user).exists(),
        "latest_marks_update": latest_marks_update,
    }
    return render(request, "students/student_detail.html", context)


@role_required(UserProfile.ROLE_ADMIN)
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            log_action(
                request.user, f"Added student '{student.name}'.",
                action_type=AuditLog.ACTION_CREATE, object_repr=f"Student: {student.name}", request=request,
            )
            messages.success(request, "Student added successfully!")
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form": form, "mode": "add"})


@role_required(UserProfile.ROLE_ADMIN)
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            log_action(
                request.user, f"Edited student '{student.name}'.",
                action_type=AuditLog.ACTION_UPDATE, object_repr=f"Student: {student.name}", request=request,
            )
            messages.success(request, "Student updated successfully!")
            return redirect("student_detail", pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(
        request, "students/student_form.html", {"form": form, "mode": "edit", "student": student}
    )


@role_required(UserProfile.ROLE_TRAINER)
def update_marks(request, pk):
    """Narrow edit surface for trainers: marks + a mandatory reason, and
    only for students enrolled in a course the trainer actually teaches.
    Students are blocked from ever reaching this view at all -- the
    role_required decorator rejects non-trainer roles (including a direct
    POST) before this line even runs."""
    if request.user.profile.is_pending_approval:
        raise PermissionDenied("Your trainer account is pending administrator approval.")

    student = get_object_or_404(Student, pk=pk)
    if not student.courses.filter(trainer=request.user).exists():
        raise PermissionDenied("You may only update marks for your own students.")

    if request.method == "POST":
        form = TrainerMarksForm(request.POST, instance=student)
        if form.is_valid():
            services.update_student_marks(
                student=student,
                trainer_user=request.user,
                new_marks=form.cleaned_data['marks'],
                reason=form.cleaned_data['reason'],
                request=request,
            )
            messages.success(request, "Marks updated.")
            return redirect("student_detail", pk=student.pk)
    else:
        form = TrainerMarksForm(instance=student)
    return render(request, "students/student_form.html", {"form": form, "mode": "marks", "student": student})


@role_required(UserProfile.ROLE_TRAINER)
def add_feedback(request, pk):
    if request.user.profile.is_pending_approval:
        raise PermissionDenied("Your trainer account is pending administrator approval.")

    student = get_object_or_404(Student, pk=pk)
    if not student.courses.filter(trainer=request.user).exists():
        raise PermissionDenied("You may only leave feedback for your own students.")

    if request.method == "POST":
        form = FeedbackForm(request.POST, trainer=request.user, student=student)
        if form.is_valid():
            services.create_feedback(
                student=student,
                trainer_user=request.user,
                course=form.cleaned_data['course'],
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment'],
                is_visible_to_student=form.cleaned_data['is_visible_to_student'],
                request=request,
            )
            messages.success(request, "Feedback saved.")
            return redirect("student_detail", pk=student.pk)
    else:
        form = FeedbackForm(trainer=request.user, student=student)
    return render(
        request, "students/student_form.html", {"form": form, "mode": "feedback", "student": student}
    )


@role_required(UserProfile.ROLE_TRAINER)
def edit_feedback(request, pk):
    """A trainer may edit only feedback they personally authored."""
    feedback = get_object_or_404(Feedback, pk=pk)
    if feedback.trainer_id != request.user.id:
        raise PermissionDenied("You may only edit your own feedback.")

    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=feedback, trainer=request.user, student=feedback.student)
        if form.is_valid():
            form.save()
            log_action(
                request.user, f"Edited feedback for '{feedback.student.name}' on {feedback.course.code}.",
                action_type=AuditLog.ACTION_FEEDBACK, object_repr=f"Student: {feedback.student.name}", request=request,
            )
            messages.success(request, "Feedback updated.")
            return redirect("student_detail", pk=feedback.student.pk)
    else:
        form = FeedbackForm(instance=feedback, trainer=request.user, student=feedback.student)
    return render(
        request, "students/student_form.html",
        {"form": form, "mode": "edit_feedback", "student": feedback.student},
    )


@role_required(UserProfile.ROLE_ADMIN)
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        name = student.name
        student.delete()
        log_action(
            request.user, f"Deleted student '{name}'.",
            action_type=AuditLog.ACTION_DELETE, object_repr=f"Student: {name}", request=request,
        )
        messages.success(request, f"Deleted student '{name}'.")
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html", {"student": student})


# ---------------------------------------------------------------------------
# Administrator: user management (activation, trainer approval)
# ---------------------------------------------------------------------------

@role_required(UserProfile.ROLE_ADMIN)
def manage_users(request):
    profiles = UserProfile.objects.select_related('user').order_by('user__username')

    role_filter = request.GET.get('role', '')
    if role_filter:
        profiles = profiles.filter(role=role_filter)

    paginator = Paginator(profiles, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        "page_obj": page_obj,
        "profiles": page_obj,
        "role_filter": role_filter,
    }
    return render(request, "students/manage_users.html", context)


@role_required(UserProfile.ROLE_ADMIN)
def toggle_user_active(request, pk):
    """Administrator-controlled account activation/deactivation. Deactivated
    users cannot log in (Django's own auth backend checks is_active)."""
    target_user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        if target_user.pk == request.user.pk:
            messages.error(request, "You cannot deactivate your own account.")
        else:
            target_user.is_active = not target_user.is_active
            target_user.save(update_fields=["is_active"])
            state = "activated" if target_user.is_active else "deactivated"
            log_action(
                request.user, f"{state.capitalize()} account '{target_user.username}'.",
                action_type=AuditLog.ACCOUNT_STATUS, object_repr=f"User: {target_user.username}", request=request,
            )
            messages.success(request, f"'{target_user.username}' was {state}.")
    return redirect("manage_users")


@role_required(UserProfile.ROLE_ADMIN)
def approve_trainer(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk, role=UserProfile.ROLE_TRAINER)
    if request.method == "POST":
        profile.is_approved = True
        profile.save(update_fields=["is_approved"])
        log_action(
            request.user, f"Approved trainer account '{profile.user.username}'.",
            action_type=AuditLog.ACCOUNT_STATUS, object_repr=f"User: {profile.user.username}", request=request,
        )
        messages.success(request, f"Trainer '{profile.user.username}' approved.")
    return redirect("manage_users")


# ---------------------------------------------------------------------------
# Administrator: audit log
# ---------------------------------------------------------------------------

@role_required(UserProfile.ROLE_ADMIN)
def audit_log_view(request):
    logs = AuditLog.objects.select_related('user').all()

    action_type = request.GET.get('action_type', '')
    username = request.GET.get('username', '').strip()
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if action_type:
        logs = logs.filter(action_type=action_type)
    if username:
        logs = logs.filter(username__icontains=username)
    if date_from:
        logs = logs.filter(timestamp__date__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__date__lte=date_to)

    paginator = Paginator(logs, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        "page_obj": page_obj,
        "logs": page_obj,
        "action_choices": AuditLog.ACTION_CHOICES,
        "selected_action_type": action_type,
        "username_query": username,
        "date_from": date_from,
        "date_to": date_to,
    }
    return render(request, "students/audit_log.html", context)


# ---------------------------------------------------------------------------
# Administrator: reports (ORM challenges 13-22)
# ---------------------------------------------------------------------------

@role_required(UserProfile.ROLE_ADMIN)
def reports_view(request):
    context = {
        "trainer_student_counts": reports.trainer_student_counts(),
        "students_with_no_visible_feedback": reports.students_with_no_visible_feedback(),
        "trainers_without_feedback": reports.trainers_without_feedback(),
        "latest_audit_actions": reports.latest_audit_actions(),
        "users_with_excess_failed_logins": reports.users_with_excess_failed_logins(),
        "marks_updated_this_week": reports.marks_updated_this_week(),
        "average_rating_by_trainer": reports.average_rating_by_trainer(),
        "courses_below_average_marks": reports.courses_below_average_marks(),
        "inactive_users_who_previously_logged_in": reports.inactive_users_who_previously_logged_in(),
        "enrolled_students_with_no_marks": reports.enrolled_students_with_no_marks(),
    }
    return render(request, "students/reports.html", context)


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def permission_denied_view(request, exception=None):
    """Custom 403 handler (wired up via handler403 in urls.py) so
    unauthorized access always renders a friendly, on-brand page instead of
    Django's default error page."""
    return render(request, "403.html", status=403)
