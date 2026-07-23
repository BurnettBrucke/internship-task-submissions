from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Student
from django.contrib import messages
from .form import StudentForm


def home(request):
    data = {
        'company': 'Bug Network Private Limited Training Program'
    }
    return render(request, 'home.html', data)


def about(request):
    return HttpResponse("<h1>About Page</h1>")

def student_list(request):
    students=Student.objects.all()#gives every student in the database
    
    active_students=Student.objects.filter(active=True).count()#gives us active student
    total_students=Student.objects.count()#gives us total students
    
    context={#used to pass data from the view to the template.
        "students":students,
        "active_students":active_students,
        "total_students":total_students,
    }
    
    return render(request,"students/student_list.html",context)\
        
def add_student(request):
    
    form = StudentForm()
    
    if request.method=="POST":
        form=StudentForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Student Added Succesfully!")
            return redirect("student_list")
    

    return render(
        request,
        "students/add_student.html",
        {"form": form},
    )