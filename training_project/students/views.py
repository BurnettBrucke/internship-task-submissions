from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from .forms import StudentForm, RegistrationForm, MarksUpdateForm, FeedbackForm,TrainerForm,TrainerEditForm
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import ( Student, Department, Course,UserProfile, TrainerProfile, AuditLog, Feedback,)
from django.contrib.auth.models import User
from .models import MarksUpdateHistory
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q , Prefetch
from .decorators import role_required

from django.contrib.auth.forms import PasswordChangeForm
from .services import (
    get_dashboard_data,
    get_filtered_students,
    update_student_marks,
    create_student_feedback,
    trainer_can_access_student,
)

def create_audit_log(
    user,
    action,
    affected_object=None,
    description=None,
    request=None
  ):
    ip_address = None

    if request:
        ip_address = request.META.get('REMOTE_ADDR')

    AuditLog.objects.create(
        user=user,
        action=action,
        affected_object=affected_object,
        description=description,
        ip_address=ip_address
    )

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                is_approved=False
            )
            
            if form.cleaned_data['role'] == 'trainer':
                TrainerProfile.objects.create(
                    user=user
                )

            messages.success(
                request,
                'Registration successful! Please wait for admin approval.'
            )

            return redirect('login')

    else:
        form = RegistrationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )

def user_login(request):

    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)

            # Get profile before authentication
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                messages.error(
                    request,
                    'User profile not found.'
                )
                return redirect('login')

            # Check if account is already blocked
            if profile.failed_login_attempts >= 5:
                messages.error(
                    request,
                    'Your account is blocked due to multiple failed login attempts.'
                )
                return redirect('login')

            # Account active check
            if not user.is_active:
                messages.error(
                    request,
                   'Your account is inactive. Please contact admin.'
                )
                return redirect('login')
            
            # Trainer approval check
            if profile.role in ['student', 'trainer'] and not profile.is_approved:
                messages.error(
                   request,
                   'Your account is pending approval by admin.'
                )
                return redirect('login')

            # Authenticate user
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if authenticated_user is not None:

                # Successful login → reset failed attempts
                profile.failed_login_attempts = 0
                profile.save()

                login(request, authenticated_user)

                create_audit_log(
                    authenticated_user,
                   "LOGIN",
                    affected_object=f"User {authenticated_user.username}",
                    description="User logged in successfully",
                    request=request
                )

                if profile.role == 'admin':
                    return redirect('admin_dashboard')

                elif profile.role == 'trainer':
                    return redirect('trainer_dashboard')

                else:
                    return redirect('student_dashboard')

            else:

                # Wrong password → increase failed attempts
                profile.failed_login_attempts += 1
                profile.save()

                create_audit_log(
    user,
    "FAILED",
    affected_object=f"User {user.username}",
    description="Failed login attempt",
    request=request
)

                if profile.failed_login_attempts >= 5:

                    messages.error(
                        request,
                        'Your account has been blocked after 5 failed login attempts.'
                    )

                else:

                    remaining_attempts = (
                        5 - profile.failed_login_attempts
                    )

                    messages.error(
                        request,
                        f'Invalid email or password. '
                        f'{remaining_attempts} attempt(s) remaining.'
                    )

        except User.DoesNotExist:

            messages.error(
                request,
                'Invalid email or password.'
            )

    return render(
        request,
        'registration/login.html'
    )

@login_required(login_url='login')
def user_logout(request):

    create_audit_log(
        request.user,
        "LOGOUT",
        affected_object=f"User {request.user.username}",
        description="User logged out",
        request=request
    )

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully!'
    )

    return redirect('login')

@login_required(login_url='login')
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                'Your password has been changed successfully.'
            )

            profile = request.user.profile

            if profile.role == 'admin':
                return redirect('admin_dashboard')

            elif profile.role == 'trainer':
                return redirect('trainer_dashboard')

            else:
                return redirect('student_dashboard')

    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'registration/password_change.html',
        {
            'form': form,
        }
    )

def home(request):
    company_name = "Bug Network Private Limited"

    return render(
        request,
        'students/home.html',
        {'company_name': company_name}
    )

def about(request):
    return render(request, 'students/about.html')

@login_required(login_url='login')
def dashboard(request):

    role = request.user.profile.role

    if role == 'admin':
        return redirect('admin_dashboard')

    elif role == 'trainer':
        return redirect('trainer_dashboard')

    elif role == 'student':
        return redirect('student_dashboard')

    return redirect('login')

@login_required(login_url='login')
@role_required(['admin'])
def admin_dashboard(request):
    dashboard_data = get_dashboard_data()

    return render(
        request,
        'dashboards/admin_dashboard.html',
        dashboard_data
    )
    
