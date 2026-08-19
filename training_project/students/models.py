from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Department(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):

    course_name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    duration = models.CharField(
        max_length=50
    )

    active = models.BooleanField(
        default=True
    )

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
        on_delete=models.PROTECT,
        related_name="students"
    )

    assigned_trainer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_students"
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    age = models.IntegerField(
        validators=[
            MinValueValidator(16),
            MaxValueValidator(60)
        ]
    )

    joined_date = models.DateField(
        auto_now_add=True
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Enrollment(models.Model):

    STATUS_CHOICES = [
        ("enrolled", "Enrolled"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="enrollments"
    )

    enrollment_date = models.DateField(
        default=timezone.now
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="enrolled"
    )

    marks = models.FloatField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course_enrollment"
            )
        ]

    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.course.course_name}"
        )


def validate_date_of_birth(value):

    if value > timezone.localdate():

        raise ValidationError(
            "Date of birth cannot be in the future."
        )


class StudentProfile(models.Model):

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    date_of_birth = models.DateField(
        validators=[
            validate_date_of_birth
        ]
    )

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

    is_approved = models.BooleanField(
        default=False
    )

    account_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.role}"
        )


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

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.PROTECT,
        related_name="feedbacks",
        null=True,
        blank=True
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

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
        return (
            f"{self.student.name} - "
            f"{self.rating}"
        )


class MarksHistory(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="marks_history"
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.PROTECT,
        related_name="marks_history",
        null=True,
        blank=True
    )

    previous_marks = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    new_marks = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.new_marks}"
        )