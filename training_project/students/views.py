from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg, Max, Q
from . models import Student, Department, Course, StudentProfile
from . forms import StudentForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("student_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("student_list")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


def home(request):
    welcome_msg = 'Welcome to Bug Network Private Limited Training Program'
    context = {'welcome msg': welcome_msg}
    return render(request, 'students/home.html', context)

def about(request):
    message = 'Welcome to the About Page'
    context = {'welcome msg': message}
    return HttpResponse('This is About Page', context)


@login_required
def student_list(request):
    active_students = Student.objects.filter(active_status=True)
    total_students = Student.objects.all().count()    

    students = Student.objects.select_related("department").prefetch_related("course").annotate(course_count=Count("course"))

    department = request.GET.get("department")
    if department:
        students = students.filter(department__id=department)


    course = request.GET.get("course")
    if course:
        students = students.filter(course__id=course)


    active = request.GET.get("active_status")
    if active != "" and active is not None:
        students = students.filter(active_status=(active == "True"))


    status = request.GET.get("status")
    if status == "pass":
        students = students.filter(marks__gte=40)

    elif status == "fail":
        students = students.filter(marks__lt=40)


    search = request.GET.get("search")
    if search:
        students = students.filter(Q(name__icontains=search) | Q(email__icontains=search) |
            Q(courses__course_name__icontains=search)).distinct()

    context = {
        "students": students,
        "departments": Department.objects.all(),
        "courses": Course.objects.all(),
        "active_students": active_students,
        "total_students": total_students
    }
    return render(request,"students/student_list.html",context,)

 
# Display one student
@login_required
def student_detail(request, id):
    student = get_object_or_404(Student, pk=id)
    return render(request,"students/student_detail.html",{"student": student})
 
# Add student
@login_required
def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "students/student_form.html", {"form": form})


@login_required
def student_edit(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)
    return render(request, "students/student_form.html", {"form": form})


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
@login_required
def student_delete(request, id):
    student = get_object_or_404(Student, pk=id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")

    return render(request, "students/student_confirm_delete.html",{"student": student})


def dashboard(request):
    context = {
        "total_students": Student.objects.count(),

        "active_students":Student.objects.filter(active_status=True).count(),

        "total_departments":Department.objects.count(),

        "total_courses":Course.objects.count(),

        "average_marks":Student.objects.aggregate(Avg("marks"))["marks__avg"],

        "highest_student":Student.objects.order_by("-marks").first(),

        "recent_students":Student.objects.order_by("-joined_date")[:5],
    }

    return render(request,"students/dashboard.html",context,)

