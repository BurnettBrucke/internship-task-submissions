from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    company = "Bug Network Private Limited"
    return render(request,"home.html",{"company": company}) #context

def about(request):
    return HttpResponse("<h1>About Page<h1><p>This is About Page.</p>")