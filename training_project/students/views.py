from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import Student, Department, Course, StudentProfile, UserProfile, AuditLog
from .form import StudentForm, StudentProfileForm
from .decorator import role_required
from .utility import create_audit_log, ensure_profile_and_student



# home page

def home(request):
    return render(request, 'home.html')


# register page

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not full_name or not email:
            messages.error(request, "Username, full name and email are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists() or Student.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('register')

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )

                UserProfile.objects.create(user=new_user, role="STUDENT")

                student = Student.objects.create(
                    user=new_user,
                    name=full_name,
                    email=email,
                    marks=0,
                    join_date=timezone.now().date(),
                    active_status="fail",
                )

                StudentProfile.objects.create(student=student)

                create_audit_log(
                    request=request,
                    user=new_user,
                    action="CREATE",
                    object_name=new_user.username,
                    description=f"New self-registration for {new_user.username}",
                )
        except IntegrityError:
            messages.error(request, "Could not create account. Please try again.")
            return redirect('register')

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

    return render(request, "register.html")



# login page

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        db_user = User.objects.filter(username=username).first()

        # Check account lock before authenticating locked to nhi he 
        if db_user:
            profile = ensure_profile_and_student(db_user)

            if profile.locked_until and profile.locked_until > timezone.now():
                messages.error(
                    request,
                    "Your account is locked. Please try again after 10 minutes."
                )
                return redirect("login")

        user = authenticate(request, username=username, password=password)

        # Successful login
        if user:
            if not user.is_active:
                messages.error(request, "Your account has been deactivated. Contact admin.")
                return redirect("login")

            profile = ensure_profile_and_student(user)
            profile.failed_attempts = 0
            profile.locked_until = None
            profile.save()

            login(request, user)

            create_audit_log(
                request=request,
                user=user,
                action="LOGIN",
                description=f"{user.username} logged in successfully"
            )

            messages.success(request, "Login successful.")

            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)

            if profile.role == "ADMIN":
                return redirect("admin_dashboard")
            elif profile.role == "TRAINER":
                return redirect("trainer_dashboard")
            elif profile.role == "STUDENT":
                return redirect("dashboard")

            return redirect("home")

        # Failed login
        else:
            if db_user:
                profile = ensure_profile_and_student(db_user)
                profile.failed_attempts += 1

                if profile.failed_attempts >= 5:
                    profile.locked_until = timezone.now() + timedelta(minutes=10)

                profile.save()

                create_audit_log(
                    request=request,
                    user=db_user,
                    action="FAILED_LOGIN",
                    description=f"Login failed for {db_user.username}"
                )

            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")



# logout

@login_required
def logout_user(request):
    create_audit_log(
        request=request,
        user=request.user,
        action="LOGOUT",
        description=f"{request.user.username} logged out")
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('home')



# admin dashboard

@login_required()
@role_required("ADMIN")
def admin_dashboard(request):
    # no of students
    students = Student.objects.filter(
    user__profile__role="STUDENT"
    ).count()
    # no of courses
    courses = Course.objects.count()
    # no of department
    dept = Department.objects.count()
    # no of trainer
    trainers = UserProfile.objects.filter(role='TRAINER').count()
    # highest marks
    highest = Student.objects.order_by('-marks').first()
    # recent joined students
    recent = Student.objects.filter(
    user__profile__role="STUDENT"
    ).order_by("-join_date")[:5]

    context = {
        "students": students,
        "courses": courses,
        "dept": dept,
        "trainers": trainers,
        "highest": highest,
        "recent": recent,
    }
    return render(request, 'admin-dashboard.html', context)


# trainer dashboard 

@role_required("TRAINER")
def trainer_dashboard(request):
    trainer = request.user.profile

    courses = Course.objects.filter(
        assigned_trainer__trainer=trainer).distinct()
    
    students = Student.objects.filter(
        course__assigned_trainer__trainer=trainer
    ).select_related(
        "department"
    ).prefetch_related(
        "course").distinct()

    context = {
        "students": students,
        "courses": courses,
        "total_students": students.count(),
        "total_course": courses.count(),
    }
    return render(request, 'trainer-dashboard.html', context)