@login_required(login_url='login')
@role_required(['admin'])
def admin_feedback_list(request):

    feedbacks = Feedback.objects.select_related(
        'student',
        'trainer',
        'course'
    ).order_by('-created_at')

    return render(
        request,
        'students/admin_feedback_list.html',
        {
            'feedbacks': feedbacks,
        }
    )

@login_required(login_url='login')
@role_required(['trainer'])
def trainer_dashboard(request):
    trainer_profile = request.user.trainer_profile

    if not trainer_profile.user.profile.is_approved:
        messages.warning(
            request,
            'Your trainer account is pending admin approval.'
        )
        return redirect('login')

    courses = trainer_profile.courses.all()

    students = Student.objects.filter(
        courses__in=courses
    ).distinct().prefetch_related(
        Prefetch(
            'marks_history',
            queryset=MarksUpdateHistory.objects.select_related(
                'trainer'
            ).order_by('-updated_at'),
            to_attr='all_marks_history'
        )
    )

    for student in students:
        student.latest_marks_update = (
            student.all_marks_history[0]
            if student.all_marks_history
            else None
        )

    feedbacks = Feedback.objects.filter(
        trainer=request.user
    ).select_related(
        'student',
        'course'
    ).order_by('-created_at')

    return render(
        request,
        'dashboards/trainer_dashboard.html',
        {
            'courses': courses,
            'students': students,
            'feedbacks': feedbacks,
        }
    )


@login_required(login_url='login')
@role_required(['trainer'])
def trainer_students(request):

    trainer_profile = request.user.trainer_profile

    students = Student.objects.filter(
        courses__in=trainer_profile.courses.all()
    ).distinct()

    return render(
        request,
        'students/trainer_students.html',
        {
            'students': students,
        }
    )

@login_required(login_url='login')
@role_required(['student'])
def student_dashboard(request):

    profile = request.user.profile
    student = profile.student

    if student is None:
        return render(
            request,
            'students/student_profile_pending.html'
        )

    feedbacks = student.feedbacks.filter(
        is_visible=True
    ).order_by('-created_at')

    marks_history = student.marks_history.all().order_by('-updated_at')

    return render(
        request,
        'dashboards/student_dashboard.html',
        {
            'student': student,
            'courses': student.courses.all(),
            'feedbacks': feedbacks,
            'marks_history': marks_history,
        }
    )
    
@login_required(login_url='login')
@role_required(['admin'])
def student_list(request):

    students = get_filtered_students(request.GET)

    students = students.order_by('id')

    paginator = Paginator(students, 5)

    page_number = request.GET.get('page')

    query_params = request.GET.copy()
    query_params.pop('page', None)

    students = paginator.get_page(page_number)  

    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        active_status=True
    ).count()

    # Dropdown data
    departments = Department.objects.all()
    courses = Course.objects.all()

    return render(
        request,
        'students/student_list.html',
        {
            'students': students,
            'total_students': total_students,
            'active_students': active_students,
            'departments': departments,
            'courses': courses,
            'query_params': query_params.urlencode(),
        }
    )


@login_required(login_url='login')
def student_detail(request, pk):

    profile = request.user.profile

    student = get_object_or_404(Student, pk=pk)

    if profile.role == 'student':

        if profile.student_id != student.id:
            return HttpResponseForbidden(
                "You do not have permission to access this student."
            )

    elif profile.role == 'trainer':

        if not student.courses.filter(
            trainers=request.user
        ).exists():
            return HttpResponseForbidden(
                "You do not have permission to access this student."
            )

    elif profile.role != 'admin':

        return HttpResponseForbidden(
            "You do not have permission to access this student."
        )

    return render(
        request,
        'students/student_detail.html',
        {'student': student}
    )


