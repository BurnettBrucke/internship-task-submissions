from django.db import models
from django.contrib.auth.models import User

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

class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('student', 'Student'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    student = models.OneToOneField(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profile'
    )

    is_approved = models.BooleanField(default=True)

    failed_login_attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class TrainerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='trainer_profile'
    )

    courses = models.ManyToManyField(
        Course,
        related_name='trainers',
        blank=True
    )

    def __str__(self):
        return self.user.username


class Feedback(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )

    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_feedbacks'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        null=True,
        blank=True
    )

    feedback = models.TextField()

    rating = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.student.name}"
    

class MarksUpdateHistory(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='marks_history'
    )

    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marks_updates'
    )

    previous_marks = models.PositiveIntegerField()

    new_marks = models.PositiveIntegerField()

    reason = models.TextField()

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.previous_marks} to {self.new_marks}"
        )
        
class AuditLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=50)

    affected_object = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.description}"
    
