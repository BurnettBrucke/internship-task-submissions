from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    duration = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name


class Student(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="student",
    null=True,
    blank=True
)
    
    department = models.ForeignKey(
    Department,
    on_delete=models.CASCADE,
    related_name="students"
)
    courses = models.ManyToManyField(
    Course,
    related_name="students"
)
    assigned_trainer = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="assigned_students"
)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    marks = models.FloatField()
    joined_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.student.name




class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("trainer", "Trainer"),
        ("student", "Student"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )
    is_approved = models.BooleanField(default=False)
    
    account_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("FAILED_LOGIN", "Failed Login"),
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("MARKS_UPDATE", "Marks Update"),
        ("FEEDBACK", "Feedback"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    description = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.action}"

class Feedback(models.Model):

    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_feedback"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )

    rating = models.IntegerField()

    comments = models.TextField()

    visible_to_student = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.rating}"

class MarksHistory(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="marks_history"
    )

    previous_marks = models.FloatField()

    new_marks = models.FloatField()

    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.name} - {self.new_marks}"