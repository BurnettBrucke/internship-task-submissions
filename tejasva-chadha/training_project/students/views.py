from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Student
from .forms import StudentForm

# Create your views here.
def home(request):
    context = {
        'company_name': 'Bug Network Private Limited'
    }
    return render(request, 'students/home.html', context)

def about(request):
    html_content = "<h1>About Page</h1><p>Welcome to the About page of our Django application!</p>"
    return HttpResponse(html_content)

def student_list(request):
    students = Student.objects.all().order_by('-joined_date')
    total_count = students.count()
    active_count = students.filter(active_status=True).count()
    
    context = {
        'students': students,
        'total_count': total_count,
        'active_count': active_count,
    }
    return render(request, 'students/student_list.html', context)

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'students/add_student.html', {'form': form})

