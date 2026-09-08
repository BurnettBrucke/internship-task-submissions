from django.db import models


class Department(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Student(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    marks = models.IntegerField()
    joined_date = models.DateField()
    active = models.BooleanField(default=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    def __str__(self):
        return self.name


class StudentProfile(models.Model):

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.student.name}'s Profile"


class Course(models.Model):

    course_name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    duration = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    students = models.ManyToManyField(
        Student,
        related_name='courses'
    )

    def __str__(self):
        return f"{self.course_name} ({self.code})"