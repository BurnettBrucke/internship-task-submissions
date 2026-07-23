from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Student
from .form import StudentForm

def student_list(request):

    students = Student.objects.all()

    context = {
        "students": students
    }
    return render(request, "student_list.html", context)


def student_detail(request, id):

    student = get_object_or_404(Student, id=id)

    context = {
        "student": student
    }

    return render(request, "student_detail.html", context)

# add student 
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully.")
            return redirect("student_list")
        else:
             form = StudentForm()

    context = {"form": form}

    return render(request, "student_form.html", context)

# edit or update student 
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":

        form = StudentForm(request.POST, instance=student)

        if form.is_valid():

            form.save()

            messages.success(request, "Student updated successfully.")

            return redirect("student_list")

    else:

        form = StudentForm(instance=student)

    context = {
        "form": form
    }

    return render(request, "student_form.html", context)

def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        student.delete()

        messages.success(request, "Student deleted successfully.")

        return redirect("student_list")

    context = {
        "student": student
    }

    return render(request, "student_confirm_delete.html", context)