from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator

from .models import (
    Student, Department, Course, StudentProfile,
    UserProfile, AuditLog, Feedback, MarksHistory,
)
from .forms import (
    StudentForm, StudentRegistrationForm,
    StudentSelfEditForm, MarksUpdateForm, MarksWithReasonForm,
    DepartmentForm, CourseForm,
    TrainerRegistrationForm, FeedbackForm, AccountActivationForm,
    AdminTrainerAddForm, AdminTrainerEditForm,
)


# Helper functions

def _get_client_ip(request):
    """Extract the real client IP from the request headers."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _log_action(request, action_type, description, user=None):
    """
    Helper function to create an AuditLog entry.
    Avoids writing AuditLog.objects.create in multiple views.
    """
    AuditLog.objects.create(
        user        = user or (request.user if request.user.is_authenticated else None),
        action_type = action_type,
        description = description,
        ip_address  = _get_client_ip(request),
    )


def _is_admin(user):
    """Returns True if user has an admin UserProfile OR is Django staff."""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.is_admin
    except UserProfile.DoesNotExist:
        # Fallback for the superuser / legacy admin created before Day 4
        return user.is_staff and user.email.endswith('@admin.com')


def _is_trainer(user):
    """Returns True if user has a trainer UserProfile that is approved."""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.is_trainer and user.userprofile.is_approved
    except UserProfile.DoesNotExist:
        return False


def _dashboard_stats():
    """Shared stats dict used on both portals."""
    avg_result = Student.objects.aggregate(avg=Avg('marks'))
    return {
        'total_students' : Student.objects.count(),
        'active_students': Student.objects.filter(is_active=True).count(),
        'total_depts'    : Department.objects.count(),
        'total_courses'  : Course.objects.count(),
        'avg_marks'      : round(avg_result['avg'], 2) if avg_result['avg'] else 0,
        'top_student'    : Student.objects.order_by('-marks').first(),
        'recent_students': Student.objects.order_by('-joined_date')[:5],
    }


# Role decorators

def _admin_required(view_func):
    """Decorator: login required + must be admin."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not _is_admin(request.user):
            # Return 403 for unauthorized access
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1>"
                "<p>You do not have admin access. "
                '<a href="/">Go back to home</a></p>'
            )
        return view_func(request, *args, **kwargs)
    return wrapper


