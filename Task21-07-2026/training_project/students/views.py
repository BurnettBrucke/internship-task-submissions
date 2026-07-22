from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    company="Bug Network Private Limited"
    return render(request,"home.html", {"company":company})

def about(request):
    return HttpResponse("<h1>About</h1><h3>Students Application</h3>")