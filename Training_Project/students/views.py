from django.shortcuts import render, redirect, get_object_or_404
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


# Display all students
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


# Display one student's details
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    return render(
        request,
        'student_detail.html',
        {'student': student}
    )


# Add a new student
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
        'student_form.html',
        {'form': form, 'title': 'Add Student'}
    )


# Edit an existing student
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_detail', id=student.id)

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'student_form.html',
        {'form': form, 'title': 'Edit Student'}
    )


# Delete a student
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('student_list')

    return render(
        request,
        'student_confirm_delete.html',
        {'student': student}
    )