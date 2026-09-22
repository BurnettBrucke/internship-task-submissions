from datetime import datetime

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_POST


from .services.audit_service import (
    audit_login,
    audit_logout,
    audit_failed_login,
    audit_account_blocked,
    audit_blocked_login,
    audit_student_created,
    audit_student_updated,
    audit_student_deleted,
    audit_course_created,
    audit_course_updated,
    audit_course_status_changed,
    audit_trainer_approved,
    audit_trainer_rejected,
    audit_user_activated,
    audit_user_deactivated,
    audit_marks_updated,
    audit_feedback_created,
    audit_feedback_updated,
    audit_trainer_deleted,
)

from .decorators import role_required

from .form import (
    StudentForm,
    TrainerRegistrationForm,
    LoginForm,
    MarkForm,
    FeedbackForm,
    StudentProfileForm,
    CourseForm,
)

from .models import (
    Student,
    Department,
    Course,
    StudentProfile,
    UserProfile,
    Enrollment,
    MarkHistory,
    TrainerCourse,
    Feedback,
    AuditLog,
)

# Service layer
from .services.student_service import (
    create_student_account,
    enroll_student_in_courses,
    update_student_courses,
)

from .services.marks_service import (
    trainer_can_update_marks,
    update_enrollment_marks,
)

from .services.feedback_service import (
    trainer_can_manage_feedback,
    create_feedback as create_feedback_service,
    update_feedback as update_feedback_service,
    trainer_owns_feedback,
)


from .services.dashboard_service import (
    get_admin_dashboard_data,
    get_trainer_dashboard_data,
    get_student_dashboard_data,
    get_trainer_detail_data,
)

from .services.permission_service import (
    is_admin,
    is_student,
    is_approved_trainer,
    student_owns_record,
)
# Create your views here.

def home(request):
    context = {'company_name' : "Bug Network private Limited"}
    return render(request ,"home.html" , context) 

def about(request):
    return render(request , "about.html")


@login_required
def student_list(request):

    students = (
        Student.objects
        .select_related("department")
        .prefetch_related("enrollments__course")
    )

    # Search
    search = request.GET.get("search", "").strip()

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(enrollments__course__course_name__icontains=search)
        )

    # Department filter
    department = request.GET.get("department")

    if department:
        students = students.filter(
            department_id=department
        )

    # Course filter
    course = request.GET.get("course")

    if course:
        students = students.filter(
            enrollments__course_id=course
        )

    # Activity filter
    status = request.GET.get("status")

    if status == "active":
        students = students.filter(active=True)

    elif status == "inactive":
        students = students.filter(active=False)

    # Pass / Fail filter
    result = request.GET.get("result")

    if result == "pass":
        students = students.filter(
            enrollments__marks__gte=40
        )

    elif result == "fail":
        students = students.filter(
            enrollments__marks__lt=40
        )

    # Enrollment joins can create duplicate students
    students = students.distinct()

    # Number of courses for each student
    students = students.annotate(
        course_count=Count(
            "enrollments__course",
            distinct=True
        )
    ).order_by("name")

    # Statistics
    total_students = students.count()

    active_students = students.filter(
        active=True
    ).count()

    # Dropdown data
    departments = Department.objects.all().order_by("name")
    courses = Course.objects.all().order_by("course_name")

    return render(
        request,
        "students/student_list.html",
        {
            "search": search,
            "department": department,
            "course": course,
            "status": status,
            "result": result,

            "departments": departments,
            "courses": courses,

            "students": students,

            "total_students": total_students,
            "active_students": active_students,
        }
    )



@role_required(UserProfile.Role.ADMIN)
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            student = create_student_account(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                age=form.cleaned_data["age"],
                active=form.cleaned_data["active"],
                department=form.cleaned_data["department"],
                request=request,
            )

            enroll_student_in_courses(
                student,
                form.cleaned_data["courses"],
            )

            audit_student_created(
                request,
                student
            )

            messages.success(
                request,
                "Student account created successfully. "
                "An activation email has been sent."
            )

            return redirect("students_list")

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "breadcrumbs": [
                {
                    "name": "Home",
                    "url": reverse("home"),
                },
                {
                    "name": "Students",
                    "url": reverse("students_list"),
                },
                {
                    "name": "Add Student",
                },
            ],
        },
    )
