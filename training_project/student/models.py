from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class department(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField()

    def __str__(self):
        return f"{self.name}"


# class UserProfile(models.Model):

#     ROLE_CHOICES= [("admin","Administrator"),
#             ("trainer","Trainer"),
#             ("student","Student"),]
#     user=models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='userprofile'

#     )

#     role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='student')
#     def __str__(self):
#         return f"{self.user.username} - {self.get_role_display()}"



class student(models.Model):
    # user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='student_profile',null=True,blank=True)

    name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    age=models.PositiveIntegerField()
    course=models.CharField(max_length=20)
    marks=models.PositiveIntegerField()
    joined_date=models.DateField(auto_now_add=True)
    active=models.BooleanField(default=True)

    department=models.ForeignKey(department,on_delete=models.CASCADE,related_name='students')

    

    def __str__(self):
        return self.name





class StudentProfile(models.Model):
    phone=models.IntegerField(10)
    address=models.TextField()
    date_of_birth=models.DateTimeField(null=True,blank=True)
    students=models.OneToOneField(student,on_delete=models.CASCADE,related_name='student_profile')

    def __str__(self):
        return f"{self.students.name}'s Profile "

class Course(models.Model):
    course_name=models.TextField()
    code=models.CharField()
    duration=models.IntegerField(help_text='Duration in Months')
    active_status=models.BooleanField(default=True)
    students=models.ManyToManyField(student,related_name='courses')
    # trainer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='training_courses')


    def __str__(self):
        return f"{self.course_name} ({self.code})"


