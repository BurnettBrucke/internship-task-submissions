from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration = models.IntegerField(help_text="Duration in weeks")
    active_status = models.BooleanField(default=True)
    assigned_trainer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_courses'
    )

    def __str__(self):
        return f"{self.course_name} ({self.code})"


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    course = models.CharField(max_length=100, null=True, blank=True)
    marks = models.IntegerField()
    joined_date = models.DateField()
    active_status = models.BooleanField(default=True)
    
    # Relationships
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='students'
    )
    courses = models.ManyToManyField(
        Course, 
        related_name='students', 
        blank=True
    )

    def __str__(self):
        if self.course:
            return f"{self.name} ({self.course})"
        return self.name


class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return f"Profile for {self.student.name}"


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('trainer', 'Trainer'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.get_or_create(user=instance)


class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('failed_login', 'Failed Login'),
        ('logout', 'Logout'),
        ('marks_update', 'Marks Update'),
        ('feedback_creation', 'Feedback Creation'),
        ('status_change', 'Status Change'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    affected_object = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"


class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_given')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField()
    is_visible = models.BooleanField(default=True, help_text="Visible to student")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback for {self.student.name} by {self.trainer.username}"


class MarksHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks_history')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='marks_history')
    previous_marks = models.IntegerField()
    new_marks = models.IntegerField()
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marks_updates')
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Marks change for {self.student.name}: {self.previous_marks} -> {self.new_marks}"