def _trainer_required(view_func):
    """Decorator: login required + must be an approved trainer."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not _is_trainer(request.user):
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1>"
                "<p>You must be an approved trainer to access this page. "
                '<a href="/">Go back to home</a></p>'
            )
        return view_func(request, *args, **kwargs)
    return wrapper


# Landing page

def landing(request):
    """
    Public landing page.
    Shows role-appropriate links if the user is already authenticated.
    """
    context = {
        'company': 'Bug Network Private Limited',
        **_dashboard_stats(),
    }
    return render(request, 'landing.html', context)


def about(request):
    """About page (/about/)."""
    return render(request, 'about.html')


# Authentication

# Failed-login tracking settings
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_KEY         = 'failed_login_{username}'  # session key template


def register_view(request):
    """
    Registers a new student user.
    Creates a Django User, a Student profile, and sets their role to student.
    """
    if request.user.is_authenticated:
        return redirect('student_portal')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            _log_action(request, 'CREATE',
                        f"New student account registered: {user.username}")
            messages.success(request, "🎉 Registration successful! Please log in.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'student_register.html', {'form': form})


def register_trainer_view(request):
    """
    Registers a new trainer user.
    Creates a User and UserProfile with role='trainer' (pending admin approval).
    """
    if request.user.is_authenticated:
        return redirect('landing')

    if request.method == 'POST':
        form = TrainerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            _log_action(request, 'CREATE',
                        f"New trainer account registered (pending approval): {user.username}")
            messages.success(
                request,
                "✅ Trainer registration submitted! "
                "An admin will approve your account before you can log in."
            )
            return redirect('login')
    else:
        form = TrainerRegistrationForm()

    return render(request, 'trainer_register.html', {'form': form})


def login_view(request):
    """
    Unified login view for students, trainers, and admins.
    Redirects users to their respective dashboards based on their role.
    Includes session-based lockout after 5 failed login attempts.
    """
    if request.user.is_authenticated:
        return _role_redirect(request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "❌ Please enter both username and password.")
            return render(request, 'login.html', {'portal': 'student'})

        # Lockout check
        session_key = LOCKOUT_KEY.format(username=username)
        attempts    = request.session.get(session_key, 0)

        if attempts >= MAX_FAILED_ATTEMPTS:
            messages.error(
                request,
                "🔒 Your account is temporarily locked due to too many failed "
                "login attempts. Please contact an administrator."
            )
            return render(request, 'login.html', {'portal': 'student', 'locked': True})


        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "❌ Your account is inactive. Contact the admin.")
                return render(request, 'login.html', {'portal': 'student'})

            # Check trainer approval
            try:
                profile = user.userprofile
                if profile.is_trainer and not profile.is_approved:
                    messages.error(
                        request,
                        "⏳ Your trainer account is pending admin approval."
                    )
                    return render(request, 'login.html', {'portal': 'student'})
            except UserProfile.DoesNotExist:
                pass

            # Successful login
            request.session.pop(session_key, None)   # clear lockout counter
            login(request, user)
            _log_action(request, 'LOGIN', f"User '{username}' logged in.", user=user)
            messages.success(request, f"🎉 Welcome back, {user.username}!")
            return _role_redirect(user)
        else:
            # Failed login
            request.session[session_key] = attempts + 1
            remaining = MAX_FAILED_ATTEMPTS - (attempts + 1)
            _log_action(
                request, 'FAILED_LOGIN',
                f"Failed login attempt for username '{username}'. "
                f"Attempt {attempts + 1}/{MAX_FAILED_ATTEMPTS}."
            )
            if remaining > 0:
                messages.error(
                    request,
                    f"❌ Wrong username or password. "
                    f"{remaining} attempt(s) remaining before lockout."
                )
            else:
                messages.error(
                    request,
                    "🔒 Account locked after too many failed attempts. "
                    "Contact an administrator."
                )

    return render(request, 'login.html', {'portal': 'student'})


def _role_redirect(user):
    """Return a redirect response appropriate for the user's role."""
    if _is_admin(user):
        return redirect('admin_dashboard')
    if _is_trainer(user):
        return redirect('trainer_dashboard')
    return redirect('student_portal')


# Hardcoded admin credentials — only this account can use the Admin login page
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'Admin@1234'


