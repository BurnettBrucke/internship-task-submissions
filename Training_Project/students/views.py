from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import StudentForm, TrainerStudentForm, TrainerForm
from .models import (
    Student,
    Department,
    Course,
    UserProfile,
    AuditLog,
)


# ============================================================
# COMMON / HELPER FUNCTIONS
# ============================================================

def create_audit_log(request, action, description, user=None):
    """
    Create an audit log entry for important user actions.
    """

    if user is None:
        user = request.user if request.user.is_authenticated else None

    AuditLog.objects.create(
        user=user,
        action=action,
        description=description
    )


def role_required(*roles):
    """
    Custom decorator for role-based access control.

    Example:
        @role_required('admin')
        @role_required('trainer')
        @role_required('admin', 'trainer')
    """

    def decorator(view_func):

        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):

            # User must have a UserProfile
            if not hasattr(request.user, 'profile'):
                raise PermissionDenied

            # Check whether user's role is allowed
            if request.user.profile.role not in roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# ============================================================
# PUBLIC PAGES
# ============================================================

def home(request):
    """
    Home page.
    """

    company_name = "Bug Network Private Limited"

    return render(
        request,
        'home.html',
        {
            'company_name': company_name
        }
    )


def about(request):
    """
    About page.
    """

    return render(
        request,
        'about.html'
    )


# ============================================================
# AUTHENTICATION
# ============================================================

def register_user(request):
    """User registration."""

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Get selected role from registration form
            selected_role = form.cleaned_data['role']

            # Create UserProfile with selected role
            UserProfile.objects.create(
                user=user,
                role=selected_role
            )

            # Automatically link existing Student record by email
            if selected_role == 'student':
                student = Student.objects.filter(
                    email__iexact=user.email
                ).first()

                if student:
                    student.user = user
                    student.save()

            create_audit_log(
                request,
                "User Registration",
                f"New {selected_role} user {user.username} registered successfully.",
                user=user
            )

            messages.success(
                request,
                "Registration successful. You can now login."
            )

            return redirect('login')

    else:
        form = RegistrationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )

# ============================================================
# USER LOGIN
# ============================================================

def login_user(request):
    """
    User login with failed login attempt handling.
    """

    # Get failed login attempts from session
    failed_attempts = request.session.get(
        'failed_login_attempts',
        0
    )

    # Block login after 5 failed attempts
    if failed_attempts >= 5:

        messages.error(
            request,
            "Too many failed login attempts. "
            "Login is temporarily blocked for this session."
        )

        form = AuthenticationForm(request)

        form.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })

        form.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

        return render(
            request,
            'login.html',
            {
                'form': form
            }
        )

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        form.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })

        form.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                # Trainer approval check
                if (
                    hasattr(user, 'profile')
                    and user.profile.role == 'trainer'
                ):

                    if not user.profile.is_approved:

                        messages.error(
                            request,
                            "Your trainer account is pending admin approval."
                        )

                        return redirect('login')

                # Successful login → reset failed attempts
                request.session['failed_login_attempts'] = 0

                login(
                    request,
                    user
                )

                create_audit_log(
                    request,
                    "User Login",
                    f"User {user.username} logged in successfully."
                )

                messages.success(
                    request,
                    "Login successful!"
                )

                return redirect('dashboard')

            else:

                # Increase failed login attempts
                failed_attempts += 1

                request.session['failed_login_attempts'] = failed_attempts

                # Create audit log for failed login
                create_audit_log(
                    request,
                    "Failed Login",
                    f"Failed login attempt for username: {username}. "
                    f"Attempt {failed_attempts} of 5.",
                    user=None
                )

                if failed_attempts >= 5:

                    messages.error(
                        request,
                        "Too many failed login attempts. "
                        "Login is now blocked for this session."
                    )

                else:

                    remaining_attempts = 5 - failed_attempts

                    messages.error(
                        request,
                        f"Invalid username or password. "
                        f"{remaining_attempts} attempt(s) remaining."
                    )

        else:

            # ====================================================
            # CHECK FOR DEACTIVATED ACCOUNT
            # ====================================================

            username = request.POST.get(
                'username',
                ''
            ).strip()

            password = request.POST.get(
                'password',
                ''
            )

            # Find the user account
            inactive_user = User.objects.filter(
                username=username
            ).first()

            # Check if account is deactivated
            # and password is correct
            if (
                inactive_user
                and not inactive_user.is_active
                and inactive_user.check_password(password)
            ):

                create_audit_log(
                    request,
                    "Inactive Account Login Attempt",
                    f"Deactivated user {username} attempted to login.",
                    user=inactive_user
                )

                messages.error(
                    request,
                    "Your account has been deactivated by the administrator. "
                    "Please contact the administrator."
                )

                # Remove default authentication error
                # while preserving entered form values
                form.errors.clear()

                return render(
                    request,
                    'login.html',
                    {
                        'form': form
                    }
                )

            # ====================================================
            # NORMAL FAILED LOGIN ATTEMPT
            # ====================================================

            failed_attempts += 1

            request.session['failed_login_attempts'] = failed_attempts

            create_audit_log(
                request,
                "Failed Login",
                "Login form validation failed.",
                user=None
            )

            if failed_attempts >= 5:

                messages.error(
                    request,
                    "Too many failed login attempts. "
                    "Login is now blocked for this session."
                )

            else:

                remaining_attempts = 5 - failed_attempts

                messages.error(
                    request,
                    f"Invalid login details. "
                    f"{remaining_attempts} attempt(s) remaining."
                )

    else:

        form = AuthenticationForm()

        form.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })

        form.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

    return render(
        request,
        'login.html',
        {
            'form': form
        }
    )

