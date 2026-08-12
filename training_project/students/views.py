from django.contrib.auth.views import PasswordChangeView
from django.core.cache import cache
from django.core.paginator import Paginator
from .decorators import role_required
from django.shortcuts import get_object_or_404
# from django.db.models import Count

from django.shortcuts import render, redirect
from .forms import StudentForm, RegisterForm, FeedbackForm, MarksHistoryForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from .models import MarksHistory
from .forms import MarksHistoryForm


# Create your views here.

from django.db.models import Q
from .models import Student, Department, Course, UserProfile, AuditLog, StudentProfile
from .services import (
    get_dashboard_statistics,
    update_student_marks,
    create_feedback
)
from django.db.models import Avg


@login_required
def student_list(request):

    students = Student.objects.select_related(
        "department"
    ).prefetch_related(
        "courses"
    )
  

    search = request.GET.get("search")
    department = request.GET.get("department")
    active = request.GET.get("active")
    result = request.GET.get("result")
    course = request.GET.get("course")
    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(courses__course_name__icontains=search)
        ).distinct()

    if department:
        students = students.filter(department_id=department)
    if course:
        students = students.filter(courses__id=course)
    if active == "yes":
        students = students.filter(active=True)

    elif active == "no":
        students = students.filter(active=False)

    if result == "pass":
        students = students.filter(marks__gte=40)

    elif result == "fail":
        students = students.filter(marks__lt=40)

    context = {
        "students": students,
        "departments": Department.objects.all(),
        "courses": Course.objects.all(),
        "total_students": Student.objects.count(),
        "active_students": Student.objects.filter(active=True).count(),
    }  
    students = students.order_by("id")
    paginator = Paginator(students, 5)
    
    page_number = request.GET.get("page")
    
    students = paginator.get_page(page_number)
    context["students"] = students

    return render(request, "student_list.html", context)
@login_required
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()

            AuditLog.objects.create(    
                user=request.user,
                action="ADD_STUDENT",
                description=f"Added student: {student.name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )
            messages.success(request, "Student added successfully!")    
            return redirect("student_list")

    else:

        form = StudentForm()

    return render(request, "add_student.html", {"form": form})
@login_required
def student_detail(request, id):

    student = get_object_or_404(Student, id=id)

    if request.user.profile.role == "student":

        if student.user != request.user:
            return render(request, "403.html", status=403)

    return render(request, "student_detail.html", {
        "student": student
    })
@login_required
def edit_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.user.profile.role == "student":
        return render(request, "403.html", status=403)

    if request.method == "POST":

        form = StudentForm(request.POST, instance=student)

        if form.is_valid():

            student = form.save()

            AuditLog.objects.create(
                user=request.user,
                action="EDIT_STUDENT",
                description=f"Updated student: {student.name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )        

            messages.success(request, "Student Updated Successfully")

            return redirect("student_list")

    else:

        form = StudentForm(instance=student)

    return render(request, "student_form.html", {
        "form": form
    })
    
@login_required
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.user.profile.role != "admin":
        return render(request, "403.html", status=403)

    if request.method == "POST":
        AuditLog.objects.create(
            user=request.user,
            action="DELETE_STUDENT",
            description=f"Deleted student: {student.name}",
            ip_address=request.META.get("REMOTE_ADDR")
        )

        student.delete()

        messages.success(request, "Student Deleted Successfully")

        return redirect("student_list")

    return render(request, "student_confirm_delete.html", {
        "student": student
    })
    
def register_user(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                role="student"
            )

            department = Department.objects.first()

            if department is None:
                messages.error(
                    request,
                     "Please create at least one department first."
                )
                return redirect("register")

            Student.objects.create(
                user=user,
                department=department,
                name=user.username,
                email=user.email,
                age=18,
                course="Not Assigned",
                marks=0,
                active=True
            )

            login(request, user)

            messages.success(
                request,
                "Registration Successful"
            )

            return redirect("student_dashboard")
            

        

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})
      
def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")

        attempts = cache.get(f"login_attempts_{username}", 0)

        if attempts >= 5:
            messages.error(
                request,
                "Account temporarily locked. Too many failed login attempts. Try again after 5 minutes."
            )
            return redirect("login")

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                # Trainer approval check
                if (
                    user.profile.role == "trainer"
                    and not user.profile.is_approved
                ):
                    messages.error(
                        request,
                        "Your trainer account is waiting for administrator approval."
                    )
                    return redirect("login")

                # Reset failed attempts
                cache.delete(f"login_attempts_{username}")

                login(request, user)

                AuditLog.objects.create(
                    user=user,
                    action="LOGIN",
                    description="User logged in",
                    ip_address=request.META.get("REMOTE_ADDR")
                )

                messages.success(
                    request,
                    "Login Successful"
                )

                if user.profile.role == "admin":
                    return redirect("admin_dashboard")

                elif user.profile.role == "trainer":
                    return redirect("trainer_dashboard")

                else:
                    return redirect("student_dashboard")

        # Failed login
        cache.set(
            f"login_attempts_{username}",
            attempts + 1,
            timeout=300
        )

        AuditLog.objects.create(
            user=None,
            action="FAILED_LOGIN",
            description=f"Failed login attempt for username: {username}",
            ip_address=request.META.get("REMOTE_ADDR")
        )

        messages.error(
            request,
            "Invalid username or password."
        )

    else:

        form = AuthenticationForm()

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )

