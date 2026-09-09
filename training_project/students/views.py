from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import StudentForm, RegistrationForm

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import Student, Department, Course
from django.contrib.auth.models import User
from django.db.models import Q


from .services import get_dashboard_data, get_filtered_students

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Registration successful!'
            )

            return redirect('student_list')

    else:
        form = RegistrationForm()

    return render(
        request,
        'students/register.html',
        {'form': form}
    )

def user_login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)

            user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if user is not None:
                login(request, user)

                messages.success(
                    request,
                    'Login successful!'
                )

                return redirect('student_list')

            else:
                messages.error(
                    request,
                    'Invalid email or password.'
                )

        except User.DoesNotExist:
            messages.error(
                request,
                'Invalid email or password.'
            )

    return render(
        request,
        'students/login.html'
    )

def user_logout(request):
    logout(request)

    messages.success(
        request,
        'You have been logged out successfully!'
    )

    return redirect('login')

def home(request):
    company_name = "Bug Network Private Limited"

    return render(
        request,
        'students/home.html',
        {'company_name': company_name}
    )


def about(request):
    return render(request, 'students/about.html')

@login_required(login_url='login')
def dashboard(request):

    dashboard_data = get_dashboard_data()

    return render(
        request,
        'students/dashboard.html',
        dashboard_data
    )

@login_required(login_url='login')
def student_list(request):

    students = get_filtered_students(request.GET)

    # Statistics
    total_students = Student.objects.count()

    active_students = Student.objects.filter(
        active_status=True
    ).count()

    # Dropdown data
    departments = Department.objects.all()
    courses = Course.objects.all()

    return render(
        request,
        'students/student_list.html',
        {
            'students': students,
            'total_students': total_students,
            'active_students': active_students,
            'departments': departments,
            'courses': courses,
        }
    )

# Display one student
@login_required(login_url='login')
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    return render(
        request,
        'students/student_detail.html',
        {'student': student}
    )


# Add student
@login_required(login_url='login')
def add_student(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Student added successfully!'
            )

            return redirect('student_list')

    else:
        form = StudentForm()

    return render(
        request,
        'students/student_form.html',
        {
            'form': form,
            'title': 'Add Student'
        }
    )


# Edit student
@login_required(login_url='login')
def edit_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Student updated successfully!'
            )

            return redirect('student_detail', pk=student.pk)

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'students/student_form.html',
        {
            'form': form,
            'title': 'Edit Student'
        }
    )

@login_required(login_url='login')
def delete_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()

        messages.success(
            request,
            'Student deleted successfully!'
        )

        return redirect('student_list')

    return render(
        request,
        'students/student_confirm_delete.html',
        {'student': student}
    )

