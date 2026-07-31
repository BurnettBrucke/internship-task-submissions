from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Student, Department, Course, StudentProfile, UserProfile,AuditLog
from .form import StudentForm,StudentProfileForm
from django.db.models import Avg,Q 
from.decorator import role_required
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .utility import create_audit_log
from django.core.paginator import Paginator



# home page
def home(request):
    return render(request,'home.html')


# register page
def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']


        if User.objects.filter(username=username).exists():
            messages.error(request,"user already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request,"email already exixts")
            return redirect('register')

        if password!=confirm_password:
            messages.error(request,"passwords do not match")
            return redirect('register')

        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request,error)
            return redirect('register')

        new_user=User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(user=new_user,role="STUDENT")
        messages.success(request,'Account created succesfully.')
        return redirect('login')
        
    return render(request,"register.html")



from django.utils import timezone
from datetime import timedelta

# login page
def login_user(request):
    print("LOGIN VIEW CALLED")
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']


        db_user=User.objects.filter(username=username).first()

        if db_user :
            print("Locked Until:", db_user.profile.locked_until)
            print("Current Time:", timezone.now())
            if(db_user.profile.locked_until and 
               db_user.profile.locked_until > timezone.now()):
                print("account locked")
                print("Locked Until:", db_user.profile.locked_until)
                messages.error(request,"Your account is locked. Please try again after 10 minutes.")
                return redirect('home')
        
        print("DB USER:", db_user)
        user=authenticate(request,username=username,password=password)
        print("Username:", username)
        print("Password:", password)
        print("User:", user)

        if user is not None:
            user.profile.failed_attempts=0
            user.profile.locked_until = None
            user.profile.save()
            login(request,user)
            create_audit_log(
                request=request,
                user=user,
                action="LOGIN",
                description=f"{user.username} logged in successfully"
            )
            messages.success(request, "Login successful.")

            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)

            if user.profile.role=="ADMIN":
                return redirect('admin_dashboard')

            elif user.profile.role=="TRAINER":
                return redirect('trainer_dashboard')

            elif user.profile.role=="STUDENT":
                return redirect('dashboard')
        else:
            if db_user:
                create_audit_log(
                                request=request,
                                user=user,
                                action="FAILED_LOGIN",
                                description=f"loggin attempt fails for {user.username}"
                            )
                db_user.profile.failed_attempts+=1
                print("Failed Attempts:", db_user.profile.failed_attempts)
                if db_user.profile.failed_attempts>=5:
                    db_user.profile.locked_until=(
                        timezone.now()+timedelta(minutes=10)
                    )
                    print("Locked Until:", db_user.profile.locked_until)

                db_user.profile.save()
            messages.error(request,"invalid user name or password")
            return redirect("home")  
    return render(request,'login.html')


# logout 
def logout_user(request):
    create_audit_log(
        request=request,
        user=request.user,
        action="LOGOUT",
        description=f"{request.user.username} logged out")
    logout(request)
    messages.success(request,"logout succesfully")
    return redirect('home')

# admin dashboard
@login_required
@role_required("ADMIN")
def admin_dashboard(request):
   students=Student.objects.count()

   courses=Course.objects.count()

   dept=Department.objects.count()

   trainers=UserProfile.objects.filter(role='TRAINER').count()

   highest=Student.objects.order_by('-marks').first()

   recent=Student.objects.order_by("-join_date")[:5]
   context={
       "students":students,
       "courses":courses,
       "dept":dept,
       "trainers":trainers,
       "highest":highest,
       "recent":recent
       }
   return render(request,'admin-dashboard.html',context)


# trainer dashboard
@login_required
@role_required("TRAINER")
def trainer_dashboard(request):
    trainer=request.user.profile
    courses=Course.objects.filter(
        assigned_trainer__trainer=trainer).distinct()
    students = Student.objects.filter(
        course__assigned_trainer__trainer=trainer
    ).select_related(
        "department"
    ).prefetch_related(
        "course").distinct()

    context={
        "students":students,
        "courses":courses,
        "total_students":students.count(),
        "total_course":courses.count()
    }
    return render(request,'trainer-dashboard.html',context)

# dashboard
@login_required
@role_required("STUDENT")
def dashboard(request):
    student=request.user.student
    print(student)
    context={
        "student":student
    }
    return render(request,'dashboard.html',context)

# def dashboard(request):
#     total_std=Student.objects.count()

#     active_std=Student.objects.filter(active_status='pass').count()

#     total_dept=Department.objects.count()

#     total_course=Course.objects.count()

#     avg_marks=Student.objects.aggregate(Avg('marks'))

#     highest_std=Student.objects.order_by('-marks').first()

#     recently_joined=Student.objects.order_by("-join_date")[:5]

#     context={
#         "total_students":total_std,
#         "active_students":active_std,
#         'total_departments':total_dept,
#         'total_courses':total_course,
#         "highest_student":highest_std,
#         "recent_students":recently_joined,
#         "average_marks": avg_marks
#     }

