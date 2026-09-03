from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Student
from .forms import StudentForm
from django.contrib import messages


def home(request):
    company_name = "Bug Network Private Limited"

    return render(
        request,
        'students/home.html',
        {'company_name': company_name}
    )

def about(request):
    return HttpResponse("""
        <h1>About Page</h1>
        <p>This is the training program website.</p>
    """)


def student_list(request):
    students = Student.objects.all()
    total_students = Student.objects.count()
    active_students = Student.objects.filter(active_status=True).count()

    return render(
        request,
        'students/student_list.html',
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
            messages.success(request, 'Student added successfully!')
            return redirect('/students/')
    else:
        form = StudentForm()

    return render(
        request,
        'students/add_student.html',
        {'form': form}
    )