def logout_user(request):

    AuditLog.objects.create(
        user=request.user,
        action="LOGOUT",
        description="User logged out",
        ip_address=request.META.get("REMOTE_ADDR")
    )

    logout(request)

    messages.success(
        request,
        "Logout Successful"
    )

    return redirect("login")

@login_required
def dashboard(request):

    context = get_dashboard_statistics()

    return render(
        request,
        "dashboard.html",
        context
    )


@login_required
@role_required("student")
def student_dashboard(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    profile_completion = 0

    try:
        student_profile = student.profile

        fields = [
            student_profile.phone,
            student_profile.address,
            student_profile.date_of_birth
        ]

        completed = sum(
            1 for field in fields if field
        )

        profile_completion = int(
            (completed / len(fields)) * 100
        )

    except StudentProfile.DoesNotExist:

        profile_completion = 0

    context = {
        "user": request.user,
        "profile": request.user.profile,
        "student": student,
        "profile_completion": profile_completion,
    }

    return render(
        request,
        "dashboards/student_dashboard.html",
        context
    )

@login_required
@role_required("admin")
def admin_dashboard(request):

    average_marks = Student.objects.aggregate(
        Avg("marks")
    )["marks__avg"] or 0

    context = {
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.count(),
        "total_departments": Department.objects.count(),
        "recent_students": Student.objects.order_by(
            "-joined_date"
        )[:5],
        "average_marks": average_marks,
    }

    return render(
        request,
        "dashboards/admin_dashboard.html",
        context
    )

@login_required
@role_required("trainer")
def trainer_dashboard(request):

    assigned_students = Student.objects.filter(
        assigned_trainer=request.user
    )

    average_marks = assigned_students.aggregate(
        Avg("marks")
    )["marks__avg"] or 0

    context = {
        "total_students": assigned_students.count(),
        "total_courses": Course.objects.count(),
        "average_marks": average_marks,
    }

    return render(
        request,
        "dashboards/trainer_dashboard.html",
        context
    )

class CustomPasswordChangeView(PasswordChangeView):

    template_name = "registration/password_change.html"

    def form_valid(self, form):

        response = super().form_valid(form)

        AuditLog.objects.create(
            user=self.request.user,
            action="PASSWORD_CHANGE",
            description="Password changed successfully",
            ip_address=self.request.META.get("REMOTE_ADDR")
        )

        return response

@login_required
@role_required("trainer")
def add_feedback(request):

    if request.method == "POST":

        form = FeedbackForm(request.POST)

        if form.is_valid():

            feedback = form.save(commit=False)

            feedback.trainer = request.user

            create_feedback(
                student=feedback.student,
                trainer=request.user,
                rating=feedback.rating,
                comments=feedback.comments,
                visible_to_student=feedback.visible_to_student
            )

            messages.success(
                request,
                "Feedback added successfully."
            )

            return redirect("student_list")

    else:

        form = FeedbackForm()

    return render(
        request,
        "feedback/add_feedback.html",
        {
            "form": form
        }
    )

@login_required
def feedback_list(request):

    if request.user.profile.role == "student":

        student = Student.objects.get(user=request.user)

        feedbacks = Feedback.objects.filter(
            student=student,
            visible_to_student=True
        )

    elif request.user.profile.role == "trainer":

        feedbacks = Feedback.objects.filter(
            trainer=request.user
        )

    else:

        feedbacks = Feedback.objects.all()

    return render(
        request,
        "feedback/feedback_list.html",
        {
            "feedbacks": feedbacks
        }
    )


@login_required
@role_required("trainer")
def edit_feedback(request, id):

    feedback = get_object_or_404(
        Feedback,
        id=id,
        trainer=request.user
    )

    if request.method == "POST":

        form = FeedbackForm(
            request.POST,
            instance=feedback
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Feedback updated successfully."
            )

            return redirect("feedback_list")

    else:

        form = FeedbackForm(
            instance=feedback
        )

    return render(
        request,
        "feedback/add_feedback.html",
        {
            "form": form
        }
    )

@login_required
@role_required("trainer")
def update_marks(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == "POST":

        form = MarksHistoryForm(request.POST)

        if form.is_valid():

            history = form.save(commit=False)

            update_student_marks(
                student=student,
                new_marks=history.new_marks,
                updated_by=request.user,
                reason=history.reason
            )

            messages.success(
                request,
                "Marks updated successfully."
            )

            return redirect("student_list")

    else:

        form = MarksHistoryForm()

    return render(
        request,
        "marks/update_marks.html",
        {
            "form": form,
            "student": student
        }
    )

@login_required
def marks_history(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    history = MarksHistory.objects.filter(
        student=student
    ).order_by("-updated_at")

    return render(
        request,
        "marks/history.html",
        {
            "student": student,
            "history": history
        }
    )
from django.db.models import Q

@login_required
@role_required("admin")
def audit_log_list(request):

    logs = AuditLog.objects.all().order_by("-timestamp")

    search = request.GET.get("search")
    action = request.GET.get("action")
    start = request.GET.get("start")
    end = request.GET.get("end")

    if search:
        logs = logs.filter(
            Q(description__icontains=search) |
            Q(user__username__icontains=search)
        )

    if action:
        logs = logs.filter(action=action)

    if start:
        logs = logs.filter(timestamp__date__gte=start)

    if end:
        logs = logs.filter(timestamp__date__lte=end)

    paginator = Paginator(logs, 10)

    page = request.GET.get("page")

    logs = paginator.get_page(page)

    return render(
        request,
        "audit/audit_log_list.html",
        {
            "logs": logs
        }
    )