@login_required(login_url='login')
@role_required(['admin'])
def add_student(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save()

            create_audit_log(
             request.user,
             "CREATE",
              affected_object=f"Student {student.name}",
              description="Student created",
             request=request
            )

            messages.success(
                request,
                'Student added successfully!'
            )

            return redirect('student_list')

    else:
        form = StudentForm()

    return render(
        request,
        'students/student_form.html',
        {
            'form': form,
            'title': 'Add Student'
        }
    )

# Edit student
@login_required(login_url='login')
@role_required(['admin'])
def edit_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            student = form.save()

            create_audit_log(
    request.user,
    "UPDATE",
    affected_object=f"Student {student.name}",
    description="Student updated",
    request=request
)

            messages.success(
                request,
                'Student updated successfully!'
            )

            return redirect('student_detail', pk=student.pk)

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'students/student_form.html',
        {
            'form': form,
            'title': 'Edit Student'
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def delete_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student_name = student.name

        create_audit_log(
    request.user,
    "DELETE",
    affected_object=f"Student {student_name}",
    description="Student deleted",
    request=request
)

        student.delete()

        messages.success(
            request,
            'Student deleted successfully!'
        )

        return redirect('student_list')

    return render(
        request,
        'students/student_confirm_delete.html',
        {'student': student}
    )

@login_required(login_url='login')
@role_required(['trainer'])
def update_marks(request, pk):
    trainer_profile = request.user.trainer_profile

    student = get_object_or_404(Student, pk=pk)

    if not trainer_can_access_student(
        trainer_profile,
        student
    ):
        return HttpResponseForbidden(
            "You do not have permission to update this student."
        )

    if request.method == 'POST':
        previous_marks = student.marks

        form = MarksUpdateForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            new_marks = form.cleaned_data['marks']
            reason = form.cleaned_data['reason']

            student = update_student_marks(
                student=student,
                trainer=request.user,
                previous_marks=previous_marks,
                new_marks=new_marks,
                reason=reason
            )

            create_audit_log(
                request.user,
                "UPDATE",
                affected_object=f"Student {student.name}",
                description=(
                    f"Marks updated from {previous_marks} "
                    f"to {new_marks}. Reason: {reason}"
                ),
                request=request
            )

            messages.success(
                request,
                'Student marks updated successfully.'
            )

            return redirect('trainer_dashboard')

    else:
        form = MarksUpdateForm(instance=student)

    return render(
        request,
        'students/trainer_update_marks.html',
        {
            'form': form,
            'student': student
        }
    )
    
@login_required(login_url='login')
@role_required(['trainer'])
def marks_history(request, pk):

    trainer_profile = request.user.trainer_profile

    student = get_object_or_404(
        Student,
        pk=pk
    )

    # Check whether this student belongs
    # to any course assigned to this trainer
    if not trainer_can_access_student(
        trainer_profile,
        student
    ):
        return HttpResponseForbidden(
           "You do not have permission to view this student's marks history."
        )

    history = MarksUpdateHistory.objects.filter(
        student=student
    ).select_related(
        'trainer'
    ).order_by(
        '-updated_at'
    )

    return render(
        request,
        'students/marks_history.html',
        {
            'student': student,
            'history': history,
        }
    )

@login_required(login_url='login')
@role_required(['trainer'])
def add_feedback(request, pk):
    trainer_profile = request.user.trainer_profile

    student = get_object_or_404(Student, pk=pk)

    trainer_courses = trainer_profile.courses.filter(
        students=student
    )

    if not trainer_courses.exists():
        return HttpResponseForbidden(
            "You do not have permission to give feedback to this student."
        )

    if request.method == 'POST':
        form = FeedbackForm(
            request.POST,
            courses=trainer_courses
        )

        if form.is_valid():
            feedback_text = form.cleaned_data['feedback']
            rating = form.cleaned_data['rating']
            course = form.cleaned_data['course']
            is_visible = form.cleaned_data['is_visible']

            feedback = create_student_feedback(
                student=student,
                trainer=request.user,
                course=course,
                feedback_text=feedback_text,
                rating=rating,
                is_visible=is_visible
            )

            create_audit_log(
                request.user,
                "CREATE",
                affected_object=f"Student {student.name}",
                description="Feedback added",
                request=request
            )

            messages.success(
                request,
                'Feedback added successfully.'
            )

            return redirect('trainer_dashboard')

    else:
        form = FeedbackForm(
            courses=trainer_courses
        )

    return render(
        request,
        'students/add_feedback.html',
        {
            'form': form,
            'student': student
        }
    )

@login_required(login_url='login')
@role_required(['trainer'])
def edit_feedback(request, pk):

    feedback = get_object_or_404(
        Feedback,
        pk=pk,
        trainer=request.user
    )

    trainer_profile = request.user.trainer_profile

    trainer_courses = trainer_profile.courses.filter(
        students=feedback.student
    )

    if not trainer_courses.exists():
        return HttpResponseForbidden(
            "You do not have permission to edit this feedback."
        )

    if request.method == 'POST':

        form = FeedbackForm(
            request.POST,
            instance=feedback,
            courses=trainer_courses
        )

        if form.is_valid():

            form.save()

            create_audit_log(
                request.user,
                "UPDATE",
                affected_object=f"Student {feedback.student.name}",
                description="Feedback updated",
                request=request
            )

            messages.success(
                request,
                'Feedback updated successfully.'
            )

            return redirect('trainer_dashboard')

    else:

        form = FeedbackForm(
            instance=feedback,
            courses=trainer_courses
        )

    return render(
        request,
        'students/edit_feedback.html',
        {
            'form': form,
            'feedback': feedback,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def trainer_list(request):

    trainers = TrainerProfile.objects.select_related(
        'user',
        'user__profile'
    ).prefetch_related(
        'courses'
    )

    return render(
        request,
        'students/trainer_list.html',
        {
            'trainers': trainers,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def course_list(request):

    courses = Course.objects.all()

    return render(
        request,
        'students/course_list.html',
        {
            'courses': courses,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def add_course(request):

    if request.method == 'POST':

        course_name = request.POST['course_name']
        code = request.POST['code']
        duration = request.POST['duration']
        active_status = request.POST.get('active_status') == 'on'

        course = Course.objects.create(
            course_name=course_name,
            code=code,
            duration=duration,
            active_status=active_status
        )

        create_audit_log(
    request.user,
    "CREATE",
    affected_object=f"Course {course.course_name}",
    description="Course created",
    request=request
)

        messages.success(
            request,
            'Course added successfully.'
        )

        return redirect('course_list')

    return render(
        request,
        'students/course_form.html'
    )

@login_required(login_url='login')
@role_required(['admin'])
def edit_course(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == 'POST':

        course.course_name = request.POST['course_name']
        course.code = request.POST['code']
        course.duration = request.POST['duration']
        course.active_status = (
            request.POST.get('active_status') == 'on'
        )

        course.save()
        create_audit_log(
           request.user,
            "UPDATE",
            affected_object=f"Course {course.course_name}",
            description="Course updated",
            request=request
        )
        messages.success(
            request,
            'Course updated successfully.'
        )

        return redirect('course_list')

    return render(
        request,
        'students/course_form.html',
        {
            'course': course,
            'edit_mode': True,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def delete_course(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == 'POST':
        course_name = course.course_name

        create_audit_log(
    request.user,
    "DELETE",
    affected_object=f"Course {course_name}",
    description="Course deleted",
    request=request
)

        course.delete()

        messages.success(
            request,
            'Course deleted successfully.'
        )

        return redirect('course_list')

    return render(
        request,
        'students/course_confirm_delete.html',
        {
            'course': course,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def add_trainer(request):

    if request.method == 'POST':

        form = TrainerForm(request.POST)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user,
                role='trainer',
                is_approved=False
            )

            trainer_profile = TrainerProfile.objects.create(
                user=user
            )

            trainer_profile.courses.set(
                form.cleaned_data['courses']
            )

            create_audit_log(
    request.user,
    "CREATE",
    affected_object=f"Trainer {user.username}",
    description="Trainer account created",
    request=request
)

            messages.success(
                request,
                'Trainer created successfully.'
            )

            return redirect('trainer_list')

    else:
        form = TrainerForm()

    return render(
        request,
        'students/trainer_form.html',
        {
            'form': form,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def approve_trainer(request, trainer_id):

    trainer = get_object_or_404(
        UserProfile,
        id=trainer_id,
        role='trainer'
    )

    trainer.is_approved = True
    trainer.save()

    create_audit_log(
        request.user,
        "UPDATE",
        affected_object=f"Trainer {trainer.user.username}",
        description="Trainer account approved",
        request=request
    )

    messages.success(
        request,
        "Trainer approved successfully."
    )

    return redirect('trainer_list')

@login_required(login_url='login')
@role_required(['admin'])
def edit_trainer(request, pk):

    trainer_profile = get_object_or_404(
        TrainerProfile,
        pk=pk
    )

    user = trainer_profile.user

    if request.method == 'POST':

        form = TrainerEditForm(
            request.POST,
            instance=user
        )

        if form.is_valid():

            form.save()

            trainer_profile.courses.set(
                form.cleaned_data['courses']
            )

            create_audit_log(
               request.user,
               "UPDATE",
               affected_object=f"Trainer {user.username}",
               description="Trainer updated",
               request=request
           )

            messages.success(
                request,
                'Trainer updated successfully.'
            )

            return redirect('trainer_list')

    else:

        form = TrainerEditForm(
            instance=user
        )

        form.fields['courses'].initial = (
            trainer_profile.courses.all()
        )

    return render(
        request,
        'students/trainer_form.html',
        {
            'form': form,
            'trainer': trainer_profile,
            'edit_mode': True,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def delete_trainer(request, pk):

    trainer_profile = get_object_or_404(
        TrainerProfile,
        pk=pk
    )

    user = trainer_profile.user

    if request.method == 'POST':

        username = user.username

        create_audit_log(
    request.user,
    "DELETE",
    affected_object=f"Trainer {username}",
    description="Trainer deleted",
    request=request
)

        user.delete()

        messages.success(
            request,
            'Trainer deleted successfully.'
        )

        return redirect('trainer_list')

    return render(
        request,
        'students/trainer_confirm_delete.html',
        {
            'trainer': trainer_profile,
        }
    )


@login_required(login_url='login')
@role_required(['admin'])
def user_list(request):

    users = User.objects.select_related(
        'profile'
    ).all().order_by('-date_joined')

    paginator = Paginator(users, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'students/user_list.html',
        {
            'users': page_obj,
            'page_obj': page_obj,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def audit_log_list(request):

    logs = AuditLog.objects.select_related(
        'user'
    ).order_by('-created_at')

    # Search
    search = request.GET.get('search', '').strip()

    if search:
        logs = logs.filter(
            Q(description__icontains=search) |
            Q(affected_object__icontains=search) |
            Q(user__username__icontains=search)
        )

    # Action filter
    action = request.GET.get('action', '').strip()

    if action:
        logs = logs.filter(action=action)

    # Date range
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    if start_date:
        logs = logs.filter(
            created_at__date__gte=start_date
        )

    if end_date:
        logs = logs.filter(
            created_at__date__lte=end_date
        )

    # Pagination
    paginator = Paginator(logs, 15)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'students/audit_log_list.html',
        {
            'logs': page_obj,
            'page_obj': page_obj,
            'search': search,
            'action': action,
            'start_date': start_date,
            'end_date': end_date,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def toggle_user_status(request, user_id):

    user = get_object_or_404(User, id=user_id)

    # Admin apna account deactivate nahi kar sakta
    if user == request.user:
        messages.error(
            request,
            "You cannot deactivate your own account."
        )
        return redirect('user_list')

    # Toggle account status
    user.is_active = not user.is_active
    user.save()

    # Account status audit log
    if user.is_active:

        create_audit_log(
            request.user,
            "UPDATE",
            affected_object=f"User {user.username}",
            description="User account activated",
            request=request
        )

        messages.success(
            request,
            f"{user.username} activated successfully."
        )

    else:

        create_audit_log(
            request.user,
            "UPDATE",
            affected_object=f"User {user.username}",
            description="User account deactivated",
            request=request
        )

        messages.warning(
            request,
            f"{user.username} deactivated successfully."
        )

    return redirect('user_list')

@login_required(login_url='login')
@role_required(['admin'])
def add_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_user')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            role=role
        )
        create_audit_log(
    request.user,
    "CREATE",
    affected_object=f"User {user.username}",
    description="User account created",
    request=request
   )

        messages.success(request, 'User created successfully.')
        return redirect('user_list')

    return render(request, 'students/user_form.html')

@login_required(login_url='login')
@role_required(['admin'])
def edit_user(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.email = request.POST.get('email')
        role = request.POST.get('role')
        student_id = request.POST.get('student')

        user.save()

        profile = get_object_or_404(UserProfile, user=user)
        profile.role = role

        if role == 'student' and student_id:
            profile.student_id = student_id
            profile.is_approved = True
        else:
            profile.student = None

        profile.save()

        create_audit_log(
            request.user,
            "UPDATE",
            affected_object=f"User {user.username}",
            description="User account updated",
            request=request
        )

        messages.success(request, 'User updated successfully.')
        return redirect('user_list')

    return render(
        request,
        'students/user_edit.html',
        {
            'user': user,
            'students': Student.objects.all(),
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def delete_user(request, pk):

    user = get_object_or_404(User, pk=pk)

    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('user_list')

    if request.method == 'POST':
        username = user.username

        create_audit_log(
    request.user,
    "DELETE",
    affected_object=f"User {username}",
    description="User account deleted",
    request=request
 )

        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')

    return render(
        request,
        'students/user_confirm_delete.html',
        {
            'user': user,
        }
    )

@login_required(login_url='login')
@role_required(['admin'])
def unlock_user(request, pk):

    user = get_object_or_404(User, pk=pk)

    profile = get_object_or_404(UserProfile, user=user)

    profile.failed_login_attempts = 0
    profile.save()

    create_audit_log(
        request.user,
        "UNLOCK",
        affected_object=f"User {user.username}",
        description="User account unlocked by admin",
        request=request
    )

    messages.success(
        request,
        f'Account for {user.username} has been unlocked successfully.'
    )

    return redirect('user_list')