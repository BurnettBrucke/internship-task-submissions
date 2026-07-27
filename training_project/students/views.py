from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from .form import StudentForm,StudentProfileForm
from django.db.models import Avg

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

        if password!=confirm_password:
            messages.error(request,"password do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request,"user already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request,'Account created succesfully.')
        return redirect('login')
        
    return render(request,"register.html")


# login page
def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        # user = authenticate(request, username=username, password=password)

        print("Username:", username)
        print("Password:", password)
        print("User:", user)

        if user is not None:
            login(request,user)
            return redirect('student_list')
        else:
            messages.error(request,"invalid user name or password")
            return redirect("home")  
    return render(request,'login.html')


# logout 
def logout_user(request):
    logout(request)
    messages.success(request,"logout succesfully")
    return redirect('home')

# dashboard
def dashboard(request):
    total_std=Student.objects.count()

    active_std=Student.objects.filter(active_status='pass')

    total_dept=Department.objects.count()

    total_course=Course.objects.count()

    avg_marks=Student.objects.aaggregate(Avg('marks'))

    highest_std=Student.objects.order_by('-marks').first()

    recently_joined=Student.objects.order_by("-join_date")[:5]

    context={
        "total_students":total_std,
        "active_student":active_std,
        'total_department':total_dept,
        'total_course':total_course,
        "highest_student":highest_std,
        "recent_std":recently_joined
    }

    return render(request,'dashboard.html',context)




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

            messages.success(request, "Student deleted successfully.")

            return redirect("student_list")
    else:
        messages.error(request,"you are not allowed to delete")
        return redirect('student_list')

    context = {
        "student": student
    }

    return render(request, "student_confirm_delete.html", context)