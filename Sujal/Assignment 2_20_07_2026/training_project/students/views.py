from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    data = {
        'company': 'Bug Network Private Limited Training Program'
    }
    return render(request, 'home.html', data)


def about(request):
    return HttpResponse("<h1>About Page</h1>")