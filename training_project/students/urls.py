from django.urls import path,include
from students import views

urlpatterns = [
    path("home/",views.home,name='home'),
    path("about/",views.about,name='about'),
    path('',views.show_student,name="show_student"),
    path('add/',views.add,name='add'),
]