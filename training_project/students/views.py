from django.shortcuts import render , redirect
from django.http import HttpResponse 
from .form import StudentForm
from .models import Student
from django.contrib import messages
# Create your views here.

def home(request):
    context = {'company_name' : "Bug Network private Limited"}
    return render(request ,"home.html" , context) 

def about(request):
    return render(request , "about.html")


def student_list(request):
    students = Student.objects.all()

    total_students = students.count()
    active_students = students.filter(active=True).count()

    return render(
        request,
        "student_list.html",
        {
            "students": students,
            "total_students": total_students,
            "active_students": active_students,
        }
    )


def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()

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
    {
        "form": form
    }

)