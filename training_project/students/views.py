from datetime import timedelta
from .services import update_student_marks

from .permissions import trainer_can_access_student_course
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import role_required
from .forms import (
    AuditLogFilterForm,
    LoginForm,
    MarksUpdateForm,
    RegisterForm,
    StudentForm,
)
from .forms_feedback import FeedbackForm
from .models import (
    AuditLog,
    Course,
    Department,
    Feedback,
    MarksHistory,
    Student,
    TrainerAssignment,
    UserProfile,
)
from .utils import create_audit_log


def home(request):
    context = {
        "company": "Bug Network Private Limited Training Program"
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "about.html")


@login_required
@role_required(UserProfile.UserRole.ADMIN)
def admin_dashboard(request):

    context = {
        "total_students": Student.objects.count(),

        "total_departments": Department.objects.count(),

        "total_courses": Course.objects.count(),

        "active_students": Student.objects.filter(
            is_active=True
        ).count(),

        "total_users": User.objects.count(),

        "recent_students": Student.objects.order_by(
            "-joined_date"
        )[:5],

        "recent_users": User.objects.order_by(
            "-date_joined"
        )[:5],
    }

    return render(
        request,
        "dashboards/admin_dashboard.html",
        context,
    )


@login_required
@role_required(UserProfile.UserRole.TRAINER)
def trainer_dashboard(request):

    assignments = TrainerAssignment.objects.filter(
        trainer=request.user
    ).select_related(
        "student",
        "course",
    )

    assigned_students = assignments.values(
        "student"
    ).distinct().count()

    assigned_courses = assignments.values(
        "course"
    ).distinct().count()

    context = {
        "assigned_students": assigned_students,
        "assigned_courses": assigned_courses,
        "assignments": assignments,
    }

    return render(
        request,
        "dashboards/trainer_dashboard.html",
        context,
    )


@login_required
@role_required(UserProfile.UserRole.STUDENT)
def student_dashboard(request):

    student = (
        Student.objects
        .select_related(
            "department",
            "user",
        )
        .prefetch_related(
            "courses",
        )
        .filter(
            user=request.user
        )
        .first()
    )

    profile_completion = 0

    if student:

        if student.department:
            profile_completion += 25

        if student.courses.exists():
            profile_completion += 25

        if student.email:
            profile_completion += 25

        if student.user:
            profile_completion += 25

    context = {
        "student": student,
        "profile_completion": profile_completion,
    }

    return render(
        request,
        "dashboards/student_dashboard.html",
        context,
    )


@login_required
@role_required(UserProfile.UserRole.TRAINER)
def add_feedback(request, student_id):

    student = get_object_or_404(
        Student,
        pk=student_id
    )

    # Check if trainer is assigned to this student
    assignment = TrainerAssignment.objects.filter(
        trainer=request.user,
        student=student
    ).first()

    if not assignment:

        return HttpResponseForbidden(
            "You are not assigned to this student."
        )

    if request.method == "POST":

        form = FeedbackForm(request.POST)

        if form.is_valid():

            feedback = form.save(commit=False)

            feedback.trainer = request.user

            feedback.student = student

            feedback.course = assignment.course

            feedback.save()

            create_audit_log(
                user=request.user,
                action=AuditLog.Action.FEEDBACK,
                object_name="Feedback",
                description=f"Added feedback for {student.name}.",
                request=request,
            )

            messages.success(
                request,
                "Feedback added successfully."
            )

            return redirect(
                "trainer_dashboard"
            )

    else:

        form = FeedbackForm(
            initial={
                "course": assignment.course
            }
        )

    return render(
        request,
        "feedback/add_feedback.html",
        {
            "form": form,
            "student": student,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Feedback", "url": "student_feedback"},
                {"label": "Add Feedback"},
            ],
        },
    )