# student dashboard - a student only ever sees their own data

@login_required()
@role_required("STUDENT")
def dashboard(request):
    student = getattr(request.user, "student", None)

    if student is None:
        messages.error(
            request,
            "Your student profile is incomplete. Please contact the admin."
        )
        return redirect('home')

    context = {
        "student": student
    }
    return render(request, 'dashboard.html', context)



# student list - full directory, ADMIN only.
@role_required("ADMIN")
def student_list(request):

    # students = Student.objects.select_related("department", "profile").prefetch_related("course")

    students = Student.objects.filter(
        Q(user__isnull=True) | Q(user__profile__role="STUDENT")
    ).select_related("department", "profile").prefetch_related("course")

    context = {
        "students": students
    }
    return render(request, "student_list.html", context)



# one student detail 
@login_required
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    profile = getattr(request.user, "profile", None)
    role = profile.role if profile else None

    if role == "ADMIN":
        pass

    elif role == "TRAINER":
        is_assigned = Course.objects.filter(
            assigned_trainer__trainer=profile,
            students=student,
        ).exists()
        if not is_assigned:
            return HttpResponseForbidden("403 Forbidden: This student is not assigned to you.")

    elif role == "STUDENT":
        own_student = getattr(request.user, "student", None)
        if own_student is None or own_student != student:
            return HttpResponseForbidden("403 Forbidden: You can only view your own profile.")

    else:
        return HttpResponseForbidden("403 Forbidden")

    context = {
        "student": student,
        "can_manage": role == "ADMIN",
    }
    return render(request, "student_detail.html", context)


# add student - ADMIN only.

@role_required("ADMIN")
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        profile_form = StudentProfileForm(request.POST)

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        account_errors = []

        if not username:
            account_errors.append("Username is required.")
        elif User.objects.filter(username=username).exists():
            account_errors.append("This username is already taken.")

        if not password or password != confirm_password:
            account_errors.append("Passwords must be provided and match.")
        else:
            try:
                validate_password(password)
            except ValidationError as e:
                account_errors.extend(e.messages)

        if form.is_valid() and profile_form.is_valid() and not account_errors:
            try:
                with transaction.atomic():
                    new_user = User.objects.create_user(
                        username=username,
                        email=form.cleaned_data.get('email'),
                        password=password,
                    )
                    UserProfile.objects.create(user=new_user, role="STUDENT")

                    student = form.save(commit=False)
                    student.user = new_user
                    student.active_status = 'pass' if student.marks >= 40 else "fail"
                    student.save()
                    form.save_m2m()

                    profile = profile_form.save(commit=False)
                    profile.student = student
                    profile.save()

                    create_audit_log(
                        request=request,
                        user=request.user,
                        action="CREATE",
                        object_name=student.name,
                        description=f"Created student: {student.name} (account: {username})"
                    )
            except IntegrityError:
                messages.error(request, "Could not create student account. Please check the details and try again.")
                context = {"form": form,
                            "profile_form": profile_form,
                            "account_errors": account_errors
                        }
                return render(request, "student_form.html", context)

            messages.success(request, "Student added successfully.")
            return redirect("student_list")
        else:
            for err in account_errors:
                messages.error(request, err)
    else:
        form = StudentForm()
        profile_form = StudentProfileForm()
        account_errors = []

    context = {
        "form": form,
        "profile_form": profile_form,
        "account_errors": account_errors,
    }

    return render(request, "student_form.html", context)



# edit or update student 

