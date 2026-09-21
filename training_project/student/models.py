from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class department(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField()

    def __str__(self):
        return f"{self.name}"


class UserProfile(models.Model):

    ROLE_CHOICES= [("admin","Administrator"),
            ("trainer","Trainer"),
            ("student","Student"),]
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile'

    )
    is_approved = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"



class LoginAttempt(models.Model):

    username = models.CharField(max_length=150)

    failed_attempts = models.PositiveIntegerField(default=0)

    blocked_until = models.DateTimeField(
        null=True,
        blank=True
    )

    last_failed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


class AuditLog(models.Model):
    ACTION_TYPES = [
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=255,
        default=""
    )

    action_type = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
        default="UPDATE"
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    # Information about the object affected by the action
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True
    )

    affected_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.action_type} - {self.description or self.action}"

class student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='student_profile',null=True,blank=True)

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
    phone=models.IntegerField(max_length=10,blank=True)
    address=models.TextField()
    date_of_birth=models.DateTimeField(null=True,blank=True)
    students=models.OneToOneField(student,on_delete=models.CASCADE,related_name='student_profile')

    def __str__(self):
        return f"{self.students.name}'s Profile "

class Course(models.Model):
    course_name=models.TextField()
    code=models.CharField(max_length=20)
    duration=models.IntegerField(help_text='Duration in Months')
    active_status=models.BooleanField(default=True)
    students=models.ManyToManyField(student,related_name='courses')
    trainer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='training_courses')


    def __str__(self):
        return f"{self.course_name} ({self.code})"

class CourseMark(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_marks"
    )

    student = models.ForeignKey(
        student,
        on_delete=models.CASCADE,
        related_name="course_marks"
    )

    marks = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_course_marks"
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "student"],
                name="unique_course_student_mark"
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name} - {self.marks}"


class MarksHistory(models.Model):

    course_mark = models.ForeignKey(
        CourseMark,
        on_delete=models.CASCADE,
        related_name="history"
    )

    previous_marks = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    new_marks = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marks_history_updates"
    )

    reason = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.course_mark.student.name} - "
            f"{self.previous_marks} -> {self.new_marks}"
        )


class Feedback(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="feedback"
    )

    student = models.ForeignKey(
        student,
        on_delete=models.CASCADE,
        related_name="feedback_received"
    )

    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feedback_given"
    )

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField()

    is_visible = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.course.course_name} - "
            f"{self.rating}/5"
        )








    