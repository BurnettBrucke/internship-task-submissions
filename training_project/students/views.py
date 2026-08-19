from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .decorators import role_required

from .forms import (
    StudentForm,
    DepartmentForm,
    CourseForm,
    RegisterForm,
    FeedbackForm,
    MarksHistoryForm,
)

from .models import (
    Student,
    Department,
    Course,
    Enrollment,
    UserProfile,
    AuditLog,
    StudentProfile,
    Feedback,
    MarksHistory,
)

from .services import (
    get_dashboard_statistics,
    update_student_marks,
    create_feedback,
)


# =========================================================
# STUDENT LIST
# =========================================================

@login_required
def student_list(request):

    if request.user.profile.role == "student":
        return render(request, "403.html", status=403)

    students = (
        Student.objects
        .select_related(
            "department",
            "assigned_trainer"
        )
        .prefetch_related(
            "enrollments__course"
        )
        .order_by("id")
    )

    search = request.GET.get("search")
    department = request.GET.get("department")
    active = request.GET.get("active")
    result = request.GET.get("result")
    course = request.GET.get("course")

    if search:
        students = students.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(
                enrollments__course__course_name__icontains=search
            )
        ).distinct()

    if department:
        students = students.filter(
            department_id=department
        )

    if course:
        students = students.filter(
            enrollments__course_id=course
        ).distinct()

    if active == "yes":
        students = students.filter(active=True)

    elif active == "no":
        students = students.filter(active=False)

    if result == "pass":
        students = students.filter(
            enrollments__marks__gte=40
        ).distinct()

    elif result == "fail":
        students = students.filter(
            enrollments__marks__lt=40
        ).distinct()

    paginator = Paginator(
        students,
        5
    )

    students_page = paginator.get_page(
        request.GET.get("page")
    )

    context = {
        "students": students_page,
        "departments": Department.objects.all(),
        "courses": Course.objects.all(),
        "total_students": Student.objects.count(),
        "active_students": Student.objects.filter(
            active=True
        ).count(),
    }

    return render(
        request,
        "student_list.html",
        context
    )


# =========================================================
# ADD STUDENT
# =========================================================

@login_required
def add_student(request):

    if request.user.profile.role not in [
        "admin",
        "trainer"
    ]:
        return render(
            request,
            "403.html",
            status=403
        )

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()

            AuditLog.objects.create(
                user=request.user,
                action="CREATE",
                description=f"Added student: {student.name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )

            messages.success(
                request,
                "Student added successfully!"
            )

            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "add_student.html",
        {"form": form}
    )


# =========================================================
# STUDENT DETAIL
# =========================================================

