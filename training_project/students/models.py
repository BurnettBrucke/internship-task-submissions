from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    duration = models.FloatField()
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name
    

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    marks = models.FloatField()
    course = models.CharField(max_length=100)
    joined_date = models.DateTimeField(auto_now_add=True)
    active_status = models.BooleanField(default=False)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,related_name="students")
    course = models.ManyToManyField(Course, related_name="students")

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="student_profile")
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.student.name