@login_required
@role_required(UserProfile.UserRole.TRAINER)
def edit_feedback(request, feedback_id):

    feedback = get_object_or_404(
        Feedback,
        pk=feedback_id
    )

    # Trainer can edit only their own feedback
    if feedback.trainer != request.user:

        return HttpResponseForbidden(
            "You can only edit your own feedback."
        )

    if request.method == "POST":

        form = FeedbackForm(
            request.POST,
            instance=feedback
        )

        if form.is_valid():

            form.save()

            create_audit_log(
                user=request.user,
                action=AuditLog.Action.UPDATE,
                object_name="Feedback",
                description=(
                    f"Updated feedback for "
                    f"{feedback.student.name}."
                ),
                request=request,
            )

            messages.success(
                request,
                "Feedback updated successfully."
            )

            return redirect(
                "trainer_dashboard"
            )

    else:

        form = FeedbackForm(
            instance=feedback
        )

    return render(
        request,
        "feedback/edit_feedback.html",
        {
            "form": form,
            "feedback": feedback,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Feedback", "url": "student_feedback"},
                {"label": "Edit Feedback"},
            ],
        },
    )


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            profile = user.profile

            profile.role = UserProfile.UserRole.STUDENT
            profile.is_approved = True

            profile.save()

            messages.success(
                request,
                "Registration successful. Please login."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )


def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        cache_key = f"failed_login_{username}"

        failed_attempts = cache.get(cache_key, 0)

        # Block login after 5 failed attempts
        if failed_attempts >= 5:

            messages.error(
                request,
                "Your account is temporarily locked due to too many failed login attempts. Please try again later."
            )

            return redirect("login")

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            profile = user.profile

            # Trainer Approval Check
            if (
                profile.role == UserProfile.UserRole.TRAINER
                and not profile.is_approved
            ):

                messages.error(
                    request,
                    "Your trainer account is awaiting administrator approval."
                )

                return redirect("login")

            # Reset failed login attempts after successful login
            cache.delete(cache_key)

            login(request, user)

            # Audit Log - Successful Login
            create_audit_log(
                user=user,
                action=AuditLog.Action.LOGIN,
                object_name="User",
                description="User logged in.",
                request=request,
            )

            messages.success(
                request,
                f"Welcome {user.username}!"
            )

            if profile.role == UserProfile.UserRole.ADMIN:
                return redirect("admin_dashboard")

            elif profile.role == UserProfile.UserRole.TRAINER:
                return redirect("trainer_dashboard")

            return redirect("student_dashboard")

        else:

            # Increase failed login attempts
            failed_attempts += 1

            # Store for 5 minutes
            cache.set(
                cache_key,
                failed_attempts,
                timeout=300
            )

            # Audit Log - Failed Login
            user = User.objects.filter(
                username=username
            ).first()

            if user:

                create_audit_log(
                    user=user,
                    action=AuditLog.Action.FAILED_LOGIN,
                    object_name="User",
                    description="Failed login attempt.",
                    request=request,
                )

            remaining = 5 - failed_attempts

            if remaining > 0:

                messages.error(
                    request,
                    f"Invalid username or password. {remaining} attempt(s) remaining."
                )

            else:

                messages.error(
                    request,
                    "Too many failed login attempts. Your account has been temporarily locked for 5 minutes."
                )

    else:

        form = LoginForm()

    return render(
        request,
        "registration/login.html",
        {
            "form": form
        }
    )


@login_required
def user_logout(request):

    create_audit_log(
        user=request.user,
        action=AuditLog.Action.LOGOUT,
        object_name="User",
        description="User logged out.",
        request=request,
    )

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")


@login_required
@role_required(UserProfile.UserRole.ADMIN)
def student_list(request):

    students = Student.objects.select_related(
        "department"
    ).prefetch_related(
        "courses"
    )

    # Search
    search = request.GET.get("search")

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(courses__course_name__icontains=search)
        ).distinct()

    # Department Filter
    department = request.GET.get("department")

    if department:
        students = students.filter(
            department_id=department
        )

    # Course Filter
    course = request.GET.get("course")

    if course:
        students = students.filter(
            courses__id=course
        )

    # Active Filter
    active = request.GET.get("active")

    if active == "yes":
        students = students.filter(
            is_active=True
        )

    elif active == "no":
        students = students.filter(
            is_active=False
        )

    # Pass / Fail Filter
    result = request.GET.get("result")

    if result == "pass":
        students = students.filter(
            marks__gte=40
        )

    elif result == "fail":
        students = students.filter(
            marks__lt=40
        )

    # Pagination
    paginator = Paginator(students, 5)

    page_number = request.GET.get("page")

    students = paginator.get_page(page_number)

    context = {
        "students": students,
        "departments": Department.objects.all(),
        "courses": Course.objects.all(),

        "total_students": Student.objects.count(),
        "active_students": Student.objects.filter(
            is_active=True
        ).count(),
        "total_departments": Department.objects.count(),
        "total_courses": Course.objects.count(),

        "average_marks": Student.objects.aggregate(
            Avg("marks")
        )["marks__avg"],

        "highest_student": Student.objects.order_by(
            "-marks"
        ).first(),

        "recent_students": Student.objects.order_by(
            "-joined_date"
        )[:5],

        # Breadcrumbs
        "breadcrumbs": [
            {"label": "Home", "url": "home"},
            {"label": "Students"},
        ],
    }

    return render(
        request,
        "students/student_list.html",
        context,
    )


