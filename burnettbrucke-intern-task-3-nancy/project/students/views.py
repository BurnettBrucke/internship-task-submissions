from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import StudentForm
from .models import Student


def home(request):
    company = "Bug Network Private Limited"
    return render(request, "home.html", {"company": company})  # context


def about(request):
    return HttpResponse("<h1>About Page</h1><p>This is About Page.</p>")


def student_list(request):
    students = Student.objects.all()
    total_students = students.count()
    active_students = students.filter(is_active=True).count()
    context = {
        "students": students,
        "total_students": total_students,
        "active_students": active_students,
    }
    return render(request, "students/student_list.html", context)


def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "students/add_student.html", {"form": form})
