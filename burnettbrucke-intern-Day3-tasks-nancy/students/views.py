from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Max, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, StudentForm
from .models import Course, Department, Student


def home(request):
    company = "Bug Network Private Limited"
    return render(request, "home.html", {"company": company})  # context


def about(request):
    return HttpResponse("<h1>About Page</h1><p>This is About Page.</p>")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome!")
            return redirect("student_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


# ---------------------------------------------------------------------------
# Student CRUD  
# ---------------------------------------------------------------------------

@login_required
def student_list(request):
    students = (
        Student.objects.select_related('department')
        .prefetch_related('courses')
        .all()
    )

    # --- filtering ---
    department_id = request.GET.get('department', '')
    course_id = request.GET.get('course', '')
    status = request.GET.get('status', '')
    result = request.GET.get('result', '')
    query = request.GET.get('q', '').strip()

    if department_id:
        students = students.filter(department_id=department_id)
    if course_id:
        students = students.filter(courses__id=course_id)
    if status == 'active':
        students = students.filter(is_active=True)
    elif status == 'inactive':
        students = students.filter(is_active=False)
    if result == 'pass':
        students = students.filter(marks__gte=40)
    elif result == 'fail':
        students = students.filter(marks__lt=40)
    if query:
        students = students.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(courses__name__icontains=query)
        )

    students = students.distinct()

    context = {
        "students": students,
        "total_students": Student.objects.count(),
        "active_students": Student.objects.filter(is_active=True).count(),
        "departments": Department.objects.all(),
        "courses": Course.objects.all(),
        "selected_department": department_id,
        "selected_course": course_id,
        "selected_status": status,
        "selected_result": result,
        "query": query,
    }
    return render(request, "students/student_list.html", context)


@login_required
def student_detail(request, pk):
    student = get_object_or_404(
        Student.objects.select_related('department', 'profile').prefetch_related('courses'),
        pk=pk,
    )
    return render(request, "students/student_detail.html", {"student": student})


@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form": form, "mode": "add"})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect("student_detail", pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(
        request, "students/student_form.html", {"form": form, "mode": "edit", "student": student}
    )


def _is_staff(user):
    return user.is_staff


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # Bonus rule: only staff users may actually delete.
    if request.method == "POST":
        if not request.user.is_staff:
            messages.error(request, "Only staff users can delete students.")
            return redirect("student_detail", pk=student.pk)
        name = student.name
        student.delete()
        messages.success(request, f"Deleted student '{name}'.")
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html", {"student": student})


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@login_required
def dashboard(request):
    students = Student.objects.all()
    stats = students.aggregate(average_marks=Avg('marks'), highest_marks=Max('marks'))

    top_student = students.order_by('-marks').first()
    recent_students = students.order_by('-joined_date', '-id')[:5]

    context = {
        "total_students": students.count(),
        "active_students": students.filter(is_active=True).count(),
        "total_departments": Department.objects.count(),
        "total_courses": Course.objects.count(),
        "average_marks": stats["average_marks"],
        "top_student": top_student,
        "recent_students": recent_students,
    }
    return render(request, "students/dashboard.html", context)
