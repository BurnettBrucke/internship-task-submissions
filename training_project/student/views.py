from django.db import transaction
from django.shortcuts import redirect,render,get_object_or_404 # type: ignore
from .form import (RegisterForm,StudentForm,AssignTrainerForm,MarksUpdateForm,FeedbackForm,AuditLogFilterForm,BootstrapPasswordChangeForm,BootstrapLoginForm,)
from .models import (
    student,
    department,
    UserProfile,
    AuditLog,
    Course,
    CourseMark,
    MarksHistory,
    Feedback,
    LoginAttempt,
)
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import role_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.views import PasswordChangeDoneView
from .services.audit import create_audit_log
from .services.marks import (
    get_course_for_trainer,
    get_assigned_student,
    get_course_mark,
    update_course_marks,
    
    get_marks_history_for_user,
)

from .services.feedback import (get_course_for_feedback, get_assigned_student_for_feedback, create_feedback, get_feedback_for_edit, update_feedback, get_feedback_for_user,)

from student.services.dashboard import (
    get_admin_dashboard_data,
    get_trainer_dashboard_data,
    get_student_dashboard_data,
)




# Authetication
def custom_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = BootstrapLoginForm(request,data=request.POST or None)

    if request.method == "POST":

        username = request.POST.get("username", "").strip()

        login_record, created = LoginAttempt.objects.get_or_create(
            username=username
        )

        now = timezone.now()

        # Check temporary block
        if (
            login_record.blocked_until
            and login_record.blocked_until > now
        ):

            remaining_seconds = (
                login_record.blocked_until - now
            ).total_seconds()

            remaining_minutes = max(
                1,
                int(remaining_seconds // 60) + 1
            )

            messages.error(
                request,
                f"Too many failed login attempts. "
                f"Please try again in {remaining_minutes} minute(s)."
            )

            return render(
                request,
                "registration/login.html",
                {"form": form}
            )

        if form.is_valid():

            user = form.get_user()

            # Check UserProfile
            try:
                profile = user.userprofile
            except UserProfile.DoesNotExist:

                messages.error(
                    request,
                    "Your account profile is not configured."
                )

                return render(
                    request,
                    "registration/login.html",
                    {"form": form}
                )

            # Check account activation
            if not user.is_active or not profile.is_active:

                messages.error(
                    request,
                    "Your account has been deactivated."
                )

                return render(
                    request,
                    "registration/login.html",
                    {"form": form}
                )

            # Check trainer approval
            if (
                profile.role == "trainer"
                and not profile.is_approved
            ):

                messages.warning(
                    request,
                    "Your trainer account is waiting for administrator approval."
                )

                return render(
                    request,
                    "registration/login.html",
                    {"form": form}
                )

            # Successful login
            login(request, user)

            login_record.failed_attempts = 0
            login_record.blocked_until = None
            login_record.last_failed_at = None
            login_record.save()

            create_audit_log(
                request=request,
                action_type="LOGIN",
                action="Successful login",
                description=f"User {user.username} logged in successfully.",
              )
            return redirect("home")

        else:

            # Failed login
            login_record.failed_attempts += 1
            login_record.last_failed_at = now

            if login_record.failed_attempts >= 5:

                login_record.blocked_until = (
                    now + timedelta(minutes=10)
                )

                message = (
                    "Too many failed login attempts. "
                    "Login has been temporarily blocked for 10 minutes."
                )

                messages.error(
                    request,
                    message
                )

            else:

                remaining = (
                    5 - login_record.failed_attempts
                )

                messages.error(
                    request,
                    f"Invalid username or password. "
                    f"{remaining} attempt(s) remaining."
                )

            login_record.save()

            create_audit_log(
                request=request,
                action_type="FAILED",
                action="Failed login",
                description=(
                    f"Failed login attempt for username: {username}"
                 ),
             )

    return render(
        request,
        "registration/login.html",
        {
            "form": form
        }
    )

@login_required
def custom_logout(request):

    username = request.user.username

    create_audit_log(
        request=request,
        action_type="LOGOUT",
        action="User logged out",
        description=(
            f"User {request.user.username} logged out."
        ),
    )

    logout(request)

    messages.success(
        request,
        f"{username} logged out successfully."
    )

    return redirect("login")

class CustomPasswordChangeView(PasswordChangeView):
    form_class = BootstrapPasswordChangeForm

    template_name = "registration/password_change.html"

    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        response = super().form_valid(form)

        create_audit_log(
            request=self.request,
            action_type="UPDATE",
            action="Password changed",
            description=(
                f"User {self.request.user.username} "
                f"changed their password."
            ),
            affected_object=self.request.user,
        )

        return response

class CustomPasswordChangeDoneView(
    PasswordChangeDoneView
):

    template_name = "registration/password_change_done.html"




# Registration

# REGISTER
def register_view(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            role=form.cleaned_data["role"]
            department_value = form.cleaned_data.get('department')
            UserProfile.objects.create(
                user=user,
                role=role,
                is_approved=(role == "student"),
                is_active=True
            )
            if role=="student":
                student.objects.create(
                    user=user,
                    name=user.username,
                    email=user.email,
                    age=18,
                    marks=0,
                    active=True,
                    department=department_value
                )
            create_audit_log(
                request=request,
                action_type="CREATE",
                description=(
                    f"Registered new user: "
                    f"{user.username} with role {role}."
                ),
                affected_object=user,
            )
            messages.success(
                request,"Account Created Successfully!!"
            )

            return redirect("login")
    else:
            form =RegisterForm()
    return render(request,"registration/register.html",
            {"form":form}

        )

# Role Redirect
def redirect_user_by_role(user):
    profile=getattr(user,"userprofile",None)

    if profile is None:
        return redirect("login")
    if profile.role=="admin":
        return redirect("admin_dashboard")
    if profile.role=="trainer":
        return redirect("trainer_dashboard")
    if profile.role=="student":
        return redirect("student_dashboard")
    return redirect("login")





# Dashboards-----------------------------------------------------

def home(request):
    return render(request,"website/home.html")

# Admin Dashboard
@role_required(["admin"])
def admin_dashboard(request):

    context = get_admin_dashboard_data()

    return render(
        request,
        "dashboards/admin_dashboard.html",
        context
    )



# Trainer Dashboard
@role_required(["trainer"])
def trainer_dashboard(request):

    trainer = request.user

    context = get_trainer_dashboard_data(trainer)

    return render(
        request,
        "dashboards/trainer_dashboard.html",
        context
    )


# Student Dashboard
@role_required(["student"])
def student_dashboard(request):

    students = get_object_or_404(
        student,
        user=request.user
    )

    context = get_student_dashboard_data(students)

    return render(
        request,
        "dashboards/student_dashboard.html",
        context
    )




# Trainer /Account management

@role_required(["admin"])
def trainer_list(request):

    trainers = UserProfile.objects.filter(
        role="trainer"
    ).select_related("user")

    return render(
        request,
        "admin/trainer_list.html",
        {"trainers": trainers}
    )


@login_required
@role_required(["admin"])
def approve_trainer(request, user_id):

    if request.method == "POST":

        trainer = get_object_or_404(
            UserProfile,
            user_id=user_id,
            role="trainer"
        )

        trainer.is_approved = True
        trainer.is_active = True
        trainer.save()

        trainer.user.is_active = True
        trainer.user.save()

        create_audit_log(
            request=request,
            action_type="UPDATE",
            description=(
                f"Approved trainer account: "
                f"{trainer.user.username}"
            ),
            affected_object=trainer,
        )
        

        messages.success(
            request,
            f"Trainer {trainer.user.username} approved successfully."
        )

    return redirect("admin_dashboard")


@role_required(["admin"])
def activate_account(request, user_id):

    if request.method != "POST":
     return HttpResponseForbidden(
        "This action requires a POST request."
    )

    profile = get_object_or_404(
        UserProfile,
        user_id=user_id
    )

    profile.is_active = True
    profile.save()

    profile.user.is_active = True
    profile.user.save()

    create_audit_log(
        request=request,
        action_type="UPDATE",
        description=(
            f"Activated account: "
            f"{profile.user.username}"
        ),
        affected_object=profile,
     )

    messages.success(
        request,
        f"Account {profile.user.username} activated."
    )

    return redirect("trainer_list")


@role_required(["admin"])
def deactivate_account(request, user_id):

    if request.method != "POST":
     return HttpResponseForbidden(
        "This action requires a POST request."
    )
    
    profile = get_object_or_404(
        UserProfile,
        user_id=user_id
    )

    profile.is_active = False
    profile.save()

    profile.user.is_active = False
    profile.user.save()

    create_audit_log(
        request=request,
        action_type="UPDATE",
        description=(
            f"Deactivated account: "
            f"{profile.user.username}"
        ),
        affected_object=profile,
    )

    messages.success(
        request,
        f"Account {profile.user.username} deactivated."
    )

    return redirect("trainer_list")

@role_required(["admin"])
def assign_trainer(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    # Don't allow assigning another trainer
    if course.trainer is not None:
        messages.warning(
            request,
            "A trainer is already assigned to this course."
        )
        return redirect("admin_dashboard")

    if request.method == "POST":

        form = AssignTrainerForm(request.POST)

        if form.is_valid():

            trainer = form.cleaned_data["trainer"]

            course.trainer = trainer
            course.save()

            create_audit_log(
                request=request,
                action_type="UPDATE",
                description=(
                    f"Assigned trainer "
                    f"{course.trainer.username} "
                    f"to course {course.course_name}."
                ),
                affected_object=course,
            )

            messages.success(
                request,
                f"{trainer.username} assigned to {course.course_name}."
            )

            return redirect("admin_dashboard")

    else:

        form = AssignTrainerForm()

    return render(
        request,
        "website/assign_trainer.html",
        {
            "form": form,
            "course": course,
        }
    )

# Account information 
@login_required
def account_information(request):

    return render(
        request,
        "account/account_information.html"
    )



# Student Management -------------------------------------------------
# Student List
@role_required(["admin","trainer"])
def student_list(request):
    students=student.objects.all().order_by("name")

    search=request.GET.get("search","")
    if search:
        students=students.filter(
            Q(name__icontains=search)|
            Q(email_icontains=search)
        )
    paginator=Paginator(
        students,
        10
    )
    page_number=request.GET.get("page")

    page_obj=paginator.get_page(
        page_number
    )

    return render(
        request,
        "students/student_list.html",
        {
            "students":page_obj,
            "page_obj":page_obj,
            "search":search
        }
    )

# Student Detail

@login_required
@role_required(["student", "admin", "trainer"])
def student_detail(request,pk):
    profile=getattr(
        request.user,
        "userprofile",
        None
    )

    if profile is None:
        return HttpResponseForbidden()

    # Student's record only
    if profile.role=="student":
        students=get_object_or_404(
            student,
            pk=pk,
            user=request.user
        )

    elif profile.role in ["admin","trainer"]:
        students=get_object_or_404(
            student,
            pk=pk

        )
    else:
        return HttpResponseForbidden()

    return render(request,"students/student_detail.html",{"student":students})

# Add Student
@login_required
@role_required(["admin"])
def student_create(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            students=form.save()
            create_audit_log(
                request=request,
                action_type="CREATE",
                description=(
                    f"Created student: {students.name}"
                ),
                affected_object=students,
            )

            messages.success(
                request,
                "Student added successfully!"
            )

            return redirect("student_detail",
                            pk=students.pk)

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {"form": form,
         "page_title":"Add Student",

         }
    )

@login_required
def student_update(request, pk):

    profile = getattr(
        request.user,
        "userprofile",
        None
    )
    if profile is None:
        return HttpResponseForbidden()

    if profile.role == "student":

        students = get_object_or_404(
            student,
            pk=pk,
            user=request.user
        )

        return HttpResponseForbidden(
            "Students cannot update this record."
        )

    if profile.role == "trainer":

        students = get_object_or_404(
            student,
            pk=pk
        )

    elif profile.role == "admin":

        students = get_object_or_404(
            student,
            pk=pk
        )

    else:

        return HttpResponseForbidden()

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=students
        )

        if form.is_valid():
            old_name = students.name
            old_marks = students.marks
            old_email=students.email


            form.save()
            create_audit_log(
                request=request,
                action_type="UPDATE",
                description=(
                        f"Updated student: {students.name}. "
                        f"Previous marks: {old_marks}, "
                        f"Current marks: {students.marks}"
                  ),
                affected_object=students,
             )
            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect(
                "student_detail",
                pk=students.pk
            )

    else:

        form = StudentForm(
            instance=students
        )

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "page_title": "Update Student",
            "student": students,
        }
    )