@login_required
def student_detail(request, pk):

    # Administrator can view every student
    if request.user.profile.role == UserProfile.UserRole.ADMIN:

        student = get_object_or_404(
            Student,
            pk=pk
        )

    # Student can view only their own profile
    elif request.user.profile.role == UserProfile.UserRole.STUDENT:

        student = get_object_or_404(
            Student,
            pk=pk,
            user=request.user
        )

    # Trainer is not allowed in Task 1
    else:
        raise PermissionDenied

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Students", "url": "student_list"},
                {"label": "Student Details"},
            ],
        }
    )

@login_required
@role_required(UserProfile.UserRole.ADMIN)
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()

            create_audit_log(
                user=request.user,
                action=AuditLog.Action.CREATE,
                object_name=f"Student: {student.name}",
                description=(
                    f"Student '{student.name}' was created."
                ),
                request=request,
            )

            messages.success(
                request,
                "Student added successfully."
            )

            return redirect("student_list")

    else:

        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "title": "Add Student",
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Students", "url": "student_list"},
                {"label": "Add Student"},
            ],
        },
    )


@login_required
@role_required(UserProfile.UserRole.ADMIN)
def edit_student(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            student = form.save()

            create_audit_log(
                user=request.user,
                action=AuditLog.Action.UPDATE,
                object_name=f"Student: {student.name}",
                description=(
                    f"Student '{student.name}' was updated."
                ),
                request=request,
            )

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect(
                "student_detail",
                pk=student.pk
            )

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "student": student,
            "title": "Edit Student",
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Students", "url": "student_list"},
                {"label": "Edit Student"},
            ],
        },
    )

@login_required
@role_required(UserProfile.UserRole.ADMIN)
def delete_student(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        student_name = student.name

        create_audit_log(
            user=request.user,
            action=AuditLog.Action.DELETE,
            object_name=f"Student: {student_name}",
            description=(
                f"Student '{student_name}' was deleted."
            ),
            request=request,
        )

        student.delete()

        messages.success(
            request,
            "Student deleted successfully."
        )

        return redirect(
            "student_list"
        )

    return render(
        request,
        "students/student_confirm_delete.html",
        {
            "student": student,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Students", "url": "student_list"},
                {"label": "Delete Student"},
            ],
        },
    )

@login_required
@role_required(UserProfile.UserRole.STUDENT)
def student_feedback(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    feedback_list = Feedback.objects.filter(
        student=student,
        is_visible=True
    ).select_related(
        "trainer",
        "course"
    )

    return render(
        request,
        "feedback/student_feedback.html",
        {
            "feedback_list": feedback_list,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Feedback"},
            ],
        },
    )


@login_required
@role_required(UserProfile.UserRole.ADMIN)
def admin_feedback(request):

    feedback_list = Feedback.objects.all().select_related(
        "trainer",
        "student",
        "course",
    )

    return render(
        request,
        "feedback/admin_feedback.html",
        {
            "feedback_list": feedback_list,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Feedback"},
                {"label": "All Feedback"},
            ],
        },
    )


@login_required
@role_required(UserProfile.UserRole.TRAINER)
def update_marks(request, student_id, course_id):

    # Get the student
    student = get_object_or_404(
        Student,
        pk=student_id
    )

    # Get the course
    course = get_object_or_404(
        Course,
        pk=course_id
    )

    # Make sure this trainer is assigned to this student
    # for this particular course.
    trainer_can_access_student_course(
        trainer=request.user,
        student=student,
        course=course,
    )

    if request.method == "POST":

        form = MarksUpdateForm(request.POST)

        if form.is_valid():

            new_marks = form.cleaned_data["new_marks"]
            reason = form.cleaned_data["reason"]

            update_student_marks(
                student=student,
                course=course,
                updated_by=request.user,
                new_marks=new_marks,
                reason=reason,
                request=request,
            )

            messages.success(
                request,
                "Marks updated successfully."
            )

            return redirect(
                "trainer_dashboard"
            )

    else:

        form = MarksUpdateForm(
            initial={
                "new_marks": student.marks,
            }
        )

    return render(
        request,
        "marks/update_marks.html",
        {
            "form": form,
            "student": student,
            "course": course,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Marks"},
                {"label": "Update Marks"},
            ],
        },
    )