def admin_login_view(request):
    """
    /admin-login/ — Exclusive admin login.
    Only the single admin account (username='admin', password='Admin@1234')
    is permitted.  All other credentials are rejected.
    """
    if request.user.is_authenticated:
        if request.user.username == ADMIN_USERNAME:
            return redirect('admin_dashboard')
        messages.error(request, "⛔ You do not have admin access.")
        return redirect('landing')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "❌ Please enter both username and password.")
            return render(request, 'login.html', {'portal': 'admin'})

        if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
            _log_action(
                request, 'FAILED_LOGIN',
                f"Failed admin login attempt for username '{username}'."
            )
            messages.error(request, "⛔ Access denied. Only the admin account can log in here.")
            return render(request, 'login.html', {'portal': 'admin'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "❌ Admin account is inactive.")
                return render(request, 'login.html', {'portal': 'admin'})
            login(request, user)
            _log_action(request, 'LOGIN', f"Admin '{user.username}' logged in.", user=user)
            messages.success(request, f"🎉 Welcome, Admin {user.username}!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "❌ Wrong username or password.")

    return render(request, 'login.html', {'portal': 'admin'})


def logout_view(request):
    """/logout/ — Logs out and redirects to landing page."""
    if request.user.is_authenticated:
        _log_action(request, 'LOGOUT', f"User '{request.user.username}' logged out.")
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('landing')


# Password Management

@login_required
def password_change_view(request):
    """
    Allows a logged-in user to change their password.
    Uses PasswordChangeForm to run the registered password validators.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)   # keep user logged in
            _log_action(request, 'UPDATE',
                        f"User '{request.user.username}' changed their password.")
            messages.success(request, "✅ Your password has been changed successfully!")
            return redirect('student_portal')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'password_change.html', {'form': form})


# Student Portal

@login_required
def student_self_edit(request):
    """Allows a logged-in student to edit their own profile info."""
    try:
        student = request.user.student_profile
    except Exception:
        messages.error(request, "❌ No student profile linked to your account. Contact admin.")
        return redirect('student_portal')

    if request.method == 'POST':
        form = StudentSelfEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            _log_action(request, 'UPDATE',
                        f"Student '{student.name}' updated their own profile.")
            messages.success(request, "✅ Your profile has been updated successfully!")
            return redirect('student_portal')
    else:
        form = StudentSelfEditForm(instance=student)

    return render(request, 'student_self_edit.html', {'form': form, 'student': student})


@login_required
def student_portal(request):
    """
    Dashboard for the student portal.
    Shows search/filter options, student lists, and visible trainer feedback.
    """
    students = Student.objects.select_related('department').prefetch_related('enrolled_courses')

    # Search
    search = request.GET.get('search', '').strip()
    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(course__icontains=search)
        )

    # Filter by Department
    dept_id = request.GET.get('department', '')
    if dept_id:
        students = students.filter(department__id=dept_id)

    # Filter by Active
    active = request.GET.get('active', '')
    if active == 'yes':
        students = students.filter(is_active=True)
    elif active == 'no':
        students = students.filter(is_active=False)

    # Filter by Pass/Fail
    status = request.GET.get('status', '')
    if status == 'pass':
        students = students.filter(marks__gte=40)
    elif status == 'fail':
        students = students.filter(marks__lt=40)

    # Show visible feedback for the student
    my_feedback = []
    try:
        my_student  = request.user.student_profile
        my_feedback = Feedback.objects.filter(
            student=my_student, is_visible=True
        ).select_related('trainer', 'course').order_by('-created_at')
    except Exception:
        pass

    context = {
        **_dashboard_stats(),
        'students'       : students,
        'departments'    : Department.objects.all(),
        'search'         : search,
        'selected_dept'  : dept_id,
        'selected_active': active,
        'selected_status': status,
        'my_feedback'    : my_feedback,
    }
    return render(request, 'student_portal.html', context)


@login_required
def student_detail_view(request, pk):
    """/student/<pk>/ — View a single student's details."""
    student = get_object_or_404(Student, pk=pk)
    
    # Fetch latest marks update
    latest_marks_update = student.marks_history.first()
    
    # Filter feedbacks based on role
    if _is_admin(request.user):
        feedbacks = student.feedback_received.all().select_related('trainer', 'course').order_by('-created_at')
    elif _is_trainer(request.user):
        feedbacks = student.feedback_received.filter(trainer=request.user).select_related('trainer', 'course').order_by('-created_at')
    else:
        # Student user
        feedbacks = student.feedback_received.filter(is_visible=True).select_related('trainer', 'course').order_by('-created_at')
        
    context = {
        'student': student,
        'latest_marks_update': latest_marks_update,
        'feedbacks': feedbacks,
    }
    return render(request, 'student_detail.html', context)


# TRAINER PORTAL  (Day 4 - Task 1)

@_trainer_required
def trainer_dashboard(request):
    """
    /trainer/ — Trainer portal.
    A trainer sees only the students assigned to them.
    """
    assigned_students = Student.objects.filter(
        trainer=request.user
    ).select_related('department').prefetch_related('enrolled_courses')
    assigned_courses = request.user.assigned_courses.all()

    context = {
        'assigned_students': assigned_students,
        'assigned_courses' : assigned_courses,
        'total_assigned'   : assigned_students.count(),
        'pass_count'       : assigned_students.filter(marks__gte=40).count(),
        'fail_count'       : assigned_students.filter(marks__lt=40).count(),
        'recent_feedback'  : Feedback.objects.filter(
            trainer=request.user
        ).order_by('-created_at')[:5],
    }
    return render(request, 'trainer_dashboard.html', context)


@_trainer_required
def trainer_marks_update(request, pk):
    """
    Updates marks for an assigned student and records it in history.
    Verifies that the student is actually assigned to the trainer.
    """
    student = get_object_or_404(Student, pk=pk)

    # Ownership check — student must be assigned to this trainer
    if student.trainer != request.user:
        return HttpResponseForbidden(
            "<h1>403 Forbidden</h1>"
            "<p>You can only update marks for your own assigned students.</p>"
        )

    if request.method == 'POST':
        form = MarksWithReasonForm(request.POST)
        if form.is_valid():
            old_marks = student.marks
            new_marks = form.cleaned_data['marks']
            reason    = form.cleaned_data.get('reason', '')

            # Save updated marks on the student record
            student.marks = new_marks
            student.save()

            # Record the change in MarksHistory
            MarksHistory.objects.create(
                student    = student,
                updated_by = request.user,
                old_marks  = old_marks,
                new_marks  = new_marks,
                reason     = reason,
            )

            # Audit log
            _log_action(
                request, 'MARKS_UPDATE',
                f"Trainer '{request.user.username}' updated marks for "
                f"'{student.name}': {old_marks} → {new_marks}. Reason: {reason}"
            )

            messages.success(
                request,
                f"📝 Marks for '{student.name}' updated from {old_marks} to {new_marks}."
            )
            return redirect('trainer_dashboard')
    else:
        form = MarksWithReasonForm(initial={'marks': student.marks})

    marks_history = student.marks_history.all()[:10]
    return render(request, 'trainer_marks_form.html', {
        'form': form, 'student': student, 'marks_history': marks_history
    })


@_trainer_required
def trainer_feedback_add(request, student_pk):
    """
    Adds feedback comments and a rating for an assigned student.
    """
    student = get_object_or_404(Student, pk=student_pk)

    if student.trainer != request.user:
        return HttpResponseForbidden(
            "<h1>403 Forbidden</h1>"
            "<p>You can only add feedback for your own assigned students.</p>"
        )

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb            = form.save(commit=False)
            fb.trainer    = request.user
            fb.student    = student
            fb.save()
            _log_action(
                request, 'FEEDBACK',
                f"Trainer '{request.user.username}' added feedback for '{student.name}'."
            )
            messages.success(request, "✅ Feedback added successfully!")
            return redirect('trainer_dashboard')
    else:
        form = FeedbackForm()

    return render(request, 'trainer_feedback_form.html', {
        'form': form, 'student': student, 'action': 'Add Feedback'
    })


@_trainer_required
def trainer_feedback_edit(request, pk):
    """
    Allows a trainer to edit their own submitted feedback.
    """
    feedback = get_object_or_404(Feedback, pk=pk)

    if feedback.trainer != request.user:
        return HttpResponseForbidden(
            "<h1>403 Forbidden</h1>"
            "<p>You can only edit your own feedback.</p>"
        )

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            _log_action(
                request, 'FEEDBACK',
                f"Trainer '{request.user.username}' edited feedback #{pk}."
            )
            messages.success(request, "✅ Feedback updated successfully!")
            return redirect('trainer_dashboard')
    else:
        form = FeedbackForm(instance=feedback)

    return render(request, 'trainer_feedback_form.html', {
        'form': form, 'student': feedback.student, 'action': 'Edit Feedback'
    })


# Admin Portal

@_admin_required
def admin_dashboard(request):
    """/admin-portal/ — Admin dashboard with stats + full student CRUD table."""
    students = Student.objects.select_related('department').prefetch_related('enrolled_courses')

    # Search
    search = request.GET.get('search', '').strip()
    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(course__icontains=search)
        )

    # Filter by Department
    dept_id = request.GET.get('department', '')
    if dept_id:
        students = students.filter(department__id=dept_id)

    # Filter by Active
    active = request.GET.get('active', '')
    if active == 'yes':
        students = students.filter(is_active=True)
    elif active == 'no':
        students = students.filter(is_active=False)

    # Filter by Pass/Fail
    status = request.GET.get('status', '')
    if status == 'pass':
        students = students.filter(marks__gte=40)
    elif status == 'fail':
        students = students.filter(marks__lt=40)

    context = {
        **_dashboard_stats(),
        'students'        : students,
        'departments'     : Department.objects.all(),
        'search'          : search,
        'selected_dept'   : dept_id,
        'selected_active' : active,
        'selected_status' : status,
        # Day 4 extras for admin
        'recent_audit'    : AuditLog.objects.all()[:5],
        'trainer_count'   : UserProfile.objects.filter(role='trainer').count(),
        'pending_trainers': UserProfile.objects.filter(
            role='trainer', is_approved=False
        ).count(),
    }
    return render(request, 'admin_dashboard.html', context)


# Admin: Student CRUD

@_admin_required
def admin_student_add(request):
    """/admin-portal/students/add/ — Admin adds a new student."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            _log_action(request, 'CREATE', f"Admin created student '{student.name}'.")
            messages.success(request, f"🎉 Student '{student.name}' added successfully!")
            return redirect('admin_dashboard')
    else:
        form = StudentForm()
    return render(request, 'admin_student_form.html', {'form': form, 'action': 'Add Student'})


@_admin_required
def admin_student_edit(request, pk):
    """/admin-portal/students/<pk>/edit/ — Admin edits a student's full record."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            _log_action(request, 'UPDATE', f"Admin updated student '{student.name}'.")
            messages.success(request, f"✅ Student '{student.name}' updated successfully!")
            return redirect('admin_dashboard')
    else:
        form = StudentForm(instance=student)
    return render(request, 'admin_student_form.html', {
        'form': form, 'action': 'Edit Student', 'student': student
    })


@_admin_required
def admin_student_delete(request, pk):
    """/admin-portal/students/<pk>/delete/ — Admin deletes a student."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        student.delete()
        _log_action(request, 'DELETE', f"Admin deleted student '{name}'.")
        messages.success(request, f"🗑️ Student '{name}' deleted.")
        return redirect('admin_dashboard')
    return render(request, 'student_confirm_delete.html', {'student': student})


@_admin_required
def admin_update_marks(request, pk):
    """/admin-portal/students/<pk>/marks/ — Admin updates a student's marks."""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = MarksUpdateForm(request.POST, instance=student)
        if form.is_valid():
            old_marks = student.marks
            new_marks = form.cleaned_data['marks']
            form.save()
            # Record history
            MarksHistory.objects.create(
                student    = student,
                updated_by = request.user,
                old_marks  = old_marks,
                new_marks  = new_marks,
                reason     = "Updated by admin",
            )
            _log_action(
                request, 'MARKS_UPDATE',
                f"Admin updated marks for '{student.name}': {old_marks} → {new_marks}."
            )
            messages.success(
                request,
                f"📝 Marks for '{student.name}' updated to {student.marks}."
            )
            return redirect('admin_dashboard')
    else:
        form = MarksUpdateForm(instance=student)
    return render(request, 'admin_marks_form.html', {'form': form, 'student': student})


# Admin: Department Management

@_admin_required
def admin_department_list(request):
    """/admin-portal/departments/ — List all departments."""
    departments = Department.objects.all()
    return render(request, 'admin_department_list.html', {'departments': departments})


@_admin_required
def admin_department_add(request):
    """/admin-portal/departments/add/ — Create a new department."""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            _log_action(request, 'CREATE', f"Admin created department '{dept.name}'.")
            messages.success(request, f"✅ Department '{dept.name}' created!")
            return redirect('admin_department_list')
    else:
        form = DepartmentForm()
    return render(request, 'admin_department_form.html', {'form': form, 'action': 'Add Department'})


@_admin_required
def admin_department_edit(request, pk):
    """/admin-portal/departments/<pk>/edit/ — Edit a department."""
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            _log_action(request, 'UPDATE', f"Admin updated department '{dept.name}'.")
            messages.success(request, f"✅ Department '{dept.name}' updated!")
            return redirect('admin_department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'admin_department_form.html', {
        'form': form, 'action': 'Edit Department', 'dept': dept
    })


