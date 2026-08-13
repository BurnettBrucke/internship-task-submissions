from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Q
from django.core.cache import cache
from django.utils import timezone

from .models import Student, Department, Course, AuditLog, Feedback, MarksHistory
from django.contrib.auth.models import User
from .forms import StudentForm, RegistrationForm, FeedbackForm, MarksUpdateForm
from .decorators import role_required
from . import services

def home(request):
    """
    Root URL redirecting users to their role-specific dashboard if authenticated,
    otherwise rendering the public stats dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    stats = services.get_dashboard_stats()
    context = {
        'company_name': 'Bug Network Private Limited',
        **stats
    }
    return render(request, 'students/home.html', context)


@login_required
def dashboard_redirect(request):
    """
    Redirects user to their role-based dashboard.
    """
    # Superuser has admin access
    if request.user.is_superuser:
        return redirect('admin_dashboard')
        
    try:
        user_role = request.user.profile.role
    except AttributeError:
        user_role = 'student'
        
    if user_role == 'admin':
        return redirect('admin_dashboard')
    elif user_role == 'trainer':
        return redirect('trainer_dashboard')
    else:
        return redirect('student_dashboard')


@login_required
@role_required('admin')
def admin_dashboard(request):
    """
    Administrator dashboard view.
    """
    stats = services.get_dashboard_stats()
    # Add admin-specific counts
    stats['total_trainers'] = User.objects.filter(profile__role='trainer').count()
    stats['total_users'] = User.objects.count()
    
    recent_students = (
        Student.objects.select_related('department')
        .prefetch_related('courses')
        .order_by('-joined_date', '-id')[:5]
    )
    recent_users = User.objects.select_related('profile').order_by('-date_joined', '-id')[:5]
    
    context = {
        'stats': stats,
        'recent_students': recent_students,
        'recent_users': recent_users,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)


@login_required
@role_required('trainer')
def trainer_dashboard(request):
    """
    Trainer dashboard view.
    """
    context = services.get_trainer_dashboard_stats(request.user)
    return render(request, 'dashboards/trainer_dashboard.html', context)


@login_required
@role_required('student')
def student_dashboard(request):
    """
    Student dashboard view.
    """
    context = services.get_student_dashboard_data(request.user)
    return render(request, 'dashboards/student_dashboard.html', context)


def about(request):
    html_content = "<h1>About Page</h1><p>Welcome to the About page of our Django application!</p>"
    return HttpResponse(html_content)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role') or 'student'
            if role == 'trainer':
                user.is_active = False
            user.save()
            
            # Ensure profile has correct role
            user.profile.role = role
            user.profile.save()
            
            # Create Audit Log for registration
            AuditLog.objects.create(
                user=None,
                action='create',
                affected_object=f"User: {user.username}",
                description=f"New user registered: {user.username} with role {role}. Active: {user.is_active}.",
                ip_address=get_client_ip(request)
            )
            
            if role == 'trainer':
                messages.warning(request, "Registration successful! Your trainer account requires administrator approval before you can log in.")
            else:
                messages.success(request, "Registration successful! Please log in.")
            return redirect(reverse('login'))
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        
        # Check block status in cache
        if username:
            block_key = f"login_block_{username}"
            if cache.get(block_key):
                messages.error(request, "This account is temporarily blocked due to 5 consecutive failed login attempts. Please try again later.")
                AuditLog.objects.create(
                    user=None,
                    action='failed_login',
                    description=f"Blocked login attempt for user: {username}",
                    ip_address=get_client_ip(request)
                )
                form = AuthenticationForm()
                return render(request, 'registration/login.html', {'form': form})
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Check if active
            if not user.is_active:
                messages.error(request, "Your account is inactive. If you registered as a trainer, your account requires administrator approval.")
                AuditLog.objects.create(
                    user=user,
                    action='failed_login',
                    description=f"Attempted login to inactive account: {user.username}",
                    ip_address=get_client_ip(request)
                )
                return render(request, 'registration/login.html', {'form': form})
            
            # Reset attempts
            if username:
                cache.delete(f"failed_attempts_{username}")
                
            login(request, user)
            AuditLog.objects.create(
                user=user,
                action='login',
                description=f"User {user.username} logged in successfully.",
                ip_address=get_client_ip(request)
            )
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(reverse('home'))
        else:
            # Failed attempt
            if username:
                failed_key = f"failed_attempts_{username}"
                attempts = cache.get(failed_key, 0) + 1
                cache.set(failed_key, attempts, timeout=300) # 5 minutes tracker
                
                # Try to get user
                try:
                    user_obj = User.objects.get(username=username)
                except User.DoesNotExist:
                    user_obj = None
                
                if attempts >= 5:
                    cache.set(f"login_block_{username}", True, timeout=300) # 5 minutes block
                    messages.error(request, "Account temporarily blocked due to 5 consecutive failed login attempts. Please try again in 5 minutes.")
                else:
                    messages.error(request, f"Invalid username or password. {5 - attempts} attempts remaining.")
                
                AuditLog.objects.create(
                    user=user_obj,
                    action='failed_login',
                    description=f"Failed login attempt for user: {username} (Attempt {attempts}/5)",
                    ip_address=get_client_ip(request)
                )
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action='logout',
            description=f"User {request.user.username} logged out.",
            ip_address=get_client_ip(request)
        )
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect(reverse('login'))


@login_required
@role_required('admin', 'trainer')
def student_list(request):
    """
    Student List view rendering tabular student data with multi-criterion filtering and search.
    Trainers can only view students enrolled in their assigned courses.
    """
    students_qs = services.filter_students(request.GET)
    
    # Check permissions & filter by ownership/assignment
    if not (request.user.is_superuser or request.user.profile.role == 'admin'):
        # Trainer: limit query to students in trainer's assigned courses
        assigned_courses = Course.objects.filter(assigned_trainer=request.user)
        students_qs = students_qs.filter(courses__in=assigned_courses).distinct()
        
    total_count = students_qs.count()
    active_count = students_qs.filter(active_status=True).count()
    
    departments = Department.objects.all().order_by('name')
    courses = Course.objects.all().order_by('course_name')
    
    from django.core.paginator import Paginator
    paginator = Paginator(students_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'students': page_obj,
        'page_obj': page_obj,
        'total_count': total_count,
        'active_count': active_count,
        'departments': departments,
        'courses': courses,
        'selected_q': request.GET.get('q', ''),
        'selected_department': request.GET.get('department', ''),
        'selected_course': request.GET.get('course', ''),
        'selected_active': request.GET.get('active_status', ''),
        'selected_pass_fail': request.GET.get('pass_fail_status', ''),
    }
    return render(request, 'students/student_list.html', context)


@login_required
@role_required('admin')
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            # Log audit
            AuditLog.objects.create(
                user=request.user,
                action='create',
                affected_object=f"Student: {student.name}",
                description=f"Admin {request.user.username} created student {student.name}.",
                ip_address=get_client_ip(request)
            )
            messages.success(request, "Student added successfully!")
            return redirect(reverse('student_list'))
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {'form': form, 'is_edit': False})


@login_required
def student_detail(request, id):
    student = get_object_or_404(
        Student.objects.select_related('department').prefetch_related('courses'),
        id=id
    )
    
    # Authorization checks
    if not services.can_user_view_student(request.user, student):
        raise PermissionDenied
        
    # Calculate profile completion if student is viewing themselves
    profile_completion = services.calculate_profile_completion(student) if getattr(getattr(request.user, 'profile', None), 'role', None) == 'student' else 0
            
    # Retrieve and filter feedbacks
    if request.user.profile.role == 'student':
        feedbacks = student.feedbacks.filter(is_visible=True).select_related('trainer', 'course').order_by('-created_at')
    else:
        feedbacks = student.feedbacks.all().select_related('trainer', 'course').order_by('-created_at')
        
    # Retrieve marks history
    marks_history = student.marks_history.all().select_related('updater', 'course').order_by('-timestamp')
    latest_update = marks_history.first()
    
    # Check if logged-in user is an assigned trainer
    is_assigned_trainer = False
    if request.user.profile.role == 'trainer':
        is_assigned_trainer = student.courses.filter(assigned_trainer=request.user).exists()
        
    context = {
        'student': student,
        'profile_completion': profile_completion,
        'feedbacks': feedbacks,
        'marks_history': marks_history,
        'latest_update': latest_update,
        'is_assigned_trainer': is_assigned_trainer,
    }
    return render(request, 'students/student_detail.html', context)


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    user_role = request.user.profile.role if not request.user.is_superuser else 'admin'
    
    # Authorization checks
    is_authorized = False
    if user_role == 'admin':
        is_authorized = True
    elif user_role == 'trainer':
        is_authorized = student.courses.filter(assigned_trainer=request.user).exists()
        
    if not is_authorized:
        raise PermissionDenied

    if request.method == 'POST':
        if user_role == 'trainer':
            # Trainer can ONLY update marks field
            marks = request.POST.get('marks')
            if marks is not None:
                try:
                    marks_val = int(marks)
                    if 0 <= marks_val <= 100:
                        old_marks = student.marks
                        student.marks = marks_val
                        student.save()
                        
                        # Save marks history
                        assigned_course = student.courses.filter(assigned_trainer=request.user).first()
                        MarksHistory.objects.create(
                            student=student,
                            course=assigned_course,
                            previous_marks=old_marks,
                            new_marks=marks_val,
                            updater=request.user,
                            reason="Trainer quick marks update"
                        )
                        
                        # Log audit
                        AuditLog.objects.create(
                            user=request.user,
                            action='marks_update',
                            affected_object=f"Student: {student.name}",
                            description=f"Trainer {request.user.username} updated marks for {student.name} from {old_marks} to {marks_val} via edit page.",
                            ip_address=get_client_ip(request)
                        )
                        messages.success(request, "Student marks updated successfully!")
                        return redirect(reverse('student_detail', kwargs={'id': student.id}))
                    else:
                        messages.error(request, "Marks must be between 0 and 100.")
                except ValueError:
                    messages.error(request, "Invalid marks value.")
            else:
                messages.error(request, "Marks value is required.")
        else:
            # Admin can update all fields
            old_marks = student.marks
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                new_student = form.save(commit=False)
                new_marks = new_student.marks
                if old_marks != new_marks:
                    MarksHistory.objects.create(
                        student=student,
                        course=None,
                        previous_marks=old_marks,
                        new_marks=new_marks,
                        updater=request.user,
                        reason="Administrator student profile update"
                    )
                    AuditLog.objects.create(
                        user=request.user,
                        action='marks_update',
                        affected_object=f"Student: {student.name}",
                        description=f"Admin {request.user.username} updated marks for {student.name} from {old_marks} to {new_marks}.",
                        ip_address=get_client_ip(request)
                    )
                new_student.save()
                form.save_m2m()
                
                # Log audit
                AuditLog.objects.create(
                    user=request.user,
                    action='update',
                    affected_object=f"Student: {student.name}",
                    description=f"Admin {request.user.username} updated student profile for {student.name}.",
                    ip_address=get_client_ip(request)
                )
                messages.success(request, "Student updated successfully!")
                return redirect(reverse('student_detail', kwargs={'id': student.id}))
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', {'form': form, 'student': student, 'is_edit': True})


@login_required
@role_required('admin')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student_name = student.name
        student.delete()
        # Log audit
        AuditLog.objects.create(
            user=request.user,
            action='delete',
            affected_object=f"Student: {student_name}",
            description=f"Admin {request.user.username} deleted student {student_name}.",
            ip_address=get_client_ip(request)
        )
        messages.success(request, "Student deleted successfully!")
        return redirect(reverse('student_list'))
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@login_required
@role_required('admin')
def user_management(request):
    """
    View for administrators to search and manage system accounts, including approving trainers.
    """
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    
    q = request.GET.get('q', '').strip()
    if q:
        users = users.filter(username__icontains=q) | users.filter(email__icontains=q)
        
    context = {
        'users': users,
        'q': q,
    }
    return render(request, 'dashboards/user_management.html', context)


@login_required
@role_required('admin')
def toggle_user_status(request, user_id):
    """
    Action for administrators to activate/approve or deactivate user accounts.
    """
    user_to_toggle = get_object_or_404(User, id=user_id)
    if user_to_toggle == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect('user_management')
        
    user_to_toggle.is_active = not user_to_toggle.is_active
    user_to_toggle.save()
    
    status_str = "activated/approved" if user_to_toggle.is_active else "deactivated"
    messages.success(request, f"Account for {user_to_toggle.username} has been {status_str} successfully.")
    
    # Log the action in AuditLog
    AuditLog.objects.create(
        user=request.user,
        action='status_change',
        affected_object=f"User: {user_to_toggle.username}",
        description=f"Admin {request.user.username} toggled status of {user_to_toggle.username} to {'Active' if user_to_toggle.is_active else 'Inactive'}.",
        ip_address=get_client_ip(request)
    )
    
    return redirect('user_management')


@login_required
@role_required('trainer')
def add_feedback(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    shared_courses = student.courses.filter(assigned_trainer=request.user)
    if not shared_courses.exists():
        raise PermissionDenied("You are not assigned to this student.")
        
    if request.method == 'POST':
        form = FeedbackForm(request.POST, trainer=request.user, student=student)
        if form.is_valid():
            services.create_feedback(
                student=student,
                trainer_user=request.user,
                course=form.cleaned_data['course'],
                rating=form.cleaned_data['rating'],
                comments=form.cleaned_data['comments'],
                is_visible=form.cleaned_data.get('is_visible', True),
                ip_address=get_client_ip(request)
            )
            messages.success(request, "Feedback added successfully!")
            return redirect(reverse('student_detail', kwargs={'id': student.id}))
    else:
        form = FeedbackForm(trainer=request.user, student=student)
        
    context = {
        'form': form,
        'student': student,
        'is_edit': False,
    }
    return render(request, 'students/feedback_form.html', context)


@login_required
@role_required('trainer')
def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if feedback.trainer != request.user:
        raise PermissionDenied("You can only edit your own feedback.")
        
    student = feedback.student
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback, trainer=request.user, student=student)
        if form.is_valid():
            form.save()
            
            # Log audit
            AuditLog.objects.create(
                user=request.user,
                action='update',
                affected_object=f"Feedback: {feedback.id}",
                description=f"Trainer {request.user.username} updated feedback (ID: {feedback.id}) for student {student.name}.",
                ip_address=get_client_ip(request)
            )
            messages.success(request, "Feedback updated successfully!")
            return redirect(reverse('student_detail', kwargs={'id': student.id}))
    else:
        form = FeedbackForm(instance=feedback, trainer=request.user, student=student)
        
    context = {
        'form': form,
        'student': student,
        'is_edit': True,
    }
    return render(request, 'students/feedback_form.html', context)


@login_required
def update_marks(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    user_role = request.user.profile.role if not request.user.is_superuser else 'admin'
    
    if user_role == 'student':
        raise PermissionDenied("Students are blocked from updating marks.")
        
    if user_role == 'trainer':
        shared_courses = student.courses.filter(assigned_trainer=request.user)
        if not shared_courses.exists():
            raise PermissionDenied("You are not assigned to this student.")
    elif user_role != 'admin':
        raise PermissionDenied("Only trainers and administrators can update marks.")
            
    if request.method == 'POST':
        form = MarksUpdateForm(request.POST, trainer=request.user, student=student)
        if form.is_valid():
            course = form.cleaned_data['course']
            new_marks = form.cleaned_data['new_marks']
            reason = form.cleaned_data['reason']
            
            services.update_student_marks(
                student=student,
                course=course,
                new_marks=new_marks,
                updater_user=request.user,
                reason=reason,
                ip_address=get_client_ip(request)
            )
            messages.success(request, f"Marks updated successfully to {new_marks}!")
            return redirect(reverse('student_detail', kwargs={'id': student.id}))
    else:
        form = MarksUpdateForm(trainer=request.user, student=student, initial={'new_marks': student.marks})
        
    context = {
        'form': form,
        'student': student,
    }
    return render(request, 'students/marks_update_form.html', context)


@login_required
@role_required('admin')
def audit_logs(request):
    logs = AuditLog.objects.select_related('user').all().order_by('-timestamp')
    
    # Search filter
    q = request.GET.get('q', '').strip()
    if q:
        logs = logs.filter(
            Q(description__icontains=q) |
            Q(user__username__icontains=q) |
            Q(affected_object__icontains=q)
        )
        
    # Action type filter
    action_filter = request.GET.get('action_type', '').strip()
    if action_filter:
        logs = logs.filter(action=action_filter)
        
    # Date range filters
    start_date = request.GET.get('start_date', '').strip()
    if start_date:
        logs = logs.filter(timestamp__date__gte=start_date)
        
    end_date = request.GET.get('end_date', '').strip()
    if end_date:
        logs = logs.filter(timestamp__date__lte=end_date)
        
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'q': q,
        'action_filter': action_filter,
        'start_date': start_date,
        'end_date': end_date,
        'action_choices': AuditLog.ACTION_CHOICES,
    }
    return render(request, 'dashboards/audit_logs.html', context)


def custom_403(request, exception=None):
    return render(request, '403.html', status=403)


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)