@login_required
def marks_history(request, student_id, course_id):

    student = get_object_or_404(
        Student,
        pk=student_id
    )

    course = get_object_or_404(
        Course,
        pk=course_id
    )

    # Only assigned trainers can view marks history
    if request.user.profile.role == UserProfile.UserRole.TRAINER:

        assignment_exists = TrainerAssignment.objects.filter(
            trainer=request.user,
            student=student,
            course=course,
        ).exists()

        if not assignment_exists:

            return HttpResponseForbidden(
                "You are not assigned to this student for this course."
            )

    elif request.user.profile.role == UserProfile.UserRole.STUDENT:

        # Student can only view their own marks history
        if student.user != request.user:

            return HttpResponseForbidden(
                "You can only view your own marks history."
            )

    elif request.user.profile.role != UserProfile.UserRole.ADMIN:

        return HttpResponseForbidden(
            "You are not authorized to view marks history."
        )

    history = MarksHistory.objects.filter(
        student=student,
        course=course,
    ).select_related(
        "updated_by",
    )

    return render(
        request,
        "marks/marks_history.html",
        {
            "student": student,
            "course": course,
            "history": history,
             "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Marks"},
                {"label": "Marks History"},
            ],
        },
    )


@login_required
@role_required(UserProfile.UserRole.ADMIN)
def audit_log_list(request):

    logs = AuditLog.objects.select_related(
        "user"
    ).order_by(
        "-timestamp"
    )

    form = AuditLogFilterForm(request.GET or None)

    if form.is_valid():

        search = form.cleaned_data.get("search")
        action = form.cleaned_data.get("action")
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")

        if search:

            logs = logs.filter(
                Q(user__username__icontains=search)
                | Q(object_name__icontains=search)
                | Q(description__icontains=search)
            )

        if action:

            logs = logs.filter(
                action=action
            )

        if start_date:

            logs = logs.filter(
                timestamp__date__gte=start_date
            )

        if end_date:

            logs = logs.filter(
                timestamp__date__lte=end_date
            )

    paginator = Paginator(
        logs,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "audit/audit_log_list.html",
        {
            "form": form,
            "page_obj": page_obj,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "Audit Logs"},
            ],
        },
    )