@_admin_required
def admin_department_delete(request, pk):
    """/admin-portal/departments/<pk>/delete/ — Delete a department."""
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        name = dept.name
        dept.delete()
        _log_action(request, 'DELETE', f"Admin deleted department '{name}'.")
        messages.success(request, f"🗑️ Department '{name}' deleted.")
        return redirect('admin_department_list')
    return render(request, 'admin_department_form.html', {
        'confirm_delete': True, 'dept': dept, 'action': 'Delete Department'
    })


# Admin: Course Management

@_admin_required
def admin_course_list(request):
    """/admin-portal/courses/ — List all courses."""
    courses = Course.objects.all()
    return render(request, 'admin_course_list.html', {'courses': courses})


@_admin_required
def admin_course_add(request):
    """/admin-portal/courses/add/ — Create a new course."""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            _log_action(request, 'CREATE', f"Admin created course '{course.name}'.")
            messages.success(request, f"✅ Course '{course.name}' created!")
            return redirect('admin_course_list')
    else:
        form = CourseForm()
    return render(request, 'admin_course_form.html', {'form': form, 'action': 'Add Course'})


@_admin_required
def admin_course_edit(request, pk):
    """/admin-portal/courses/<pk>/edit/ — Edit a course."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            _log_action(request, 'UPDATE', f"Admin updated course '{course.name}'.")
            messages.success(request, f"✅ Course '{course.name}' updated!")
            return redirect('admin_course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin_course_form.html', {
        'form': form, 'action': 'Edit Course', 'course': course
    })


@_admin_required
def admin_course_delete(request, pk):
    """/admin-portal/courses/<pk>/delete/ — Delete a course."""
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        name = course.name
        course.delete()
        _log_action(request, 'DELETE', f"Admin deleted course '{name}'.")
        messages.success(request, f"🗑️ Course '{name}' deleted.")
        return redirect('admin_course_list')
    return render(request, 'admin_course_form.html', {
        'confirm_delete': True, 'course': course, 'action': 'Delete Course'
    })


# Admin: Audit Log

@_admin_required
def admin_audit_log(request):
    """
    View audit logs (admin only).
    Supports searching, action filtering, and date range filtering.
    """
    logs = AuditLog.objects.select_related('user').all()

    # Search by description or username
    search = request.GET.get('search', '').strip()
    if search:
        logs = logs.filter(
            Q(description__icontains=search) |
            Q(user__username__icontains=search)
        )

    # Filter by action type
    action = request.GET.get('action', '')
    if action:
        logs = logs.filter(action_type=action)

    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to   = request.GET.get('date_to', '')
    if date_from:
        logs = logs.filter(timestamp__date__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__date__lte=date_to)

    # Pagination
    paginator = Paginator(logs, 15)  # 15 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build query params string to preserve filters in pagination links
    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    query_params = params.urlencode()

    context = {
        'page_obj'       : page_obj,
        'logs'           : page_obj.object_list,
        'action_choices' : AuditLog.ACTION_CHOICES,
        'search'         : search,
        'selected_action': action,
        'date_from'      : date_from,
        'date_to'        : date_to,
        'query_params'   : query_params,
    }
    return render(request, 'admin_audit_log.html', context)


# Admin: User Account Management

@_admin_required
def admin_user_list(request):
    """/admin-portal/users/ — List all non-admin users for management."""
    profiles = UserProfile.objects.select_related('user').exclude(role='admin')
    return render(request, 'admin_user_list.html', {'profiles': profiles})


@_admin_required
def admin_activate_user(request, user_pk):
    """
    Allows admins to toggle account active status and approval status.
    """
    target_user = get_object_or_404(User, pk=user_pk)
    profile     = get_object_or_404(UserProfile, user=target_user)

    if request.method == 'POST':
        # Toggle is_active on the Django User
        is_active   = 'is_active'   in request.POST
        is_approved = 'is_approved' in request.POST

        old_active   = target_user.is_active
        old_approved = profile.is_approved

        target_user.is_active = is_active
        target_user.save()

        profile.is_approved = is_approved
        profile.save()

        _log_action(
            request, 'ACCOUNT_STATUS',
            f"Admin changed status of '{target_user.username}': "
            f"is_active={old_active}→{is_active}, "
            f"is_approved={old_approved}→{is_approved}."
        )
        messages.success(
            request,
            f"✅ Account status for '{target_user.username}' updated."
        )
        return redirect('admin_user_list')

    return render(request, 'admin_activate_user.html', {
        'target_user': target_user,
        'profile'    : profile,
    })


# Admin: Trainer Management

@_admin_required
def admin_trainer_list(request):
    """
    /admin-portal/trainers/ — List all trainers.
    Can filter by course.
    """
    trainers = User.objects.filter(userprofile__role='trainer').select_related('userprofile').prefetch_related('assigned_courses').order_by('username')
    courses = Course.objects.all()

    selected_course_id = request.GET.get('course', '')
    if selected_course_id:
        trainers = trainers.filter(assigned_courses__id=selected_course_id).distinct()

    # Pagination for trainers
    paginator = Paginator(trainers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Build query params
    params = request.GET.copy()
    if 'page' in params:
        del params['page']
    query_params = params.urlencode()

    context = {
        'page_obj': page_obj,
        'trainers': page_obj.object_list,
        'courses': courses,
        'selected_course': selected_course_id,
        'query_params': query_params,
    }
    return render(request, 'admin_trainer_list.html', context)


@_admin_required
def admin_trainer_add(request):
    """/admin-portal/trainers/add/ — Add new trainer."""
    if request.method == 'POST':
        form = AdminTrainerAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            _log_action(request, 'CREATE', f"Admin created trainer '{user.username}'.")
            messages.success(request, f"✅ Trainer '{user.username}' created successfully!")
            return redirect('admin_trainer_list')
    else:
        form = AdminTrainerAddForm()
    return render(request, 'admin_trainer_form.html', {'form': form, 'action': 'Add Trainer'})


@_admin_required
def admin_trainer_edit(request, pk):
    """/admin-portal/trainers/<pk>/edit/ — Edit trainer."""
    trainer = get_object_or_404(User, pk=pk, userprofile__role='trainer')
    if request.method == 'POST':
        form = AdminTrainerEditForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            _log_action(request, 'UPDATE', f"Admin updated trainer '{trainer.username}'.")
            messages.success(request, f"✅ Trainer '{trainer.username}' updated successfully!")
            return redirect('admin_trainer_list')
    else:
        form = AdminTrainerEditForm(instance=trainer)
    return render(request, 'admin_trainer_form.html', {
        'form': form, 'action': 'Edit Trainer', 'trainer': trainer
    })


@_admin_required
def admin_trainer_delete(request, pk):
    """/admin-portal/trainers/<pk>/delete/ — Remove trainer."""
    trainer = get_object_or_404(User, pk=pk, userprofile__role='trainer')
    if request.method == 'POST':
        username = trainer.username
        trainer.delete()
        _log_action(request, 'DELETE', f"Admin deleted trainer '{username}'.")
        messages.success(request, f"🗑️ Trainer '{username}' deleted.")
        return redirect('admin_trainer_list')
    return render(request, 'admin_trainer_form.html', {
        'confirm_delete': True, 'trainer': trainer, 'action': 'Delete Trainer'
    })