@role_required("ADMIN")
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    profile, created = StudentProfile.objects.get_or_create(student=student)

    if created:
        print("Naya student profile banaya gaya!")
    else:
        print("Purana student profile pehle se tha, wahi fetch kiya gaya.")
    if request.method == "POST":

        form = StudentForm(request.POST, instance=student)
        profile_form = StudentProfileForm(request.POST, instance=profile)

        if form.is_valid() and profile_form.is_valid():

            student = form.save(commit=False)
            student.active_status = 'pass' if student.marks >= 40 else "fail"
            student.save()
            form.save_m2m()
            profile_form.save()

            create_audit_log(
                request=request,
                user=request.user,
                action="UPDATE",
                object_name=student.name,
                description=f"Updated student: {student.name}"
            )

            messages.success(request, "Student updated successfully.")

            return redirect("student_list")

    else:
        form = StudentForm(instance=student)
        profile_form = StudentProfileForm(instance=profile)

    context = {
        "form": form,
        "profile_form": profile_form,
    }

    return render(request, "student_form.html", context)



# delete student 
@role_required("ADMIN")
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student_name = student.name
        linked_user = student.user

        if linked_user:
            linked_user.delete()  # cascades to Student, StudentProfile, UserProfile
        else:
            student.delete()

        create_audit_log(
            request=request,
            user=request.user,
            action="DELETE",
            object_name=student_name,
            description=f"Deleted student {student_name}"
        )

        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")

    context = {
        "student": student
    }
    return render(request, "student_confirm_delete.html", context)



# change password 
@login_required
def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully")

            create_audit_log(
                request=request,
                user=user,
                action="UPDATE",
                object_name=user.username,
                description=f"{user.username} changed their password",
            )

            profile = getattr(user, "profile", None)
            role = profile.role if profile else None

            if role == "ADMIN":
                return redirect('admin_dashboard')
            elif role == "TRAINER":
                return redirect('trainer_dashboard')
            elif role == "STUDENT":
                return redirect('dashboard')
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = PasswordChangeForm(request.user)

    context = {
        "form": form
    }
    return render(request, 'change_password.html', context)



# user management 

@role_required("ADMIN")
def user_list(request):
    users = User.objects.select_related("profile").all()
    context = {
        "users": users
    }
    return render(request, 'user_list.html', context)


@role_required("ADMIN")
def toggle_status(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot activate/deactivate your own account.")
        return redirect('user_list')

    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        create_audit_log(
            request=request,
            user=request.user,
            action="ACTIVATE",
            object_name=user.username,
            description=f"Activated user {user.username}"
        )
    else:
        create_audit_log(
            request=request,
            user=request.user,
            action="DEACTIVATE",
            object_name=user.username,
            description=f"Deactivated user {user.username}"
        )

    return redirect('user_list')


@role_required("ADMIN")
def make_trainer(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot change your own role.")
        return redirect('user_list')

    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={"role": "STUDENT"})
    profile.role = "TRAINER"
    profile.save()

    create_audit_log(
        request=request,
        user=request.user,
        action="UPDATE",
        object_name=user.username,
        description=f"Made {user.username} a TRAINER"
    )

    messages.success(request, f"{user.username} is now a trainer.")
    return redirect('user_list')


@role_required("ADMIN")
def remove_trainer(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot change your own role.")
        return redirect('user_list')

    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={"role": "STUDENT"})
    profile.role = "STUDENT"
    profile.save()

    create_audit_log(
        request=request,
        user=request.user,
        action="UPDATE",
        object_name=user.username,
        description=f"Removed trainer role from {user.username}"
    )

    messages.success(request, f"{user.username} is no longer a trainer.")
    return redirect('user_list')



# audit log 

@role_required("ADMIN")
def audit_list(request):
    logs = AuditLog.objects.all().order_by('-created_at')
    search = request.GET.get("search")
    action = request.GET.get("action")

    if search:
        logs = logs.filter(
            Q(user__username__icontains=search) |
            Q(action__icontains=search) |
            Q(object_name__icontains=search)
        )

    if action:
        logs = logs.filter(action=action)

    paginator = Paginator(logs, 5)
    page_number = request.GET.get("page")
    logs = paginator.get_page(page_number)

    context = {
        "logs": logs,
        "search": search,
    }
    return render(request, 'audit_list.html', context)



# to check custom error pages
def forbidden(request):
    raise PermissionDenied


def server_error(request):
    x = 10 / 0
