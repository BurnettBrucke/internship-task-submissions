from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse 
from .form import StudentForm
from .models import Student
from django.contrib import messages
from .services import send_mail
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

def student_detail(request , id):
    student = get_object_or_404(Student , id = id)
    return render(
        request , 
        "student_detail.html",
        {
            "student" : student
        }
    )

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

            return redirect("student_detail", id=student.id)

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

def delete_student(request , id):
    student = get_object_or_404(Student , id = id)
    if request.method == "POST":
        student.delete()
        messages.success(request , "Student delete successfully.")

        return redirect("students_list")

    return render(
        request , "student_confirm_delete.html" , {"student" : student}
    )