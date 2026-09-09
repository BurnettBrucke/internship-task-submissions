from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Department, Course
from .forms import StudentForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.db.models import Avg, Count, Q


# Home Page
def home(request):
    company_name = "Bug Network Private Limited"

    return render(
        request,
        'home.html',
        {'company_name': company_name}
    )


# About Page
def about(request):
    return render(request, 'about.html')


# User Registration
def register_user(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Registration successful!"
            )

            return redirect('dashboard')

    else:
        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


# User Login
def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)

                messages.success(
                    request,
                    "Login successful!"
                )

                return redirect('dashboard')

    else:
        form = AuthenticationForm()

    return render(
        request,
        'login.html',
        {'form': form}
    )


# User Logout
def logout_user(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully!"
    )

    return redirect('login')


# Display All Students
@login_required
def student_list(request):
    students = Student.objects.annotate(
        course_count=Count('courses')
    )

    # Search
    search = request.GET.get('search', '')

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(courses__course_name__icontains=search)
        ).distinct()

    # Department filter
    department_id = request.GET.get('department', '')

    if department_id:
        students = students.filter(department_id=department_id)

    # Course filter
    course_id = request.GET.get('course', '')

    if course_id:
        students = students.filter(courses__id=course_id).distinct()

    # Active status filter
    status = request.GET.get('status', '')

    if status == 'active':
        students = students.filter(active=True)
    elif status == 'inactive':
        students = students.filter(active=False)

    # Pass / Fail filter
    result = request.GET.get('result', '')

    if result == 'pass':
        students = students.filter(marks__gte=40)
    elif result == 'fail':
        students = students.filter(marks__lt=40)

    departments = Department.objects.all()
    courses = Course.objects.all()

    total_students = Student.objects.count()
    active_students = Student.objects.filter(active=True).count()

    return render(request, 'student_list.html', {
        'students': students,
        'total_students': total_students,
        'active_students': active_students,
        'departments': departments,
        'courses': courses,
        'search': search,
        'department_id': department_id,
        'course_id': course_id,
        'status': status,
        'result': result,
    })

@login_required
def dashboard(request):
    total_students = Student.objects.count()

    total_active_students = Student.objects.filter(active=True).count()

    total_departments = Department.objects.count()

    total_courses = Course.objects.count()

    average_marks = Student.objects.aggregate(
        average=Avg('marks')
    )['average']

    highest_student = Student.objects.order_by('-marks').first()

    recent_students = Student.objects.order_by('-joined_date')[:5]

    return render(request, 'dashboard.html', {
        'total_students': total_students,
        'total_active_students': total_active_students,
        'total_departments': total_departments,
        'total_courses': total_courses,
        'average_marks': average_marks,
        'highest_student': highest_student,
        'recent_students': recent_students,
    })

# Display One Student's Details
@login_required
def student_detail(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    return render(
        request,
        'student_detail.html',
        {'student': student}
    )


# Add New Student
@login_required
def add_student(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student added successfully!"
            )

            return redirect('student_list')

    else:
        form = StudentForm()

    return render(
        request,
        'student_form.html',
        {
            'form': form,
            'title': 'Add Student'
        }
    )


# Edit Existing Student
@login_required
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student updated successfully!"
            )

            return redirect(
                'student_detail',
                id=student.id
            )

    else:
        form = StudentForm(
            instance=student
        )

    return render(
        request,
        'student_form.html',
        {
            'form': form,
            'title': 'Edit Student'
        }
    )


# Delete Student
@login_required
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':

        student.delete()

        messages.success(
            request,
            "Student deleted successfully!"
        )

        return redirect('student_list')

    return render(
        request,
        'student_confirm_delete.html',
        {
            'student': student
        }
    )

'''
user-id = admin
password = admin12345
'''