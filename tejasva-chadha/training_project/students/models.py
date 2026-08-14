from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .validators import validate_not_future_date, validate_trainer_role


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
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
        related_name='assigned_courses',
        validators=[validate_trainer_role]
    )

    def clean(self):
        super().clean()
        if self.assigned_trainer:
            validate_trainer_role(self.assigned_trainer)

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
    age = models.IntegerField(validators=[MinValueValidator(16), MaxValueValidator(60)])
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
        through='Enrollment',
        related_name='students', 
        blank=True
    )

    def clean(self):
        super().clean()
        if self.age is not None and (self.age < 16 or self.age > 60):
            raise ValidationError({'age': 'Age must be between 16 and 60.'})
        if self.user and self.user.email and self.email and self.email.lower() != self.user.email.lower():
            raise ValidationError({'email': 'Student email must match associated User email.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    current_mark = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_student_course_enrollment')
        ]

    def clean(self):
        super().clean()
        if self.current_mark is not None and (self.current_mark < 0 or self.current_mark > 100):
            raise ValidationError({'current_mark': 'Marks must be between 0 and 100.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.course.code} ({self.current_mark})"


class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField(validators=[validate_not_future_date])

    def clean(self):
        super().clean()
        if self.date_of_birth:
            validate_not_future_date(self.date_of_birth)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_given')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField()
    is_visible = models.BooleanField(default=True, help_text="Visible to student")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.student and self.course:
            if not Enrollment.objects.filter(student=self.student, course=self.course).exists():
                raise ValidationError("Feedback can only be submitted for an active enrollment.")
        if self.enrollment:
            if self.enrollment.student != self.student or self.enrollment.course != self.course:
                raise ValidationError("Feedback enrollment does not match student and course.")

    def save(self, *args, **kwargs):
        if not self.enrollment and self.student and self.course:
            self.enrollment = Enrollment.objects.filter(student=self.student, course=self.course).first()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback for {self.student.name} by {self.trainer.username}"


class MarksHistory(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True, related_name='marks_history')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks_history')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='marks_history')
    previous_marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    new_marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marks_updates')
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.previous_marks < 0 or self.previous_marks > 100:
            raise ValidationError({'previous_marks': 'Marks must be between 0 and 100.'})
        if self.new_marks < 0 or self.new_marks > 100:
            raise ValidationError({'new_marks': 'Marks must be between 0 and 100.'})

    def save(self, *args, **kwargs):
        if not self.enrollment and self.student and self.course:
            self.enrollment = Enrollment.objects.filter(student=self.student, course=self.course).first()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Marks change for {self.student.name}: {self.previous_marks} -> {self.new_marks}"