@login_required
def student_detail(request, id):

    student = get_object_or_404(
        Student.objects.select_related(
            "department",
            "profile",
        ),
        id=id,
    )

    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if is_admin(request.user):

        enrollments = (
            Enrollment.objects
            .filter(student=student)
            .select_related("course")
        )

    elif student_owns_record(
        request.user,
        student,
    ):

        enrollments = (
            Enrollment.objects
            .filter(student=student)
            .select_related("course")
        )

    elif is_approved_trainer(request.user):

        enrollments = (
            Enrollment.objects
            .filter(
                student=student,
                course__trainer_assignments__trainer=request.user,
            )
            .select_related("course")
            .distinct()
        )

        if not enrollments.exists():
            return HttpResponseForbidden(
                "You are not authorized to view this student."
            )

    else:

        return HttpResponseForbidden(
            "You are not authorized to view student details."
        )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student,
            "enrollments": enrollments,

            "breadcrumbs": [
                {
                    "name": "Home",
                    "url": reverse("home"),
                },
                {
                    "name": "Students",
                    "url": reverse("students_list"),
                },
                {
                    "name": student.name,
                },
            ],
        }
    )
@role_required(UserProfile.Role.ADMIN)
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            update_student_courses(
                student,
                form.cleaned_data["courses"],
            )

            audit_student_updated(
                request,
                student
            )

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("admin_dashboard")

    else:

        form = StudentForm(
            instance=student
        )

        form.fields["courses"].initial = (
            Enrollment.objects
            .filter(student=student)
            .values_list("course_id", flat=True)
        )

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "student": student,
            "breadcrumbs": [
                {
                    "name": "Home",
                    "url": reverse("home"),
                },
                {
                    "name": "Students",
                    "url": reverse("students_list"),
                },
                {
                    "name": student.name,
                    "url": reverse(
                        "student_detail",
                        args=[student.id]
                    ),
                },
                {
                    "name": "Edit",
                },
            ],
        }
    )
@role_required(UserProfile.Role.ADMIN)
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == "POST":

        audit_student_deleted(request , student.name , student.id)
        student.delete()


        messages.success(
            request,
            "Student deleted successfully."
        )

        return redirect("admin_dashboard")

    return render(
        request,
        "students/student_confirm_delete.html",
        {
            "student": student
        }
    )

def set_student_password(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None:
        messages.error(
            request,
            "This password setup link is invalid."
        )
        return redirect("login")

    if not default_token_generator.check_token(user, token):
        messages.error(
            request,
            "This password setup link is invalid or has expired."
        )
        return redirect("login")

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your password has been set successfully. You can now log in."
            )

            return redirect("login")

    else:
        form = SetPasswordForm(user)

    return render(
        request,
        "registration/set_student_password.html",
        {
            "form": form,
        }
    )

def trainer_register(request):
    if request.method == "POST":
        form = TrainerRegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            UserProfile.objects.create(
                user=user,
                role=UserProfile.Role.TRAINER,
                status=UserProfile.Status.PENDING,
                requested_course = form.cleaned_data["requested_course"],
            )

            messages.success(
                request,
                "Trainer registration submitted successfully. "
                "Your account is waiting for admin approval."
            )

            return redirect("login")

    else:
        form = TrainerRegistrationForm()

    return render(
        request,
         "registration/register.html",
        {"form": form}
    )


