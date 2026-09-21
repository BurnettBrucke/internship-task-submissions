from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Student(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    marks = models.IntegerField()
    feedback = models.TextField(blank=True, default='')
    joined_date = models.DateField()
    active = models.BooleanField(default=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_record'
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

    trainer = models.ManyToManyField(
        User,
        related_name='assigned_courses',
        blank=True
    )

    def __str__(self):
        return f"{self.course_name} ({self.code})"

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

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class AuditLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=100)
    description = models.TextField()

    affected_object = models.CharField(
        max_length=255,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.action} - "
            f"{self.timestamp}"
        )

class CourseMark(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='course_marks'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_marks'
    )

    marks = models.IntegerField()

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_marks_updated'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course_mark'
            )
        ]

    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.course.course_name} - "
            f"{self.marks}"
        )

class MarksHistory(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='marks_history'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='marks_history'
    )

    previous_marks = models.IntegerField()

    new_marks = models.IntegerField()

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marks_history_updates'
    )

    reason = models.TextField()

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.previous_marks} → "
            f"{self.new_marks}"
        )

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
        related_name='feedbacks'
    )

    rating = models.PositiveIntegerField()

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

    def __str__(self):
        return (
            f"{self.student.name} - "
            f"{self.course.course_name} - "
            f"{self.rating}/5"
        )