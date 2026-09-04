from django.contrib import messages
from django.shortcuts import redirect,render # type: ignore
from .form import StudentForm
from .models import student


# Create your views here.
def home(request):
    comp={ "company_name":"Burnett"}
    return render(request,"website/home.html",comp)

def about(request):
    return render(request,"website/about.html")

def student_list(request):
    students=student.objects.all()
    active_student=students.filter(active=True).count()
    total_student=students.count()

    context={
        "students":students,
        "active_student":active_student,
        "total_student":total_student
    }

    return render(request,("website/student_list.html"),context)

def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Student added successfully!"
            )

            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "website/add_student.html",
        {"form": form}
    )