@role_required(["admin"])
def student_delete(request, pk):

    students = get_object_or_404(
        student,
        pk=pk
    )

    if request.method == "POST":
        student_name=students.name
        create_audit_log(
            request=request,
            action_type="DELETE",
            description=(
                f"Deleted student: {student_name}"
            ),
            affected_object=students,
        )
        students.delete()

        messages.success(
            request,
            "Student deleted successfully."
        )

        return redirect("student_list")

    return render(
        request,
        "students/student_detail.html",
        {
            "student": students,
            "confirm_delete": True,
        }
    )

# Marks----------------------------------------------------

@login_required
@role_required(["trainer"])
def update_course_marks(request, course_id, student_id):

    course = get_course_for_trainer(
            course_id=course_id,
            user=request.user,
        )
  

    assigned_student = get_assigned_student(
        course=course,
        student_id=student_id,
    )

    course_mark = get_course_mark(
        course=course,
        assigned_student=assigned_student,
        user=request.user,
    )

    if request.method == "POST":

        form = MarksUpdateForm(
            request.POST,
            instance=course_mark,
        )

        if form.is_valid():

            update_course_marks(
                request=request,
                course=course,
                assigned_student=assigned_student,
                form=form,
            )

            messages.success(
                request,
                "Marks updated successfully."
            )

            return redirect(
                "marks_history",
                course_id=course.id,
                student_id=assigned_student.id,
            )

    else:

        form = MarksUpdateForm(
            instance=course_mark,
        )

    return render(
        request,
        "students/marks_update.html",
        {
            "form": form,
            "course": course,
            "student": assigned_student,
            "course_mark": course_mark,
        },
    )