#     return render(request,'dashboard.html',context)




# student list
@login_required
def student_list(request):
    print(request.user)
    print(request.user.is_authenticated)
    students = Student.objects.all()

    context = {
        "students": students
    }
    return render(request, "student_list.html", context)


# one student detail 
@login_required
def student_detail(request, id):

    student = get_object_or_404(Student, id=id)
    if request.user.profile.role == "STUDENT":
        if request.user.student != student:
            return HttpResponseForbidden("403 Forbidden")

    context = {
        "student": student
    }

    return render(request, "student_detail.html", context)

# add student 
@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        profile_form = StudentProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            student=form.save(commit=False)
            student.active_status='pass' if student.marks>=40 else "fail"
            student.save()
            form.save_m2m()

            profile=profile_form.save(commit=False)

            profile.student=student
            profile.save()
            create_audit_log(
                    request=request,
                    user=request.user,
                    action="CREATED",
                    object_name=student.name,
                    description=f"created student:{student.name}"
                )
            messages.success(request, "Student added successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()
        profile_form=StudentProfileForm()

    context = {"form": form,
               "profile_form":profile_form}

    return render(request, "student_form.html", context)

# edit or update student 
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    profile, created = StudentProfile.objects.get_or_create(
    student=student)

    if request.method == "POST":

        form = StudentForm(request.POST, instance=student)
        profile_form=StudentProfileForm(request.POST,instance=profile)

        if form.is_valid() and profile_form.is_valid():

            form.save()
            profile_form.save()

            create_audit_log(
                            request=request,
                            user=request.user,
                            action="UPDATE",
                            object_name=student.name,
                            description=f"updated student:{student.name}"
                            )

            messages.success(request, "Student updated successfully.")

            return redirect("student_list")

    else:

        form = StudentForm(instance=student)
        profile_form=StudentProfileForm(instance=profile)

    context = {
        "form": form,
        "profile_form":profile_form
    }

    return render(request, "student_form.html", context)


# delete student 
@login_required
def delete_student(request, id):
    print(request.user)
    print(request.user.is_staff)
    if request.user.is_staff:

        student = get_object_or_404(Student, id=id)
        

        if request.method == "POST":

            student.delete()
            create_audit_log(
                request=request,
                user=request.user,
                action="DELETE",
                object_name=student.name,
                description=f"Deleted student {student.name}"
            )

            messages.success(request, "Student deleted successfully.")

            return redirect("student_list")
    else:
        messages.error(request,"you are not allowed to delete")
        return redirect('student_list')

    context = {
        "student": student
    }

    return render(request, "student_confirm_delete.html", context)


# change password
@login_required
def change_password(request):

    if request.method=='POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"password change successfully")
            if user.profile.role=="ADMIN":
                return redirect('admin_dashboard')
            
            elif user.profile.role=="TRAINER":
                return redirect('trainer_dashboard')
            
            elif user.profile.role=="STUDENT":
                return redirect('dashboard')
        else:
            messages.error(request,"enter correct details")
            
    else:
        form=PasswordChangeForm(request.user)

    context={
        "form":form
    }
    return render(request,'change_password.html',context)


@login_required
@role_required("ADMIN")
def user_list(request):
    users=User.objects.all()
    context={
        "users":users
    }

    return render(request,'user_list.html',context)

def toggle_status(request,user_id):
    user=get_object_or_404(User,id=user_id)
    user.is_active=not user.is_active
    if user.is_active:
        create_audit_log(
                        request=request,
                        user=request.user,
                        action="ACTIVATE",
                        object_name=user.username,
                        description=f"Deleted student {user.username}"
                    )
    else:
        create_audit_log(
                    request=request,
                    user=request.user,
                    action="DEACTIVATE",
                    object_name=user.username,
                    description=f"Deleted student {user.username}"
                )
    user.save()
    return redirect('user_list')

def make_trainer(request,user_id):
    user=get_object_or_404(User,id=user_id)
    user.profile.role="TRAINER"
    user.profile.save()
    return redirect('user_list')

def remove_trainer(request,user_id):
    user=get_object_or_404(User,id=user_id)
    user.profile.role="STUDENT"
    user.profile.save()
    return redirect('user_list')

@login_required
@role_required("ADMIN")
def audit_list(request):
    logs=AuditLog.objects.all().order_by('-created_at')
    search=request.GET.get("search")
    print("search:",search)
    if search:
        logs=logs.filter(
            Q(user__username__icontains=search)|
            Q(action__icontains=search)|
            Q(object_name__icontains=search)
        )

        action=request.GET.get("action")
        if action:
            logs=logs.filter(action=action)
        print(logs)

    paginator=Paginator(logs,5)
    page_number=request.GET.get("page")
    logs=paginator.get_page(page_number)
    context={
        "logs":logs,
        "search":search
    }
    return render(request,'audit_list.html',context)



from django.core.exceptions import PermissionDenied
# to check custom error pages 
def forbidden(request):
    raise PermissionDenied

def server_error(request):
    x = 10 / 0