@login_required
@role_required(UserProfile.UserRole.ADMIN)
def orm_challenges(request):

    # ---------------------------------------------------------
    # 13. Count assigned students for each trainer
    # ---------------------------------------------------------

    trainer_student_counts = (
        TrainerAssignment.objects
        .values(
            "trainer__username"
        )
        .annotate(
            student_count=Count(
                "student",
                distinct=True
            )
        )
        .order_by(
            "trainer__username"
        )
    )


    # ---------------------------------------------------------
    # 14. Find students with no visible feedback
    # ---------------------------------------------------------

    students_without_visible_feedback = (
        Student.objects
        .exclude(
            feedback_received__is_visible=True
        )
        .distinct()
    )


    # ---------------------------------------------------------
    # 15. Find trainers who have not submitted feedback
    # ---------------------------------------------------------

    trainers_without_feedback = (
        UserProfile.objects
        .filter(
            role=UserProfile.UserRole.TRAINER
        )
        .exclude(
            user__feedback_given__isnull=False
        )
        .select_related(
            "user"
        )
    )


    # ---------------------------------------------------------
    # 16. Get the five latest audit actions
    # ---------------------------------------------------------

    latest_audit_actions = (
        AuditLog.objects
        .select_related(
            "user"
        )
        .order_by(
            "-timestamp"
        )[:5]
    )


    # ---------------------------------------------------------
    # 17. Find users with more than three failed login attempts
    # ---------------------------------------------------------

    users_with_failed_logins = (
        AuditLog.objects
        .filter(
            action=AuditLog.Action.FAILED_LOGIN
        )
        .values(
            "user",
            "user__username"
        )
        .annotate(
            failed_attempts=Count("id")
        )
        .filter(
            failed_attempts__gt=3
        )
        .order_by(
            "-failed_attempts"
        )
    )


    # ---------------------------------------------------------
    # 18. Find marks updated during the current week
    # ---------------------------------------------------------

    today = timezone.localdate()

    start_of_week = today - timedelta(
        days=today.weekday()
    )

    marks_updated_this_week = (
        MarksHistory.objects
        .filter(
            updated_at__date__gte=start_of_week
        )
        .select_related(
            "student",
            "course",
            "updated_by"
        )
        .order_by(
            "-updated_at"
        )
    )


    # ---------------------------------------------------------
    # 19. Calculate average feedback rating by trainer
    # ---------------------------------------------------------

    average_feedback_by_trainer = (
        Feedback.objects
        .values(
            "trainer__username"
        )
        .annotate(
            average_rating=Avg(
                "rating"
            )
        )
        .order_by(
            "-average_rating"
        )
    )


    # ---------------------------------------------------------
    # 20. Find courses with average marks below 50
    # ---------------------------------------------------------

    courses_below_average = (
        Course.objects
        .annotate(
            average_marks=Avg(
                "students__marks"
            )
        )
        .filter(
            average_marks__lt=50
        )
        .order_by(
            "average_marks"
        )
    )


    # ---------------------------------------------------------
    # 21. Find inactive users who previously logged in
    # ---------------------------------------------------------

    inactive_users_previously_logged_in = (
        User.objects
        .filter(
            is_active=False,
            last_login__isnull=False
        )
        .order_by(
            "-last_login"
        )
    )


    # ---------------------------------------------------------
    # 22. Find enrolled students with no marks
    # ---------------------------------------------------------

    enrolled_students_without_marks = (
        Student.objects
        .filter(
            courses__isnull=False
        )
        .filter(
            marks__isnull=True
        )
        .distinct()
    )


    context = {
        "trainer_student_counts": trainer_student_counts,
        "students_without_visible_feedback": (
            students_without_visible_feedback
        ),
        "trainers_without_feedback": (
            trainers_without_feedback
        ),
        "latest_audit_actions": latest_audit_actions,
        "users_with_failed_logins": (
            users_with_failed_logins
        ),
        "marks_updated_this_week": (
            marks_updated_this_week
        ),
        "average_feedback_by_trainer": (
            average_feedback_by_trainer
        ),
        "courses_below_average": (
            courses_below_average
        ),
        "inactive_users_previously_logged_in": (
            inactive_users_previously_logged_in
        ),
        "enrolled_students_without_marks": (
            enrolled_students_without_marks
        ),
        
        "breadcrumbs": [
            {"label": "Home", "url": "home"},
            {"label": "ORM Challenges"},
        ],
    }

    return render(
        request,
        "orm/orm_challenges.html",
        context,
    )


@login_required
@role_required(UserProfile.UserRole.ADMIN)
def user_management(request):

    users = User.objects.all().order_by(
        "-date_joined"
    )

    return render(
        request,
        "users/user_management.html",
        {
            "users": users,
            "breadcrumbs": [
                {"label": "Home", "url": "home"},
                {"label": "User Management"},
            ],
        },
    )


@login_required
@role_required(UserProfile.UserRole.ADMIN)
def toggle_user_status(request, user_id):

    if request.method != "POST":
        return HttpResponseForbidden(
            "Only POST requests are allowed."
        )

    user = get_object_or_404(
        User,
        pk=user_id,
    )

    # Prevent an administrator from deactivating their own account.
    if user == request.user:
        messages.error(
            request,
            "You cannot change your own account status."
        )
        return redirect("user_management")

    previous_status = user.is_active

    user.is_active = not user.is_active

    user.save(
        update_fields=["is_active"]
    )

    new_status = user.is_active

    create_audit_log(
        user=request.user,
        action=AuditLog.Action.STATUS_CHANGE,
        object_name="User Account",
        description=(
            f"Changed account status for "
            f"{user.username} from "
            f"{'Active' if previous_status else 'Inactive'} "
            f"to "
            f"{'Active' if new_status else 'Inactive'}."
        ),
        request=request,
    )

    messages.success(
        request,
        (
            f"{user.username} account has been "
            f"{'activated' if new_status else 'deactivated'}."
        ),
    )

    return redirect("user_management")