def login_backend(request):

    # If user is already logged in
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = LoginForm(request.POST)

        login_value = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")

        # -------------------------------------------------
        # 1. FIND USER BY EMAIL OR USERNAME
        # -------------------------------------------------

        user = None

        try:
            user = User.objects.get(
                email__iexact=login_value
            )

        except User.DoesNotExist:

            try:
                user = User.objects.get(
                    username=login_value
                )

            except User.DoesNotExist:
                user = None

        # -------------------------------------------------
        # 2. UNKNOWN USER
        # -------------------------------------------------

        if user is None:

            form.add_error(
                None,
                "Invalid username/email or password."
            )

            audit_failed_login(request)

            return render(
                request,
                "registration/login.html",
                {"form": form}
            )

        # -------------------------------------------------
        # 3. GET USER PROFILE
        # -------------------------------------------------

        profile = getattr(
            user,
            "profile",
            None
        )

        # -------------------------------------------------
        # 4. CHECK IF ACCOUNT IS ALREADY BLOCKED
        # -------------------------------------------------

        if profile and profile.login_blocked:

            audit_blocked_login(
                request,
                user
            )

            form.add_error(
                None,
                "Your account is blocked because of too many "
                "failed login attempts. Please contact the administrator."
            )

            return render(
                request,
                "registration/login.html",
                {"form": form}
            )

        # -------------------------------------------------
        # 5. AUTHENTICATE PASSWORD
        # -------------------------------------------------

        authenticated_user = authenticate(
            request,
            username=user.username,
            password=password
        )

        # -------------------------------------------------
        # 6. WRONG PASSWORD
        # -------------------------------------------------

        if authenticated_user is None:

            if profile:

                profile.failed_login_attempts += 1

                # -----------------------------------------
                # BLOCK AFTER 5 FAILED ATTEMPTS
                # -----------------------------------------

                if profile.failed_login_attempts >= 5:

                    profile.login_blocked = True

                    profile.login_blocked_at = timezone.now()

                    profile.save(
                        update_fields=[
                            "failed_login_attempts",
                            "login_blocked",
                            "login_blocked_at",
                        ]
                    )

                    audit_account_blocked(
                        request,
                        user
                    )

                    form.add_error(
                        None,
                        "Your account has been blocked after "
                        "5 failed login attempts. "
                        "Please contact the administrator."
                    )

                # -----------------------------------------
                # FAILED ATTEMPTS 1-4
                # -----------------------------------------

                else:

                    profile.save(
                        update_fields=[
                            "failed_login_attempts"
                        ]
                    )

                    audit_failed_login(
                        request,
                        user,
                        profile.failed_login_attempts
                    )

                    remaining = (
                        5 - profile.failed_login_attempts
                    )

                    form.add_error(
                        None,
                        f"Invalid credentials. You have "
                        f"{remaining} login attempt(s) remaining."
                    )

            return render(
                request,
                "registration/login.html",
                {"form": form}
            )

        # -------------------------------------------------
        # 7. CHECK IF DJANGO USER IS INACTIVE
        # -------------------------------------------------

        if not authenticated_user.is_active:

            form.add_error(
                None,
                "Your account is inactive. "
                "Please contact the administrator."
            )

            return render(
                request,
                "registration/login.html",
                {"form": form}
            )

        # -------------------------------------------------
        # 8. SUCCESSFUL LOGIN
        # -------------------------------------------------

        if profile:

            # Reset failed attempts after successful login
            profile.failed_login_attempts = 0
            profile.login_blocked = False
            profile.login_blocked_at = None

            profile.save(
                update_fields=[
                    "failed_login_attempts",
                    "login_blocked",
                    "login_blocked_at",
                ]
            )

        # Login user
        login(
            request,
            authenticated_user
        )

        # Create audit log
        audit_login(
            request,
            authenticated_user
        )

        messages.success(
            request,
            "Login successful."
        )

        # -------------------------------------------------
        # 9. REDIRECT TO HOME
        # -------------------------------------------------

        return redirect("home")

    # -----------------------------------------------------
    # GET REQUEST
    # -----------------------------------------------------

    form = LoginForm()

    return render(
        request,
        "registration/login.html",
        {"form": form}
    )
@login_required
def logout_backend(request):

    if request.method != "POST":
        return HttpResponseForbidden(
            "Logout must use POST."
        )
    user = request.user
    audit_logout(request,user)

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")