# ============================================================
# LOGOUT
# ============================================================


def logout_user(request):
    """
    Logout user and create audit log.
    """

    if request.user.is_authenticated:

        create_audit_log(
            request,
            "User Logout",
            f"User {request.user.username} logged out successfully."
        )

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully!"
    )

    return redirect('login')


# ============================================================
# MAIN DASHBOARD REDIRECTION
# ============================================================

@login_required
def dashboard(request):
    """
    Redirect logged-in users to their role-specific dashboard.
    """

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    role = request.user.profile.role

    if role == 'admin':
        return redirect('admin_dashboard')

    elif role == 'trainer':
        return redirect('trainer_dashboard')

    elif role == 'student':
        return redirect('student_dashboard')

    raise PermissionDenied


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@role_required('admin')
def admin_dashboard(request):
    """
    Admin dashboard.

    Shows:
    - Total students
    - Active students
    - Departments
    - Courses
    - Total Trainers
    - Average marks
    - Highest-scoring student
    - Recent students

    Trainer information is managed separately
    on the Trainers page.
    """

    # --------------------------------------------------------
    # Student statistics
    # --------------------------------------------------------

    total_students = Student.objects.count()

    total_active_students = Student.objects.filter(
        active=True
    ).count()

    # --------------------------------------------------------
    # Department and course statistics
    # --------------------------------------------------------

    total_departments = Department.objects.count()

    total_courses = Course.objects.count()

    total_trainers = User.objects.filter(
        profile__role='trainer'
    ).count()

    # --------------------------------------------------------
    # Marks statistics
    # --------------------------------------------------------

    average_marks = Student.objects.aggregate(
        average=Avg('marks')
    )['average']

    highest_student = Student.objects.order_by(
        '-marks'
    ).first()

    # --------------------------------------------------------
    # Recent students
    # --------------------------------------------------------

    recent_students = Student.objects.order_by(
        '-joined_date'
    )[:5]

    return render(
        request,
        'admin_dashboard.html',
        {
            'total_students': total_students,
            'total_active_students': total_active_students,
            'total_departments': total_departments,
            'total_courses': total_courses,
            'total_trainers': total_trainers,
            'average_marks': average_marks,
            'highest_student': highest_student,
            'recent_students': recent_students,
        }
    )


# ============================================================
# TRAINER DASHBOARD
# ============================================================

