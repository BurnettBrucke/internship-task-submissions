from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm
from django.contrib import messages


def home(request):
    company_name = "Bug Network Private Limited"

    return render(
        request,
        'home.html',
        {'company_name': company_name}
    )


def about(request):
    return HttpResponse("This is the About Page")


def student_list(request):
    students = Student.objects.all()

    total_students = Student.objects.count()

    active_students = Student.objects.filter(active=True).count()

    return render(
        request,
        'student_list.html',
        {
            'students': students,
            'total_students': total_students,
            'active_students': active_students,
        }
    )

def add_student(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')

    else:
        form = StudentForm()

    return render(
        request,
        'add_student.html',
        {'form': form}
    )