@login_required
def dashboard(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role == UserProfile.Role.ADMIN:
        return redirect("admin_dashboard")

    if profile.role == UserProfile.Role.TRAINER:
        return redirect("trainer_dashboard")

    if profile.role == UserProfile.Role.STUDENT:
        return redirect("student_dashboard")

    return HttpResponseForbidden(
        "You are not authorized to access a dashboard."
    )


@role_required(UserProfile.Role.ADMIN)
def admin_dashboard(request):

    context = get_admin_dashboard_data()

    return render(
        request,
        "dashboards/admin_dashboard.html",
        context,
    )
@role_required(UserProfile.Role.ADMIN)
def trainer_detail(request, id):

    trainer = get_object_or_404(
        User.objects.select_related(
            "profile",
            "profile__requested_course",
        ),
        id=id,
        profile__role=UserProfile.Role.TRAINER,
    )

    context = get_trainer_detail_data(
        trainer
    )

    return render(
        request,
        "trainers/trainer_detail.html",
        context,
    )


@role_required(UserProfile.Role.ADMIN)
@require_POST
def assign_trainer_course(request, id):

    trainer = get_object_or_404(
        User,
        id=id,
        profile__role=UserProfile.Role.TRAINER,
    )

    course_id = request.POST.get("course")

    if not course_id:
        messages.error(
            request,
            "Please select a course."
        )
        return redirect(
            "trainer_detail",
            id=trainer.id
        )

    course = get_object_or_404(
        Course,
        id=course_id,
        active_status=True,
    )

    assignment, created = TrainerCourse.objects.get_or_create(
        trainer=trainer,
        course=course,
    )

    if created:
        messages.success(
            request,
            f"{course.course_name} has been assigned to "
            f"{trainer.username}."
        )
    else:
        messages.info(
            request,
            f"{trainer.username} is already assigned to "
            f"{course.course_name}."
        )

    return redirect(
        "trainer_detail",
        id=trainer.id
    )

@role_required(UserProfile.Role.TRAINER)
def trainer_dashboard(request):

    profile = request.user.profile

    if profile.status != UserProfile.Status.APPROVED:

        messages.warning(
            request,
            "Your trainer account is waiting for admin approval."
        )

        return render(
            request,
            "trainer_pending.html"
        )

    context = get_trainer_dashboard_data(
        request.user
    )

    return render(
        request,
        "dashboards/trainer_dashboard.html",
        context,
    )


@role_required(UserProfile.Role.STUDENT)
def edit_student_profile(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    profile = get_object_or_404(
        StudentProfile,
        student=student
    )

    if request.method == "POST":

        form = StudentProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully."
            )

            return redirect("student_dashboard")

    else:

        form = StudentProfileForm(
            instance=profile
        )

    return render(
        request,
        "students/edit_profile.html",
        {
            "form": form,
            "student": student,
        }
    )

@role_required(UserProfile.Role.STUDENT)
def student_dashboard(request):

    student = get_object_or_404(
        Student.objects.select_related(
            "department",
            "profile",
        ),
        user=request.user,
    )

    context = get_student_dashboard_data(
        student
    )

    return render(
        request,
        "dashboards/student_dashboard.html",
        context,
    )

@role_required(UserProfile.Role.ADMIN)
def approve_trainer(request, id):

    if request.method != "POST":
        return HttpResponseForbidden(
            "Approval must use POST."
        )

    profile = get_object_or_404(
        UserProfile,
        id=id,
        role=UserProfile.Role.TRAINER
    )

    if profile.requested_course is None:

        messages.error(
            request,
            "This trainer has not selected a course."
        )

        return redirect(
            "admin_dashboard"
        )

    profile.status = UserProfile.Status.APPROVED

    profile.save(
        update_fields=["status"]
    )

    TrainerCourse.objects.get_or_create(
        trainer=profile.user,
        course=profile.requested_course
    )
    audit_trainer_approved(request , profile , profile.requested_course)

    messages.success(
        request,
        f"{profile.user.username} has been approved "
        f"for {profile.requested_course.course_name}."
    )

    return redirect(
        "admin_dashboard"
    )

@role_required(UserProfile.Role.ADMIN)
def reject_trainer(request, id):

    if request.method != "POST":
        return HttpResponseForbidden(
            "Rejection must use POST."
        )

    profile = get_object_or_404(
        UserProfile,
        id=id,
        role=UserProfile.Role.TRAINER
    )
    TrainerCourse.objects.filter(
        trainer=profile.user
    ).delete()

    profile.status = UserProfile.Status.REJECTED

    profile.save(
        update_fields=["status"]
    )
    audit_trainer_rejected(request , profile)

    messages.success(
        request,
        f"{profile.user.username} has been rejected."
    )

    return redirect(
        "admin_dashboard"
    )

@role_required(UserProfile.Role.ADMIN)
def delete_trainer(request, id):

    if request.method != "POST":
        return HttpResponseForbidden(
            "Trainer deletion must use POST."
        )

    trainer = get_object_or_404(
        User.objects.select_related("profile"),
        id=id,
        profile__role=UserProfile.Role.TRAINER
    )

    # Admin cannot delete their own account
    if trainer == request.user:
        messages.error(
            request,
            "You cannot delete your own account."
        )
        return redirect("admin_dashboard")

    # Preserve marks history
    if MarkHistory.objects.filter(
        updated_by=trainer
    ).exists():
        messages.error(
            request,
            "This trainer cannot be deleted because they have marks history records."
        )
        return redirect("admin_dashboard")

    # Preserve feedback history
    if Feedback.objects.filter(
        trainer=trainer
    ).exists():
        messages.error(
            request,
            "This trainer cannot be deleted because they have feedback history records."
        )
        return redirect("admin_dashboard")

    trainer_name = trainer.username
    trainer_id = trainer.id

    # Remove trainer-course assignments first
    TrainerCourse.objects.filter(
        trainer=trainer
    ).delete()

    # Delete trainer account and profile
    trainer.delete()
    audit_trainer_deleted(
    request,
    trainer_name,
    trainer_id
)

    messages.success(
        request,
        f"Trainer '{trainer_name}' has been deleted."
    )

    return redirect("admin_dashboard")

@login_required
def update_marks(request, id):

    enrollment = get_object_or_404(
        Enrollment.objects.select_related(
            "student",
            "course",
        ),
        id=id,
    )

    if not trainer_can_update_marks(
        request.user,
        enrollment,
    ):
        return HttpResponseForbidden(
            "You are not authorized to update marks."
        )

    if request.method == "POST":

        form = MarkForm(request.POST)

        if form.is_valid():

            previous_marks = enrollment.marks

            new_marks = form.cleaned_data["marks"]

            reason = form.cleaned_data["reason"]

            updated_enrollment, history = (
                update_enrollment_marks(
                    enrollment=enrollment,
                    new_marks=new_marks,
                    reason=reason,
                    updated_by=request.user,
                )
            )

            audit_marks_updated(
                request,
                enrollment,
                previous_marks,
                new_marks,
                reason,
            )

            messages.success(
                request,
                "Marks updated successfully."
            )

            return redirect(
                "student_detail",
                id=enrollment.student.id,
            )

    else:

        initial_marks = {}

        if enrollment.marks is not None:
            initial_marks["marks"] = enrollment.marks

        form = MarkForm(
            initial=initial_marks
        )

    return render(
        request,
        "marks/mark_form.html",
        {
            "form": form,
            "enrollment": enrollment,
        }
    )

@login_required
def create_feedback(request, id):

    enrollment = get_object_or_404(
        Enrollment.objects.select_related(
            "student",
            "course",
        ),
        id=id,
    )

    if not trainer_can_manage_feedback(
        request.user,
        enrollment,
    ):
        return HttpResponseForbidden(
            "You are not authorized to create feedback."
        )

    if request.method == "POST":

        form = FeedbackForm(request.POST)

        if form.is_valid():

            feedback = create_feedback_service(
                enrollment=enrollment,
                trainer=request.user,
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"],
                visible=form.cleaned_data.get(
                    "visible",
                    True,
                ),
            )

            audit_feedback_created(
                request,
                feedback,
            )

            messages.success(
                request,
                "Feedback added successfully."
            )

            return redirect(
                "student_detail",
                id=enrollment.student.id,
            )

    else:

        form = FeedbackForm()

    return render(
        request,
        "feedback/feedback_form.html",
        {
            "form": form,
            "enrollment": enrollment,
        }
    )
@login_required
def edit_feedback(request, id):

    feedback = get_object_or_404(
        Feedback.objects.select_related(
            "student",
            "course",
            "trainer",
        ),
        id=id,
    )

    if not trainer_owns_feedback(
        feedback,
        request.user,
    ):
        return HttpResponseForbidden(
            "You can only edit your own feedback."
        )

    if request.method == "POST":

        form = FeedbackForm(
            request.POST,
            instance=feedback,
        )

        if form.is_valid():

            feedback = update_feedback_service(
                feedback=feedback,
                rating=form.cleaned_data["rating"],
                comment=form.cleaned_data["comment"],
                visible=form.cleaned_data.get(
                    "visible",
                    feedback.visible,
                ),
            )

            audit_feedback_updated(
                request,
                feedback,
            )

            messages.success(
                request,
                "Feedback updated successfully."
            )

            return redirect(
                "student_detail",
                id=feedback.student.id,
            )

    else:

        form = FeedbackForm(
            instance=feedback
        )

    return render(
        request,
        "feedback/feedback_form.html",
        {
            "form": form,
            "feedback": feedback,
            "enrollment": None,
        }
    )
@role_required(UserProfile.Role.ADMIN)
def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            course = form.save()

            audit_course_created(request , course)

            messages.success(
                request,
                "Course created successfully."
            )

            return redirect(
                "admin_dashboard"
            )

    else:

        form = CourseForm()

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "title": "Add Course",
            "breadcrumbs": [
    {
        "name": "Home",
        "url": reverse("home"),
    },
    {
        "name": "Courses",
        "url": reverse("course_list"),
    },
    {
        "name": "Add Course",
    },
],
        }
    )