@role_required('trainer')
def trainer_dashboard(request):
    """
    Trainer dashboard.

    Shows courses assigned to the logged-in trainer
    and students belonging to those courses.
    """

    assigned_courses = Course.objects.filter(
        trainer=request.user
    )

    assigned_students = Student.objects.filter(
        courses__trainer=request.user
    ).distinct()

    return render(
        request,
        'trainer_dashboard.html',
        {
            'assigned_courses': assigned_courses,
            'assigned_students': assigned_students,
        }
    )


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@role_required('student')
def student_dashboard(request):
    """
    Student dashboard.

    Shows student's own information,
    active courses and profile completion.
    """

    try:

        student = Student.objects.get(
            user=request.user
        )

    except Student.DoesNotExist:

        student = None

    if student:

        courses = student.courses.filter(
            active=True
        )

        performance_percentage = student.marks

        if hasattr(student, 'profile'):

            profile = student.profile

            completed_fields = 0

            if student.name:
                completed_fields += 1

            if student.email:
                completed_fields += 1

            if student.age:
                completed_fields += 1

            if student.course:
                completed_fields += 1

            if profile.phone:
                completed_fields += 1

            if profile.address:
                completed_fields += 1

            if profile.date_of_birth:
                completed_fields += 1

            profile_completion = int(
                (completed_fields / 7) * 100
            )

        else:

            profile_completion = 57

    else:

        courses = Course.objects.none()

        performance_percentage = 0

        profile_completion = 0

    return render(
        request,
        'student_dashboard.html',
        {
            'student': student,
            'courses': courses,
            'performance_percentage': performance_percentage,
            'profile_completion': profile_completion,
        }
    )


# ============================================================
# STUDENT LIST
# ============================================================

