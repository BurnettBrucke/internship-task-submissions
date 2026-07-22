from django.shortcuts import render
from django.http import HttpResponse
from .models import Student
from .form import StudentForm 
from django.shortcuts import redirect  
# Create your views here.
def home(request):
    return render (request,"home.html")

def about(request):
    return HttpResponse("this is about page")

def show_student(request):
    all_students=Student.objects.all()
    pass_student=Student.objects.filter(active_status='pass')
    std_getmore=Student.objects.filter(marks__gt=40)
    std_getless=Student.objects.filter(marks__lt=40)
    for student in all_students:
        if student.marks>=40:
            student.result='pass'
        else:
            student.result='fail'

    context={"students":all_students,
            "active_students":pass_student,
            "total_std":Student.objects.count(),
            "active_std":Student.objects.filter(active_status='pass').count(),
            "pass_std":std_getmore,
            "fail_std":std_getless
            }

    return render (request,'show_std.html',context)

# adding student or form 
# def add(request):
#     if request.method == "POST":
#         name=request.POST.get("name")
#         age=request.POST.get("age")
#         email=request.POST.get("email")
#         course=request.POST.get("course")
#         marks=request.POST.get("marks")
#         join_date=request.POST.get("join_date")
    

#         Student.objects.create(
#             name=name,
#             age=age,
#             email=email,
#             course=course,
#             marks=marks,
#             join_date=join_date,
#             active_status="pass" if int(marks)>=40 else "fail"
#         )
#     return render(request,'add.html')

def add(request):
    if request.method=="POST":
        form=StudentForm(request.POST)
        if form.is_valid():
            student=form.save(commit=False)
            if student.marks>=40:
                student.active_status='pass'
            else:
                student.active_status="fail"
            form.save()
            return redirect("show_student")
    else:
        form=StudentForm()
    
    return render(request,"add.html",{"forms":form})