@role_required(UserProfile.Role.ADMIN)
def edit_course(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            course = form.save()

            audit_course_updated(request , course)

            messages.success(
                request,
                "Course updated successfully."
            )

            return redirect(
                "admin_dashboard"
            )

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "course": course,
            "title": "Edit Course",
            "breadcrumbs": [
    {
        "name": "Home",
        "url": reverse("home"),
    },
    {
        "name": "Courses",
        "url": reverse("course_list"),
    },
    {
        "name": course.course_name,
        "url": reverse("course_detail", args=[course.id]),
    },
    {
        "name": "Edit",
    },
],
        }
    )

@role_required(UserProfile.Role.ADMIN)
def toggle_course_status(request, id):

    if request.method != "POST":
        return HttpResponseForbidden(
            "This action must use POST."
        )

    course = get_object_or_404(
        Course,
        id=id
    )

    course.active_status = not course.active_status

    course.save(
        update_fields=["active_status"]
    )

    audit_course_status_changed(request , course)

    if course.active_status:

        messages.success(
            request,
            f"{course.course_name} has been activated."
        )

    else:

        messages.warning(
            request,
            f"{course.course_name} has been deactivated."
        )

    return redirect(
        "admin_dashboard"
    )

@login_required
@role_required(UserProfile.Role.ADMIN)
@require_POST
def deactivate_user(request, id):
    profile = get_object_or_404(UserProfile, id=id)

    user = profile.user

    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect("admin_dashboard")

    user.is_active = False
    user.save(update_fields=["is_active"])

    # Keep Student status synchronized with account status
    if profile.role == UserProfile.Role.STUDENT:
        student = Student.objects.filter(user=user).first()

        if student:
            student.active = False
            student.save(update_fields=["active"])
    audit_user_deactivated(request,profile)
    messages.success(
        request,
        f"{user.username}'s account has been deactivated."
    )

    return redirect("admin_dashboard")