@login_required
def student_list(request):
    """
    Display students according to logged-in user's role.

    Admin:
        Can see all students.

    Trainer:
        Can see students assigned to trainer's courses.

    Student:
        Can see only their own record.
    """

    if not hasattr(request.user, 'profile'):
        raise PermissionDenied

    role = request.user.profile.role

    # --------------------------------------------------------
    # Base queryset according to role
    # --------------------------------------------------------

    if role == 'admin':

        students = Student.objects.annotate(
            course_count=Count('courses')
        )

    elif role == 'trainer':

        students = Student.objects.filter(
            courses__trainer=request.user
        ).annotate(
            course_count=Count('courses')
        ).distinct()

    elif role == 'student':

        students = Student.objects.filter(
            user=request.user
        ).annotate(
            course_count=Count('courses')
        )

    else:

        raise PermissionDenied

    # ========================================================
    # SEARCH
    # ========================================================

    search = request.GET.get(
        'search',
        ''
    )

    if search:

        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(courses__course_name__icontains=search)
        ).distinct()

    # ========================================================
    # DEPARTMENT FILTER
    # ========================================================

    department_id = request.GET.get(
        'department',
        ''
    )

    if department_id:

        students = students.filter(
            department_id=department_id
        )

    # ========================================================
    # COURSE FILTER
    # ========================================================

    course_id = request.GET.get(
        'course',
        ''
    )

    if course_id:

        students = students.filter(
            courses__id=course_id
        ).distinct()

    # ========================================================
    # ACTIVE / INACTIVE FILTER
    # ========================================================

    status = request.GET.get(
        'status',
        ''
    )

    if status == 'active':

        students = students.filter(
            active=True
        )

    elif status == 'inactive':

        students = students.filter(
            active=False
        )

    # ========================================================
    # PASS / FAIL FILTER
    # ========================================================

    result = request.GET.get(
        'result',
        ''
    )

    if result == 'pass':

        students = students.filter(
            marks__gte=40
        )

    elif result == 'fail':

        students = students.filter(
            marks__lt=40
        )

    # ========================================================
    # FILTER OPTIONS
    # ========================================================

    departments = Department.objects.all()

    courses = Course.objects.all()

    # ========================================================
    # TOTAL STUDENT COUNTS
    # ========================================================

    if role == 'admin':

        total_students = Student.objects.count()

        active_students = Student.objects.filter(
            active=True
        ).count()

    elif role == 'trainer':

        total_students = Student.objects.filter(
            courses__trainer=request.user
        ).distinct().count()

        active_students = Student.objects.filter(
            courses__trainer=request.user,
            active=True
        ).distinct().count()

    else:

        total_students = Student.objects.filter(
            user=request.user
        ).count()

        active_students = Student.objects.filter(
            user=request.user,
            active=True
        ).count()

    # ========================================================
    # ORDERING
    # ========================================================

    students = students.order_by('id')

    # ========================================================
    # PAGINATION
    # ========================================================

    paginator = Paginator(
        students,
        5
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    # ========================================================
    # RENDER
    # ========================================================

    return render(
        request,
        'student_list.html',
        {
            'students': page_obj,
            'page_obj': page_obj,

            'total_students': total_students,
            'active_students': active_students,

            'departments': departments,
            'courses': courses,

            'search': search,
            'department_id': department_id,
            'course_id': course_id,
            'status': status,
            'result': result,
        }
    )


# ============================================================
# STUDENT DETAIL
# ============================================================

@login_required
def student_detail(request, id):
    """
    Display student details according to role.

    Admin:
        Can view any student.

    Trainer:
        Can view only students assigned to trainer's courses.

    Student:
        Can view only their own record.
    """

    student = get_object_or_404(
        Student,
        id=id
    )

    role = request.user.profile.role

    # --------------------------------------------------------
    # Student ownership check
    # --------------------------------------------------------

    if role == 'student':

        if student.user != request.user:
            raise PermissionDenied

    # --------------------------------------------------------
    # Trainer ownership check
    # --------------------------------------------------------

    elif role == 'trainer':

        if not student.courses.filter(
            trainer=request.user
        ).exists():
            raise PermissionDenied

    # --------------------------------------------------------
    # Only Admin / Trainer / Student allowed
    # --------------------------------------------------------

    elif role != 'admin':

        raise PermissionDenied

    return render(
        request,
        'student_detail.html',
        {
            'student': student
        }
    )


# ============================================================
# ADD STUDENT
# ============================================================

@role_required('admin')
def add_student(request):
    """
    Admin can add a new student.

    Student creation is restricted to Admin.
    """

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()

            # ------------------------------------------------
            # Optional Department assignment
            # ------------------------------------------------

            department_id = request.POST.get(
                'department'
            )

            if department_id:

                department = get_object_or_404(
                    Department,
                    id=department_id
                )

                student.department = department
                student.save()

            # ------------------------------------------------
            # Course assignment
            #
            # Supports multiple course IDs if the form
            # provides a field named "courses".
            # ------------------------------------------------

            course_ids = request.POST.getlist(
                'courses'
            )

            if course_ids:

                selected_courses = Course.objects.filter(
                    id__in=course_ids
                )

                student.courses.set(
                    selected_courses
                )

            # ------------------------------------------------
            # Audit log
            # ------------------------------------------------

            create_audit_log(
                request,
                "Student Added",
                f"Student {student.name} was added successfully."
            )

            messages.success(
                request,
                "Student added successfully!"
            )

            return redirect(
                'student_list'
            )

    else:

        form = StudentForm()

    departments = Department.objects.all()

    courses = Course.objects.all()

    return render(
        request,
        'student_form.html',
        {
            'form': form,
            'departments': departments,
            'courses': courses,
            'title': 'Add Student',
        }
    )


# ============================================================
# EDIT STUDENT
# ============================================================

@role_required('admin')
def edit_student(request, id):
    """
    Admin can edit an existing student.

    Admin can update:
    - Student information
    - Department
    - Multiple courses
    """

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            student = form.save()

            # ------------------------------------------------
            # Department assignment
            # ------------------------------------------------

            department_id = request.POST.get(
                'department'
            )

            if department_id:

                department = get_object_or_404(
                    Department,
                    id=department_id
                )

                student.department = department

            else:

                student.department = None

            student.save()

            # ------------------------------------------------
            # Course assignment
            # ------------------------------------------------

            course_ids = request.POST.getlist(
                'courses'
            )

            if course_ids:

                selected_courses = Course.objects.filter(
                    id__in=course_ids
                )

                student.courses.set(
                    selected_courses
                )

            else:

                student.courses.clear()

            # ------------------------------------------------
            # Audit log
            # ------------------------------------------------

            create_audit_log(
                request,
                "Student Updated",
                f"Student {student.name} was updated successfully."
            )

            messages.success(
                request,
                "Student updated successfully!"
            )

            return redirect(
                'student_detail',
                id=student.id
            )

    else:

        form = StudentForm(
            instance=student
        )

    departments = Department.objects.all()

    courses = Course.objects.all()

    selected_courses = student.courses.all()

    return render(
        request,
        'student_form.html',
        {
            'form': form,
            'student': student,
            'departments': departments,
            'courses': courses,
            'selected_courses': selected_courses,
            'title': 'Edit Student',
        }
    )


# ============================================================
# DELETE STUDENT
# ============================================================

@role_required('admin')
def delete_student(request, id):
    """
    Admin can delete a student.

    Confirmation page is displayed before deletion.
    """

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == 'POST':

        student_name = student.name

        student.delete()

        create_audit_log(
            request,
            "Student Deleted",
            f"Student {student_name} was deleted successfully."
        )

        messages.success(
            request,
            "Student deleted successfully!"
        )

        return redirect(
            'student_list'
        )

    return render(
        request,
        'student_confirm_delete.html',
        {
            'student': student
        }
    )


# ============================================================
# TRAINER - UPDATE STUDENT
# ============================================================

@role_required('trainer')
def trainer_update_student(request, id):
    """
    Trainer can update only:
    - Marks
    - Feedback

    Trainer can update a student only when that
    student is assigned to one of the trainer's courses.
    """

    student = get_object_or_404(
        Student,
        id=id
    )

    # --------------------------------------------------------
    # Ownership check
    # --------------------------------------------------------

    if not student.courses.filter(
        trainer=request.user
    ).exists():

        raise PermissionDenied

    if request.method == 'POST':

        form = TrainerStudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            student = form.save()

            create_audit_log(
                request,
                "Student Marks/Feedback Updated",
                (
                    f"Trainer {request.user.username} updated "
                    f"marks/feedback for student {student.name}."
                )
            )

            messages.success(
                request,
                "Student marks and feedback updated successfully!"
            )

            return redirect(
                'student_detail',
                id=student.id
            )

    else:

        form = TrainerStudentForm(
            instance=student
        )

    return render(
        request,
        'trainer_student_form.html',
        {
            'form': form,
            'student': student,
        }
    )


# ============================================================
# TRAINER MANAGEMENT
# ============================================================


# ============================================================
# TRAINER LIST
# ============================================================

@role_required('admin')
def trainer_list(request):
    """
    Display all trainers.

    Only Admin can access this page.

    Shows:
    - Trainer name
    - Trainer email
    - Assigned courses
    """

    trainers = User.objects.filter(
        profile__role='trainer'
    ).prefetch_related(
        'assigned_courses'
    )

    total_trainers = trainers.count()
    total_courses = Course.objects.count()

    return render(
        request,
        'trainer_list.html',
        {
            'trainers': trainers,
            'total_trainers': total_trainers,
            'total_courses': total_courses,
        }
    )


# ============================================================
# TRAINER DETAIL
# ============================================================

@role_required('admin')
def trainer_detail(request, id):
    """
    Display complete information about one trainer.

    Only Admin can view trainer details.
    """

    trainer = get_object_or_404(
        User,
        id=id,
        profile__role='trainer'
    )

    assigned_courses = Course.objects.filter(
        trainer=trainer
    )

    return render(
        request,
        'trainer_detail.html',
        {
            'trainer': trainer,
            'assigned_courses': assigned_courses,
        }
    )

# ============================================================
# APPROVE TRAINER
# ============================================================

@role_required('admin')
def approve_trainer(request, id):
    """Admin can approve a pending trainer account."""

    trainer = get_object_or_404(
        User,
        id=id,
        profile__role='trainer'
    )

    trainer.profile.is_approved = True
    trainer.profile.save()

    create_audit_log(
        request,
        "Trainer Approved",
        f"Trainer {trainer.username} was approved successfully."
    )

    messages.success(
        request,
        f"Trainer {trainer.username} approved successfully!"
    )

    return redirect('trainer_detail', id=trainer.id)

# ============================================================
# ACTIVATE / DEACTIVATE TRAINER
# ============================================================

@role_required('admin')
def toggle_trainer_status(request, id):
    """Admin can activate or deactivate a trainer account."""

    trainer = get_object_or_404(
        User,
        id=id,
        profile__role='trainer'
    )

    trainer.is_active = not trainer.is_active
    trainer.save()

    if trainer.is_active:
        action = "Trainer Activated"
        message = f"Trainer {trainer.username} activated successfully!"
    else:
        action = "Trainer Deactivated"
        message = f"Trainer {trainer.username} deactivated successfully!"

    create_audit_log(
        request,
        action,
        f"Trainer {trainer.username} account status changed."
    )

    messages.success(request, message)

    return redirect('trainer_detail', id=trainer.id)

# ============================================================
# ADD TRAINER
# ============================================================

@role_required('admin')
def add_trainer(request):

    """Admin can create a new Trainer account."""

    if request.method == 'POST':

        form = TrainerForm(request.POST)

        if form.is_valid():

            # Save trainer user
            trainer = form.save()

            # Create Trainer UserProfile
            UserProfile.objects.create(
                user=trainer,
                role='trainer'
            )

            # Get selected courses
            selected_courses = form.cleaned_data.get(
                'courses'
            )

            # Assign multiple courses to trainer
            if selected_courses:
                for course in selected_courses:
                    course.trainer.add(trainer)

            # Audit log
            create_audit_log(
                request,
                "Trainer Added",
                f"Trainer {trainer.username} was added successfully."
            )

            messages.success(
                request,
                "Trainer added successfully!"
            )

            return redirect(
                'trainer_list'
            )

    else:

        form = TrainerForm()

    return render(
        request,
        'trainer_form.html',
        {
            'form': form,
            'title': 'Add Trainer'
        }
    )


# ============================================================
# EDIT TRAINER
# ============================================================

@role_required('admin')
def edit_trainer(request, id):

    """Admin can edit an existing Trainer."""

    trainer = get_object_or_404(
        User,
        id=id,
        profile__role='trainer'
    )

    if request.method == 'POST':

        form = TrainerForm(
            request.POST,
            instance=trainer
        )

        if form.is_valid():

            trainer = form.save()

            # Remove this trainer from all previous course assignments
            for course in Course.objects.filter(trainer=trainer):
                course.trainer.remove(trainer)

            # Get newly selected courses
            selected_courses = form.cleaned_data.get('courses')

            # Assign selected courses to this trainer
            if selected_courses:
                for course in selected_courses:
                    course.trainer.add(trainer)

            # Audit log
            create_audit_log(
                request,
                "Trainer Updated",
                f"Trainer {trainer.username} was updated successfully."
            )

            messages.success(
                request,
                "Trainer updated successfully!"
            )

            return redirect(
                'trainer_detail',
                id=trainer.id
            )

    else:

        form = TrainerForm(
            instance=trainer
        )

    return render(
        request,
        'trainer_form.html',
        {
            'form': form,
            'title': 'Edit Trainer',
            'trainer': trainer
        }
    )


# ============================================================
# DELETE TRAINER
# ============================================================

@role_required('admin')
def delete_trainer(request, id):
    """
    Admin can delete a Trainer account.

    A confirmation page is displayed before deletion.
    """

    trainer = get_object_or_404(
        User,
        id=id,
        profile__role='trainer'
    )

    if request.method == 'POST':

        trainer_name = trainer.username

        # Course.trainer uses SET_NULL,
        # so assigned courses become unassigned.
        trainer.delete()

        # Audit log
        create_audit_log(
            request,
            "Trainer Deleted",
            f"Trainer {trainer_name} was deleted successfully."
        )

        messages.success(
            request,
            "Trainer deleted successfully!"
        )

        return redirect(
            'trainer_list'
        )

    return render(
        request,
        'trainer_confirm_delete.html',
        {
            'trainer': trainer
        }
    )


# ============================================================
# AUDIT LOGS
# ============================================================

@role_required('admin')
def audit_logs(request):
    """
    Display audit logs.

    Only Admin can access audit logs.
    """

    logs = AuditLog.objects.select_related(
        'user'
    ).order_by(
        '-timestamp'
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    search = request.GET.get(
        'search',
        ''
    )

    if search:

        logs = logs.filter(
            Q(action__icontains=search) |
            Q(description__icontains=search) |
            Q(user__username__icontains=search)
        )

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    paginator = Paginator(
        logs,
        10
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        'audit_logs.html',
        {
            'logs': page_obj,
            'page_obj': page_obj,
            'search': search,
        }
    )

# ============================================================
# CUSTOM 403 ERROR PAGE
# ============================================================

def custom_403(request, exception):
    """
    Custom 403 Forbidden error page.
    """

    return render(
        request,
        '403.html',
        status=403
    )