@login_required
def marks_history(request, course_id, student_id):

    (
        course,
        assigned_student,
        course_mark,
        history,
    ) = get_marks_history_for_user(
        user=request.user,
        course_id=course_id,
        student_id=student_id,
    )

    return render(
        request,
        "students/marks_history.html",
        {
            "course": course,
            "student": assigned_student,
            "course_mark": course_mark,
            "history": history,
        }
    )

# Feedback -----------------------------------------------

@login_required
@role_required(["trainer"])
def feedback_create(request, course_id, student_id):

    course = get_course_for_feedback(
        course_id=course_id,
        user=request.user,
    )

    assigned_student = get_assigned_student_for_feedback(
        course=course,
        student_id=student_id,
    )

    if request.method == "POST":

        form = FeedbackForm(
            request.POST
        )

        if form.is_valid():

            feedback = create_feedback(
                user=request.user,
                course=course,
                assigned_student=assigned_student,
                form=form,
            )

            create_audit_log(
                request=request,
                action_type="CREATE",
                description=(
                    f"Created feedback for "
                    f"{assigned_student.name} in "
                    f"{course.course_name}. "
                    f"Rating: {feedback.rating}/5"
                ),
                affected_object=feedback,
            )

            messages.success(
                request,
                "Feedback added successfully."
            )

            return redirect(
                "feedback_list"
            )

    else:

        form = FeedbackForm()

    return render(
        request,
        "students/feedback_form.html",
        {
            "form": form,
            "course": course,
            "student": assigned_student,
            "page_title": "Add Feedback",
        }
    )