@login_required
def student_detail(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    role = request.user.profile.role

    if role == "student":

        if student.user != request.user:
            return render(
                request,
                "403.html",
                status=403
            )

    elif role == "trainer":

        if student.assigned_trainer != request.user:
            return render(
                request,
                "403.html",
                status=403
            )

    elif role != "admin":

        return render(
            request,
            "403.html",
            status=403
        )

    enrollments = (
        Enrollment.objects
        .filter(student=student)
        .select_related("course")
    )

    return render(
        request,
        "student_detail.html",
        {
            "student": student,
            "enrollments": enrollments,
        }
    )


# =========================================================
# EDIT STUDENT
# =========================================================

@login_required
def edit_student(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    role = request.user.profile.role

    if role == "student":

        return render(
            request,
            "403.html",
            status=403
        )

    if (
        role == "trainer"
        and student.assigned_trainer != request.user
    ):
        return render(
            request,
            "403.html",
            status=403
        )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            student = form.save()

            AuditLog.objects.create(
                user=request.user,
                action="UPDATE",
                description=f"Updated student: {student.name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("student_list")

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "student_form.html",
        {"form": form}
    )


# =========================================================
# DELETE STUDENT
# =========================================================

@login_required
def delete_student(request, student_id):

    if request.user.profile.role != "admin":

        return render(
            request,
            "403.html",
            status=403
        )

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        AuditLog.objects.create(
            user=request.user,
            action="DELETE",
            description=f"Deleted student: {student.name}",
            ip_address=request.META.get("REMOTE_ADDR")
        )

        student.delete()

        messages.success(
            request,
            "Student deleted successfully."
        )

        return redirect("student_list")

    return render(
        request,
        "student_confirm_delete.html",
        {"student": student}
    )


# =========================================================
# DEPARTMENT LIST
# =========================================================

@login_required
@role_required("admin")
def department_list(request):

    departments = (
        Department.objects
        .prefetch_related("students")
        .order_by("name")
    )

    return render(
        request,
        "department/department_list.html",
        {
            "departments": departments
        }
    )


# =========================================================
# ADD DEPARTMENT
# =========================================================

@login_required
@role_required("admin")
def add_department(request):

    if request.method == "POST":

        form = DepartmentForm(
            request.POST
        )

        if form.is_valid():

            department = form.save()

            AuditLog.objects.create(
                user=request.user,
                action="CREATE",
                description=f"Created department: {department.name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )

            messages.success(
                request,
                "Department created successfully."
            )

            return redirect("department_list")

    else:

        form = DepartmentForm()

    return render(
        request,
        "department/department_form.html",
        {
            "form": form,
            "title": "Add Department"
        }
    )


# =========================================================
# EDIT DEPARTMENT
# =========================================================

@login_required
@role_required("admin")
def edit_department(request, department_id):

    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method == "POST":

        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():

            department = form.save()

            AuditLog.objects.create(
                user=request.user,
                action="UPDATE",
                description=f"Updated department: {department.name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )

            messages.success(
                request,
                "Department updated successfully."
            )

            return redirect("department_list")

    else:

        form = DepartmentForm(
            instance=department
        )

    return render(
        request,
        "department/department_form.html",
        {
            "form": form,
            "title": "Edit Department"
        }
    )


# =========================================================
# DELETE DEPARTMENT
# =========================================================

@login_required
@role_required("admin")
def delete_department(request, department_id):

    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method != "POST":

        return render(
            request,
            "department/department_confirm_delete.html",
            {
                "department": department
            }
        )

    name = department.name

    try:

        department.delete()

    except Exception:

        messages.error(
            request,
            "Department cannot be deleted because students are assigned to it."
        )

        return redirect("department_list")

    AuditLog.objects.create(
        user=request.user,
        action="DELETE",
        description=f"Deleted department: {name}",
        ip_address=request.META.get("REMOTE_ADDR")
    )

    messages.success(
        request,
        "Department deleted successfully."
    )

    return redirect("department_list")


# =========================================================
# COURSE LIST
# =========================================================

@login_required
@role_required("admin")
def course_list(request):

    courses = (
        Course.objects
        .prefetch_related("enrollments")
        .order_by("course_name")
    )

    return render(
        request,
        "course/course_list.html",
        {
            "courses": courses
        }
    )


# =========================================================
# ADD COURSE
# =========================================================

@login_required
@role_required("admin")
def add_course(request):

    if request.method == "POST":

        form = CourseForm(
            request.POST
        )

        if form.is_valid():

            course = form.save()

            AuditLog.objects.create(
                user=request.user,
                action="CREATE",
                description=f"Created course: {course.course_name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )

            messages.success(
                request,
                "Course created successfully."
            )

            return redirect("course_list")

    else:

        form = CourseForm()

    return render(
        request,
        "course/course_form.html",
        {
            "form": form,
            "title": "Add Course"
        }
    )


# =========================================================
# EDIT COURSE
# =========================================================

@login_required
@role_required("admin")
def edit_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            course = form.save()

            AuditLog.objects.create(
                user=request.user,
                action="UPDATE",
                description=f"Updated course: {course.course_name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )

            messages.success(
                request,
                "Course updated successfully."
            )

            return redirect("course_list")

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "course/course_form.html",
        {
            "form": form,
            "title": "Edit Course"
        }
    )


# =========================================================
# DELETE COURSE
# =========================================================

@login_required
@role_required("admin")
def delete_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    if request.method != "POST":

        return render(
            request,
            "course/course_confirm_delete.html",
            {
                "course": course
            }
        )

    name = course.course_name

    try:

        course.delete()

    except Exception:

        messages.error(
            request,
            "Course cannot be deleted because students are enrolled in it."
        )

        return redirect("course_list")

    AuditLog.objects.create(
        user=request.user,
        action="DELETE",
        description=f"Deleted course: {name}",
        ip_address=request.META.get("REMOTE_ADDR")
    )

    messages.success(
        request,
        "Course deleted successfully."
    )

    return redirect("course_list")


# =========================================================
# REGISTER
# =========================================================

def register_user(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            department = Department.objects.first()

            if department is None:

                messages.error(
                    request,
                    "Please create at least one department first."
                )

                return redirect("register")

            with transaction.atomic():

                user = form.save()

                UserProfile.objects.create(
                    user=user,
                    role="student"
                )

                Student.objects.create(
                    user=user,
                    department=department,
                    name=user.username,
                    email=user.email,
                    age=18,
                    active=True
                )

            login(
                request,
                user
            )

            messages.success(
                request,
                "Registration successful."
            )

            return redirect(
                "student_dashboard"
            )

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


# =========================================================
# LOGIN
# =========================================================

def login_user(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        )

        attempts = cache.get(
            f"login_attempts_{username}",
            0
        )

        if attempts >= 5:

            messages.error(
                request,
                "Account temporarily locked. Try again after 5 minutes."
            )

            return redirect("login")

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get(
                "username"
            )

            password = form.cleaned_data.get(
                "password"
            )

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                try:

                    profile = user.profile

                except UserProfile.DoesNotExist:

                    messages.error(
                        request,
                        "User profile is not configured."
                    )

                    return redirect("login")

                if (
                    profile.role == "trainer"
                    and not profile.is_approved
                ):

                    messages.error(
                        request,
                        "Your trainer account is waiting for administrator approval."
                    )

                    return redirect("login")

                cache.delete(
                    f"login_attempts_{username}"
                )

                login(
                    request,
                    user
                )

                AuditLog.objects.create(
                    user=user,
                    action="LOGIN",
                    description="User logged in",
                    ip_address=request.META.get("REMOTE_ADDR")
                )

                messages.success(
                    request,
                    "Login successful."
                )

                if profile.role == "admin":

                    return redirect(
                        "admin_dashboard"
                    )

                elif profile.role == "trainer":

                    return redirect(
                        "trainer_dashboard"
                    )

                return redirect(
                    "student_dashboard"
                )

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


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_user(request):

    if request.method != "POST":

        return render(
            request,
            "403.html",
            status=403
        )

    AuditLog.objects.create(
        user=request.user,
        action="LOGOUT",
        description="User logged out",
        ip_address=request.META.get("REMOTE_ADDR")
    )

    logout(request)

    messages.success(
        request,
        "Logout successful."
    )

    return redirect("login")


# =========================================================
# GENERAL DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    role = request.user.profile.role

    if role == "admin":

        return redirect(
            "admin_dashboard"
        )

    elif role == "trainer":

        return redirect(
            "trainer_dashboard"
        )

    return redirect(
        "student_dashboard"
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

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
            student_profile.date_of_birth,
        ]

        completed = sum(
            1
            for field in fields
            if field
        )

        profile_completion = int(
            (completed / len(fields)) * 100
        )

    except StudentProfile.DoesNotExist:

        profile_completion = 0

    enrollments = (
        Enrollment.objects
        .filter(student=student)
        .select_related("course")
    )

    context = {
        "user": request.user,
        "profile": request.user.profile,
        "student": student,
        "profile_completion": profile_completion,
        "enrollments": enrollments,
    }

    return render(
        request,
        "dashboards/student_dashboard.html",
        context
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@login_required
@role_required("admin")
def admin_dashboard(request):

    context = get_dashboard_statistics()

    return render(
        request,
        "dashboards/admin_dashboard.html",
        context
    )


# =========================================================
# TRAINER DASHBOARD
# =========================================================

@login_required
@role_required("trainer")
def trainer_dashboard(request):

    assigned_students = Student.objects.filter(
        assigned_trainer=request.user
    )

    average_marks = Enrollment.objects.filter(
        student__in=assigned_students
    ).aggregate(
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


# =========================================================
# PASSWORD CHANGE
# =========================================================

class CustomPasswordChangeView(
    PasswordChangeView
):

    template_name = (
        "registration/password_change.html"
    )

    def form_valid(self, form):

        response = super().form_valid(
            form
        )

        AuditLog.objects.create(
            user=self.request.user,
            action="UPDATE",
            description="Password changed successfully",
            ip_address=self.request.META.get("REMOTE_ADDR")
        )

        return response


# =========================================================
# ADD FEEDBACK
# =========================================================

@login_required
@role_required("trainer")
def add_feedback(request):

    assigned_enrollments = (
        Enrollment.objects
        .filter(
            student__assigned_trainer=request.user
        )
        .select_related(
            "student",
            "course"
        )
        .order_by(
            "student__name",
            "course__course_name"
        )
    )

    if request.method == "POST":

        form = FeedbackForm(
            request.POST,
            user=request.user
        )

        form.fields[
            "enrollment"
        ].queryset = assigned_enrollments

        if form.is_valid():

            enrollment = form.cleaned_data[
                "enrollment"
            ]

            create_feedback(
                enrollment=enrollment,
                trainer=request.user,
                rating=form.cleaned_data["rating"],
                comments=form.cleaned_data["comments"],
                visible_to_student=form.cleaned_data[
                    "visible_to_student"
                ]
            )

            messages.success(
                request,
                "Feedback added successfully."
            )

            return redirect(
                "feedback_list"
            )

    else:

        form = FeedbackForm(
            user=request.user
        )

        form.fields[
            "enrollment"
        ].queryset = assigned_enrollments

    return render(
        request,
        "feedback/add_feedback.html",
        {
            "form": form
        }
    )


# =========================================================
# FEEDBACK LIST
# =========================================================

@login_required
def feedback_list(request):

    role = request.user.profile.role

    if role == "student":

        student = get_object_or_404(
            Student,
            user=request.user
        )

        feedbacks = (
            Feedback.objects
            .filter(
                student=student,
                visible_to_student=True
            )
            .select_related(
                "trainer",
                "enrollment__course"
            )
        )

    elif role == "trainer":

        feedbacks = (
            Feedback.objects
            .filter(
                trainer=request.user
            )
            .select_related(
                "student",
                "enrollment__course"
            )
        )

    elif role == "admin":

        feedbacks = (
            Feedback.objects
            .all()
            .select_related(
                "student",
                "trainer",
                "enrollment__course"
            )
        )

    else:

        return render(
            request,
            "403.html",
            status=403
        )

    return render(
        request,
        "feedback/feedback_list.html",
        {
            "feedbacks": feedbacks
        }
    )


# =========================================================
# EDIT FEEDBACK
# =========================================================

@login_required
@role_required("trainer")
def edit_feedback(request, feedback_id):

    feedback = get_object_or_404(
        Feedback,
        id=feedback_id,
        trainer=request.user
    )

    assigned_enrollments = (
        Enrollment.objects
        .filter(
            student__assigned_trainer=request.user
        )
        .select_related(
            "student",
            "course"
        )
    )

    if request.method == "POST":

        form = FeedbackForm(
            request.POST,
            instance=feedback,
            user=request.user
        )

        form.fields[
            "enrollment"
        ].queryset = assigned_enrollments

        if form.is_valid():

            enrollment = form.cleaned_data[
                "enrollment"
            ]

            feedback.enrollment = enrollment
            feedback.student = enrollment.student
            feedback.rating = form.cleaned_data["rating"]
            feedback.comments = form.cleaned_data["comments"]
            feedback.visible_to_student = form.cleaned_data[
                "visible_to_student"
            ]

            feedback.save()

            AuditLog.objects.create(
                user=request.user,
                action="UPDATE",
                description=f"Updated feedback for {feedback.student.name}",
                ip_address=request.META.get("REMOTE_ADDR")
            )

            messages.success(
                request,
                "Feedback updated successfully."
            )

            return redirect(
                "feedback_list"
            )

    else:

        form = FeedbackForm(
            instance=feedback,
            user=request.user
        )

        form.fields[
            "enrollment"
        ].queryset = assigned_enrollments

    return render(
        request,
        "feedback/add_feedback.html",
        {
            "form": form
        }
    )


# =========================================================
# UPDATE MARKS
# =========================================================

@login_required
@role_required("trainer")
def update_marks(request, enrollment_id):

    enrollment = get_object_or_404(
        Enrollment.objects.select_related(
            "student",
            "course"
        ),
        id=enrollment_id
    )

    if enrollment.student.assigned_trainer != request.user:

        return render(
            request,
            "403.html",
            status=403
        )

    if request.method == "POST":

        form = MarksHistoryForm(
            request.POST
        )

        form.fields[
            "enrollment"
        ].queryset = Enrollment.objects.filter(
            id=enrollment.id
        )

        if form.is_valid():

            new_marks = form.cleaned_data["new_marks"]
            reason = form.cleaned_data["reason"]

            update_student_marks(
                enrollment=enrollment,
                new_marks=new_marks,
                updated_by=request.user,
                reason=reason
            )

            messages.success(
                request,
                "Marks updated successfully."
            )

            return redirect(
                "student_list"
            )

    else:

        form = MarksHistoryForm(
            initial={
                "enrollment": enrollment,
                "new_marks": enrollment.marks,
            }
        )

        form.fields[
            "enrollment"
        ].queryset = Enrollment.objects.filter(
            id=enrollment.id
        )

    return render(
        request,
        "marks/update_marks.html",
        {
            "form": form,
            "student": enrollment.student,
            "enrollment": enrollment,
        }
    )


# =========================================================
# MARKS HISTORY
# =========================================================

@login_required
def marks_history(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    role = request.user.profile.role

    if role == "student":

        if student.user != request.user:

            return render(
                request,
                "403.html",
                status=403
            )

    elif role == "trainer":

        if student.assigned_trainer != request.user:

            return render(
                request,
                "403.html",
                status=403
            )

    elif role != "admin":

        return render(
            request,
            "403.html",
            status=403
        )

    history = (
        MarksHistory.objects
        .filter(
            student=student
        )
        .select_related(
            "enrollment__course",
            "updated_by"
        )
        .order_by("-updated_at")
    )

    return render(
        request,
        "marks/history.html",
        {
            "student": student,
            "history": history,
        }
    )


# =========================================================
# AUDIT LOG
# =========================================================

@login_required
@role_required("admin")
def audit_log_list(request):

    logs = (
        AuditLog.objects
        .select_related("user")
        .all()
        .order_by("-timestamp")
    )

    search = request.GET.get("search")
    action = request.GET.get("action")
    start = request.GET.get("start")
    end = request.GET.get("end")

    if search:

        logs = logs.filter(
            Q(description__icontains=search)
            | Q(user__username__icontains=search)
        )

    if action:

        logs = logs.filter(
            action=action
        )

    if start:

        logs = logs.filter(
            timestamp__date__gte=start
        )

    if end:

        logs = logs.filter(
            timestamp__date__lte=end
        )

    paginator = Paginator(
        logs,
        10
    )

    logs = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "audit/audit_log_list.html",
        {
            "logs": logs
        }
    )