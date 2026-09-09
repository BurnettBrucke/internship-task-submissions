from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration = models.CharField(max_length=50)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='students',
    )

    courses = models.ManyToManyField(
        Course,
        related_name='students'
    )

    marks = models.IntegerField()
    joined_date = models.DateField()
    active_status = models.BooleanField(default=True)

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