@login_required
@role_required(["trainer"])
def feedback_edit(request, feedback_id):

    feedback = get_feedback_for_edit(
        feedback_id=feedback_id,
        user=request.user,
    )

    if request.method == "POST":

        form = FeedbackForm(
            request.POST,
            instance=feedback,
        )

        if form.is_valid():

            feedback = update_feedback(
                feedback=feedback,
                form=form,
            )

            create_audit_log(
                request=request,
                action_type="UPDATE",
                description=(
                    f"Updated feedback for "
                    f"{feedback.student.name} in "
                    f"{feedback.course.course_name}. "
                    f"Rating: {feedback.rating}/5"
                ),
                affected_object=feedback,
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
            instance=feedback
        )

    return render(
        request,
        "students/feedback_form.html",
        {
            "form": form,
            "feedback": feedback,
            "course": feedback.course,
            "student": feedback.student,
            "page_title": "Edit Feedback",
        }
    )


@login_required
def feedback_list(request):

    feedback_queryset = get_feedback_for_user(
        user=request.user,
    )

    return render(
        request,
        "students/feedback_list.html",
        {
            "feedback_list": feedback_queryset,
        }
    )


# Audit log list ----------------------------------------
@login_required
@role_required(["admin"])
def audit_log_list(request):

    form = AuditLogFilterForm(request.GET or None)

    logs = AuditLog.objects.select_related(
        "user"
    ).order_by("-created_at")

    if form.is_valid():

        search = form.cleaned_data.get("search")
        action_type = form.cleaned_data.get("action_type")
        date_from = form.cleaned_data.get("date_from")
        date_to = form.cleaned_data.get("date_to")

        if search:
            logs = logs.filter(
                Q(user__username__icontains=search)
                | Q(description__icontains=search)
                | Q(action__icontains=search)
            )

        if action_type:
            logs = logs.filter(
                action_type=action_type
            )

        if date_from:
            logs = logs.filter(
                created_at__date__gte=date_from
            )

        if date_to:
            logs = logs.filter(
                created_at__date__lte=date_to
            )

    paginator = Paginator(logs, 20)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "admin/audit_logs.html",
        {
            "logs": page_obj,
            "page_obj": page_obj,
            "form": form,
        }
    )
