from django.shortcuts import redirect,render,get_object_or_404 # type: ignore
from .form import StudentForm
from .models import student
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg,Max,Min


# Create your views here.
def home(request):
    comp={ "company_name":"Burnett"}
    return render(request,"website/home.html",comp)

def about(request):
    return render(request,"website/about.html")

@login_required
def student_list(request):
    students = student.objects.all()

    # Search
    search = request.GET.get("search")

    if search:
        students = students.filter(
            name__icontains=search
        ) | students.filter(
            email__icontains=search
        ) | students.filter(
            course__icontains=search
        )

    # Department filter
    department = request.GET.get("department")

    if department:
        students = students.filter(department=department)

    # Course filter
    course = request.GET.get("course")

    if course:
        students = students.filter(course=course)

    # Active status filter
    active = request.GET.get("active")

    if active == "active":
        students = students.filter(active=True)

    elif active == "inactive":
        students = students.filter(active=False)

    # Pass / Fail filter
    status = request.GET.get("status")

    if status == "pass":
        students = students.filter(marks__gte=40)

    elif status == "fail":
        students = students.filter(marks__lt=40)

    context = {
        "students": students,

        "departments": student.objects.values_list(
            "department", flat=True
        ).distinct(),

        "courses": student.objects.values_list(
            "course", flat=True
        ).distinct(),

        "selected_department": department,
        "selected_course": course,
        "selected_active": active,
        "selected_status": status,
        "search": search,
    }

    return render(request,("website/student_list.html"),context)

@login_required
def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student added successfully!"
            )

            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "website/add_student.html",
        {"form": form}
    )

@login_required
def update_student(request,id):
    students = get_object_or_404(student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=students)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = StudentForm(instance=students)

    return render(request,'website/update_student.html',{'form':form})

@login_required
def delete_student(request, id):
    students = get_object_or_404(student, id=id)

    if request.method == 'POST':
        students.delete()
        return redirect('student_list')

    return render(
        request,
        'website/delete_confirmation.html',
        {'students': students}
    )

@login_required
def single_student(request,id=id):

    students=get_object_or_404(student,id=id)

    return render(request,'website/single_student.html',{'students':students})


def register_user(request):
    if request.method == "POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exist')
            return redirect('register')
        user=User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request,"Registration Succeffull. Please Login...")
        return redirect('login')
    return render(request,'website/register.html')

def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request,user)

            messages.success(request,f"Welcome {user.username}")
            return redirect('student_list')
        else:
            messages.error(request,"Invalid email or username")
            # return redirect(request,'website/login.html')

    return render(request,'website/login.html')


def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out!!")
    return redirect("login")

def dashboard(request):
     
    # Total Students
     total_students=student.objects.count()

    #  Total Acivte Students
     active_students=student.objects.filter(active=True).count()
    #  Total Departments
     total_departments=student.objects.values('department').distinct().count()

    # Total Courses
     total_courses=student.objects.values('courses').distinct().count()

    # Average Students mark
     average_marks= (student.objects.aggregate(average=Avg("marks"))["average"])
    # Highest Scoring Student
     highest_student=student.objects.order_by("-marks").first()

    # Recently Joined Person
     recent_students=student.objects.order_by('-joined_date')[:5]
     context = {
        "total_students": total_students,
        "active_students": active_students,
        "total_departments": total_departments,
        "total_courses": total_courses,
        "average_marks": average_marks,
        "highest_student": highest_student,
        "recent_students": recent_students,
       }
     return render(request,'website/dashboard.html',context)