from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import StudentForm, TrainerStudentForm
from .models import Student, Department, Course, UserProfile, AuditLog

def create_audit_log(request, action, description, user=None):
    AuditLog.objects.create(
        user=user if user else request.user,
        action=action,
        description=description
    )

# =========================================================
# ROLE-BASED ACCESS CONTROL
# =========================================================

def role_required(*roles):
    """
    Allow access only to logged-in users
    having one of the given roles.
    """
    def decorator(view_func):

        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):

            if not hasattr(request.user, 'profile'):
                raise PermissionDenied

            if request.user.profile.role not in roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# =========================================================
# BASIC PAGES
# =========================================================

def home(request):
    company_name = "Bug Network Private Limited"

    return render(
        request,
        'home.html',
        {
            'company_name': company_name
        }
    )


def about(request):
    return render(request, 'about.html')


# =========================================================
# REGISTER
# =========================================================

def register_user(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            # Every newly registered user gets Student role
            UserProfile.objects.create(
                user=user,
                role='student'
            )

            user = form.save()

            create_audit_log(
                request,
                "User Registration",
                f"New user {user.username} registered successfully.",
                user=user
            )

            messages.success(
                request,
                'Registration successful. You can now login.'
            )

            return redirect('login')

    else:
        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# =========================================================
# LOGIN
# =========================================================

def login_user(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

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
        form = AuthenticationForm()

    return render(
        request,
        'login.html',
        {
            'form': form
        }
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_user(request):
    if request.user.is_authenticated:
        create_audit_log(
            request,
            "User Logout",
            f"User {request.user.username} logged out successfully."
        )

    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')


# =========================================================
# MAIN DASHBOARD ROUTER
# =========================================================

@login_required
def dashboard(request):

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


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@role_required('admin')
def admin_dashboard(request):

    total_students = Student.objects.count()

    total_active_students = Student.objects.filter(
        active=True
    ).count()

    total_departments = Department.objects.count()

    total_courses = Course.objects.count()

    average_marks = Student.objects.aggregate(
        average=Avg('marks')
    )['average']

    highest_student = Student.objects.order_by(
        '-marks'
    ).first()

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
            'average_marks': average_marks,
            'highest_student': highest_student,
            'recent_students': recent_students,
        }
    )


# =========================================================
# TRAINER DASHBOARD
# =========================================================

@role_required('trainer')
def trainer_dashboard(request):

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


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@role_required('student')
def student_dashboard(request):

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

        # Calculate profile completion
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


# =========================================================
# STUDENT LIST
# =========================================================

@login_required
def student_list(request):

    role = request.user.profile.role

    # -----------------------------------------
    # ADMIN → Can see all students
    # -----------------------------------------

    if role == 'admin':

        students = Student.objects.annotate(
            course_count=Count('courses')
        )

    # -----------------------------------------
    # TRAINER → Can see assigned students only
    # -----------------------------------------

    elif role == 'trainer':

        students = Student.objects.filter(
            courses__trainer=request.user
        ).annotate(
            course_count=Count('courses')
        ).distinct()

    # -----------------------------------------
    # STUDENT → Can see own record only
    # -----------------------------------------

    elif role == 'student':

        students = Student.objects.filter(
            user=request.user
        ).annotate(
            course_count=Count('courses')
        )

    else:
        raise PermissionDenied

    # =====================================================
    # SEARCH
    # =====================================================

    search = request.GET.get('search', '')

    if search:

        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(courses__course_name__icontains=search)
        ).distinct()

    # =====================================================
    # DEPARTMENT FILTER
    # =====================================================

    department_id = request.GET.get(
        'department',
        ''
    )

    if department_id:

        students = students.filter(
            department_id=department_id
        )

    # =====================================================
    # COURSE FILTER
    # =====================================================

    course_id = request.GET.get(
        'course',
        ''
    )

    if course_id:

        students = students.filter(
            courses__id=course_id
        ).distinct()

    # =====================================================
    # STATUS FILTER
    # =====================================================

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

    # =====================================================
    # RESULT FILTER
    # =====================================================

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

    # =====================================================
    # FILTER DATA
    # =====================================================

    departments = Department.objects.all()

    courses = Course.objects.all()

    # =====================================================
    # ROLE-BASED COUNTS
    # =====================================================

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


    students = students.order_by('id')

    # Pagination
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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


# =========================================================
# STUDENT DETAIL
# =========================================================

@login_required
def student_detail(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    role = request.user.profile.role

    # Admin can view any student
    if role == 'admin':
        pass

    # Trainer can view assigned students only
    elif role == 'trainer':

        if not student.courses.filter(
            trainer=request.user
        ).exists():

            raise PermissionDenied

    # Student can view own record only
    elif role == 'student':

        if student.user != request.user:

            raise PermissionDenied

    else:
        raise PermissionDenied

    return render(
        request,
        'student_detail.html',
        {
            'student': student
        }
    )


# =========================================================
# ADD STUDENT
# =========================================================

@role_required('admin')
def add_student(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save()

            create_audit_log(
                request,
                "Student Added",
                f"Student {student.name} was added."
            )

            messages.success(request, "Student added successfully!")
            return redirect('student_list')

    else:

        form = StudentForm()

    return render(
        request,
        'student_form.html',
        {
            'form': form,
            'title': 'Add Student'
        }
    )


# =========================================================
# EDIT STUDENT
# =========================================================

@role_required('admin')
def edit_student(request, id):

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

            create_audit_log(
                request,
                "Student Updated",
                f"Student {student.name} was updated successfully."
            )

            messages.success(request, "Student updated successfully!")

            return redirect(
                'student_detail',
                id=student.id
            )

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        'student_form.html',
        {
            'form': form,
            'title': 'Edit Student'
        }
    )

# =========================================================
# TRAINER UPDATE STUDENT
# =========================================================

@role_required('trainer')
def trainer_update_student(request, id):
    student = get_object_or_404(Student, id=id)

    # Trainer can update only students assigned to their courses
    if not student.courses.filter(trainer=request.user).exists():
        raise PermissionDenied

    if request.method == 'POST':
        form = TrainerStudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()

            create_audit_log(
                request,
                "Trainer Student Update",
                f"Trainer {request.user.username} updated marks and feedback for student {student.name}."
            )

            messages.success(request, "Marks and feedback updated successfully!")
            return redirect('student_detail', id=student.id)

    else:
        form = TrainerStudentForm(instance=student)

    return render(
        request,
        'trainer_student_form.html',
        {
            'form': form,
            'student': student,
        }
    )

# =========================================================
# DELETE STUDENT
# =========================================================

@role_required('admin')
def delete_student(request, id):

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

        messages.success(request, "Student deleted successfully!")

        return redirect('student_list')

    return render(
        request,
        'student_confirm_delete.html',
        {
            'student': student
        }
    )

@role_required('admin')
def audit_logs(request):
    logs = AuditLog.objects.select_related('user').order_by('-timestamp')

    paginator = Paginator(logs, 15)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'audit_logs.html',
        {
            'logs': page_obj,
            'page_obj': page_obj,
        }
    )

def custom_403(request, exception):
    return render(request, '403.html', status=403)