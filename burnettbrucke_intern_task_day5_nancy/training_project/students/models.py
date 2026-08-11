from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Attaches a role to every Django user: Administrator, Trainer, or Student.

    This is the backbone of role-based access control for the whole app.
    Every User should end up with exactly one UserProfile (see the post_save
    signal at the bottom of this file, which creates one automatically).
    """

    ROLE_ADMIN = 'admin'
    ROLE_TRAINER = 'trainer'
    ROLE_STUDENT = 'student'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Administrator'),
        (ROLE_TRAINER, 'Trainer'),
        (ROLE_STUDENT, 'Student'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    # Trainer accounts must be approved by an Administrator before they can
    # use the trainer dashboard or touch marks/feedback. Students and
    # Administrators are approved automatically (see the signal below).
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_trainer(self):
        return self.role == self.ROLE_TRAINER

    @property
    def is_student(self):
        return self.role == self.ROLE_STUDENT

    @property
    def is_pending_approval(self):
        """True for a trainer account that has registered but has not yet
        been approved by an Administrator."""
        return self.role == self.ROLE_TRAINER and not self.is_approved

    @property
    def completion_percentage(self):
        """Rough profile-completion score used for the progress bar on
        dashboards. Counts how many of the "nice to have" fields are filled
        in, plus whether a Student record is linked."""
        fields_filled = 0
        total_fields = 3

        if self.phone:
            fields_filled += 1
        if self.bio:
            fields_filled += 1
        if getattr(self.user, 'student_record', None):
            fields_filled += 1

        return int((fields_filled / total_fields) * 100)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Every new User automatically gets a UserProfile (default role:
    student, auto-approved). If the profile is later switched to Trainer
    (either via the trainer sign-up form or the Django admin) approval
    should be granted explicitly by an Administrator -- see
    RegisterForm/TrainerRegisterForm for where is_approved=False is set."""
    if created:
        UserProfile.objects.get_or_create(user=instance)


class Department(models.Model):
    """A department can contain many students (one-to-many)."""

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    """A course can have many students, and a student can take many courses
    (many-to-many). A course also has an assigned trainer."""

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    duration_weeks = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    # A trainer "owns" a course: only that trainer can update marks /
    # feedback for students taking it (checked in views, not just hidden
    # in templates).
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trainer_courses',
        limit_choices_to={'profile__role': UserProfile.ROLE_TRAINER},
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    """Represents a single student record."""

    # Links the student record to a real login account so a student can
    # see "their own" data. Optional/nullable because records can exist
    # (e.g. imported by an admin) before the person ever registers.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_record',
    )

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(60)]
    )
    marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # One department has many students. SET_NULL (rather than CASCADE) is
    # used so that deleting a department never deletes student records --
    # the students are simply left "unassigned" and can be reassigned later.
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
    )

    # A student can take many courses, and a course can have many students.
    courses = models.ManyToManyField(
        Course,
        related_name='students',
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} <{self.email}>"

    @property
    def result_status(self):
        """Return 'Pass' when marks are 40 or above, otherwise 'Fail'."""
        return "Pass" if self.marks >= 40 else "Fail"


class StudentProfile(models.Model):
    """Extra one-to-one profile information for a student."""

    # One-to-one: CASCADE is appropriate here because a profile has no
    # meaning without its student -- if the student is deleted, the profile
    # should be deleted too.
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.student.name}"


class Feedback(models.Model):
    """Feedback a trainer leaves for a student on a specific course."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='given_feedbacks',
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate the student's performance from 1 (poor) to 5 (excellent).",
    )
    comment = models.TextField()
    # Trainers can draft feedback and only publish it when ready.
    is_visible_to_student = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for {self.student.name} on {self.course.code}"


class AuditLog(models.Model):
    """Production-style audit trail. Records *who* did *what* to *which
    object*, from *where* (IP address), and *when* -- covering logins,
    logouts, failed logins, CRUD actions, marks updates, feedback, and
    account-status changes. Only Administrators may view this (enforced in
    the view, see students.views.audit_log)."""

    ACTION_LOGIN = 'LOGIN'
    ACTION_LOGOUT = 'LOGOUT'
    ACTION_LOGIN_FAILED = 'LOGIN_FAILED'
    ACTION_CREATE = 'CREATE'
    ACTION_UPDATE = 'UPDATE'
    ACTION_DELETE = 'DELETE'
    ACTION_MARKS_UPDATE = 'MARKS_UPDATE'
    ACTION_FEEDBACK = 'FEEDBACK'
    ACCOUNT_STATUS = 'ACCOUNT_STATUS'
    ACTION_CHOICES = [
        (ACTION_LOGIN, 'Login'),
        (ACTION_LOGOUT, 'Logout'),
        (ACTION_LOGIN_FAILED, 'Failed login'),
        (ACTION_CREATE, 'Create'),
        (ACTION_UPDATE, 'Update'),
        (ACTION_DELETE, 'Delete'),
        (ACTION_MARKS_UPDATE, 'Marks update'),
        (ACTION_FEEDBACK, 'Feedback'),
        (ACCOUNT_STATUS, 'Account status change'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='audit_logs'
    )
    # Kept even if the user record is later deleted, so the log entry still
    # says who performed the action.
    username = models.CharField(max_length=150, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES, default=ACTION_UPDATE)
    description = models.CharField(max_length=255)
    object_repr = models.CharField(max_length=255, blank=True, help_text="The affected object, e.g. 'Student: Asha Verma'")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['action_type']),
        ]

    def __str__(self):
        return f"[{self.action_type}] {self.timestamp:%Y-%m-%d %H:%M} - {self.description}"

    # Kept for backwards compatibility with the old field name.
    @property
    def action(self):
        return self.description


def log_action(user, description, action_type=AuditLog.ACTION_UPDATE, object_repr='', request=None):
    """Helper so views/signals can record an audit entry in one line.

    `request` is optional; when passed, the caller's IP address is captured
    automatically.
    """
    ip_address = get_client_ip(request) if request is not None else None
    is_authenticated = getattr(user, 'is_authenticated', False)
    AuditLog.objects.create(
        user=user if is_authenticated else None,
        username=getattr(user, 'username', '') if is_authenticated else (user or ''),
        action_type=action_type,
        description=description,
        object_repr=object_repr,
        ip_address=ip_address,
    )


def get_client_ip(request):
    """Best-effort client IP lookup. X-Forwarded-For is only trustworthy
    behind a properly configured reverse proxy; for a plain dev server
    REMOTE_ADDR is what actually matters."""
    if request is None:
        return None
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class MarksHistory(models.Model):
    """One row per marks change -- keeps the full history rather than just
    the current value, so "who changed what, when, and why" is always
    answerable."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks_history')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='marks_history')
    old_marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    new_marks = models.DecimalField(max_digits=5, decimal_places=2)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='marks_updates'
    )
    reason = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'Marks history'

    def __str__(self):
        return f"{self.student.name}: {self.old_marks} -> {self.new_marks}"
