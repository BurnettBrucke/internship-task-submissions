from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    context = {
        'company_name': 'Bug Network Private Limited'
    }
    return render(request, 'students/home.html', context)

def about(request):
    html_content = "<h1>About Page</h1><p>Welcome to the About page of our Django application!</p>"
    return HttpResponse(html_content)
