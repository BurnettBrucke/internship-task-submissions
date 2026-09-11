from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse 
from .form import StudentForm
from .models import Student , Department , Course , StudentProfile
from django.contrib import messages
from .services import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg , Max , Q , Count
# Create your views here.

def home(request):
    context = {'company_name' : "Bug Network private Limited"}
    return render(request ,"home.html" , context) 

def about(request):
    return render(request , "about.html")

@login_required
def student_list(request):

    students = Student.objects.all()

    # Search
    search = request.GET.get("search", "").strip()

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(course__course_name__icontains=search)
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
            course__id=course
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
        students = students.filter(marks__gte=40)

    elif result == "fail":
        students = students.filter(marks__lt=40)

    # Remove duplicates from ManyToMany filtering
    students = students.distinct()

    # Course count
    students = students.annotate(
        course_count=Count("course", distinct=True)
    )

    # Statistics
    total_students = students.count()

    active_students = students.filter(active=True).count()

    # Dropdown data
    departments = Department.objects.all()

    courses = Course.objects.all()

    return render(
        request,
        "student_list.html",
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
@login_required
def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save()
            send_mail(student)

            messages.success(
                request , 
                "Student added sucessfully."
            )

            return redirect("students_list")

    else:
        form = StudentForm()
    return render(
    request,
    "add_student.html",
    {"form": form}

)

@login_required
def student_detail(request , id):
    student = get_object_or_404(Student , id = id)
    return render(
        request , 
        "student_detail.html",
        {
            "student" : student
        }
    )
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("student_detail", id=student.id) # type: ignore

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "edit_student.html",
        {
            "form": form,
            "student": student
        }
    )

@login_required
def delete_student(request , id):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to delete students."
        )
        return redirect("students_list")

    student = get_object_or_404(Student , id = id)
    if request.method == "POST":
        student.delete()
        messages.success(request , "Student delete successfully.")

        return redirect("students_list")

    return render(
        request , "student_confirm_delete.html" , {"student" : student}
    )

def register(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request , "Username & Password is requried.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists please try to login.")
                return redirect("register")

        User.objects.create_user(
            username = username,
            password = password
        )

        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "register.html")

def login_backend(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request , username= username , password= password)

        if user is not None:
            login(request , user)
            messages.success(request , "Login successful.")
            return redirect("home")
        
        messages.error(request,"You don't have id please register.")

    return render(request, "login.html")

def logout_backend(request):
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")

@login_required
def dashboard(request):

    total_students = Student.objects.count()

    active_students = Student.objects.filter(active = True).count()

    total_departments = Department.objects.count()

    total_courses = Course.objects.count()

    average_marks = Student.objects.aggregate(average_marks = Avg("marks"))["average_marks"]

    highest_students = Student.objects.order_by("-marks")[:3]

    recent_students =  Student.objects.order_by("-joined_date")[:3] 
    return render(
        request,
        "dashboard.html",
        {
            "total_students": total_students,
            "active_students": active_students,
            "total_departments": total_departments,
            "total_courses": total_courses,
            "average_marks": average_marks,
            "highest_students": highest_students,
            "recent_students": recent_students,
        }
    )