@login_required
@role_required(UserProfile.Role.ADMIN)
@require_POST
def activate_user(request, id):
    profile = get_object_or_404(UserProfile, id=id)

    user = profile.user

    user.is_active = True
    user.save(update_fields=["is_active"])

    # Keep Student status synchronized with account status
    if profile.role == UserProfile.Role.STUDENT:
        student = Student.objects.filter(user=user).first()

        if student:
            student.active = True
            student.save(update_fields=["active"])
            
    audit_user_activated(request,profile)

    messages.success(
        request,
        f"{user.username}'s account has been activated."
    )

    return redirect("admin_dashboard")


@login_required
def audit_logs(request):

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # Admin only
    if profile.role != UserProfile.Role.ADMIN:
        return HttpResponseForbidden(
            "You are not authorized to view audit logs."
        )

    logs = AuditLog.objects.select_related("user").all()

    # Search
    search = request.GET.get("search", "").strip()

    if search:
        logs = logs.filter(
            Q(user__username__icontains=search)
            | Q(user__email__icontains=search)
            | Q(description__icontains=search)
            | Q(ip_address__icontains=search)
        )

    # Action filter
    action = request.GET.get("action", "").strip()

    if action:
        logs = logs.filter(action=action)

    # User filter
    user_id = request.GET.get("user", "").strip()

    if user_id:
        logs = logs.filter(user_id=user_id)

    # Start date
    start_date = request.GET.get("start_date", "").strip()

    if start_date:
        try:
            start = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

            logs = logs.filter(
                timestamp__date__gte=start
            )
        except ValueError:
            pass

    # End date
    end_date = request.GET.get("end_date", "").strip()

    if end_date:
        try:
            end = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()

            logs = logs.filter(
                timestamp__date__lte=end
            )
        except ValueError:
            pass

    # Pagination
    paginator = Paginator(logs, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    users = User.objects.filter(
        audit_logs__isnull=False
    ).distinct().order_by("username")

    context = {
        "page_obj": page_obj,
        "users": users,
        "actions": AuditLog.Action.choices,

        "search": search,
        "selected_action": action,
        "selected_user": user_id,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(
        request,
        "audit_logs.html",
        context
    )


def error_403(request, exception):
    return render(
        request,
        "errors/403.html",
        status=403,
    )


def error_404(request, exception):
    return render(
        request,
        "errors/404.html",
        status=404,
    )


def error_500(request):
    return render(
        request,
        "errors/500.html",
        status=500,
    )


