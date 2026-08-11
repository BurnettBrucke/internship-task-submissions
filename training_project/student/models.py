from django.db import models
from django.contrib.auth.models import User


# Department Model
class Department(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        # Shows department name in admin and shell
        return self.name

    class Meta:
        ordering = ['name']


# Course Model
class Course(models.Model):
    name      = models.CharField(max_length=100)
    code      = models.CharField(max_length=20, unique=True)
    duration  = models.CharField(max_length=50)   # e.g. "3 months"
    is_active = models.BooleanField(default=True)
    trainer   = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_courses',
        limit_choices_to={'userprofile__role': 'trainer'},
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']


# Student Model
class Student(models.Model):
    # Basic info (Day 2 requirements)
    name        = models.CharField(max_length=100)
    email       = models.EmailField(unique=True)
    age         = models.IntegerField()
    course      = models.CharField(max_length=100)   # e.g. "Python Django"
    marks       = models.FloatField()
    joined_date = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)

    # Department relationship
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'   # dept.students.all() gives all students in dept
    )

    # Courses enrolled by student
    enrolled_courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name='enrolled_students'  # course.enrolled_students.all()
    )

    # Link to Django Auth User (set when student registers themselves)
    # Nullable so existing/admin-created students don't break.
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile'
    )

    # Assigned trainer
    trainer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_students',
        limit_choices_to={'userprofile__role': 'trainer'},
    )

    def __str__(self):
        # Shows clearly in admin: "Alice (alice@email.com)"
        return f"{self.name} ({self.email})"

    @property
    def is_pass(self):
        """Returns True if marks >= 40 (Pass), False if below (Fail)."""
        return self.marks >= 40

    class Meta:
        ordering = ['-joined_date']   # newest students first


# StudentProfile Model (Additional student details)
class StudentProfile(models.Model):
    student       = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='profile'   # student.profile gives the profile object
    )
    phone         = models.CharField(max_length=15, blank=True)
    address       = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.student.name}"


# UserProfile Model (extends default User with roles)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin',   'Administrator'),
        ('trainer', 'Trainer'),
        ('student', 'Student'),
    ]

    user        = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile'
    )
    role        = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    # Trainers require admin approval before they can log in to the trainer portal
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} [{self.role}]"

    # Helpers
    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_trainer(self):
        return self.role == 'trainer'

    @property
    def is_student(self):
        return self.role == 'student'


# AuditLog Model (records sensitive system actions)
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN',          'Login'),
        ('LOGOUT',         'Logout'),
        ('FAILED_LOGIN',   'Failed Login'),
        ('CREATE',         'Create'),
        ('UPDATE',         'Update'),
        ('DELETE',         'Delete'),
        ('MARKS_UPDATE',   'Marks Update'),
        ('FEEDBACK',       'Feedback'),
        ('ACCOUNT_STATUS', 'Account Status Change'),
    ]

    user        = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address  = models.GenericIPAddressField(null=True, blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f"[{self.action_type}] {username} @ {self.timestamp:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-timestamp']   # most recent first


# Feedback Model
class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]   # 1 to 5

    trainer    = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_feedback'
    )
    student    = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='feedback_received'
    )
    course     = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='feedback_list',
        null=True,
        blank=True,
    )
    rating     = models.IntegerField(choices=RATING_CHOICES, default=3)
    comment    = models.TextField()
    # is_visible controls whether the student can see this feedback
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Feedback by {self.trainer.username} for "
            f"{self.student.name} (rating: {self.rating})"
        )

    class Meta:
        ordering = ['-created_at']


# MarksHistory Model (records marks history trail)
class MarksHistory(models.Model):
    student    = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='marks_history'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marks_updates'
    )
    old_marks  = models.FloatField()
    new_marks  = models.FloatField()
    reason     = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        updater = self.updated_by.username if self.updated_by else 'Unknown'
        return (
            f"{self.student.name}: {self.old_marks} → {self.new_marks} "
            f"by {updater}"
        )

    class Meta:
        ordering = ['-updated_at']
