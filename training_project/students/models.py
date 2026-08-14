from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    course_name = models.CharField(
        max_length=100,
        unique=True
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    duration = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name


class UserProfile(models.Model):

    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        TRAINER = "TRAINER", "Trainer"
        STUDENT = "STUDENT", "Student"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.STUDENT
    )

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Student(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True
    )

    courses = models.ManyToManyField(
        Course,
        related_name="students"
    )

    marks = models.PositiveIntegerField()
    joined_date = models.DateField()
    is_active = models.BooleanField(default=True)

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


class TrainerAssignment(models.Model):

    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trainer_assignments",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="trainer_assignments",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="trainer_assignments",
    )

    assigned_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            "trainer",
            "student",
            "course",
        )

    def __str__(self):

        return (
            f"{self.trainer.username} → "
            f"{self.student.name} ({self.course.course_name})"
        )


class AuditLog(models.Model):

    class Action(models.TextChoices):

        LOGIN = "LOGIN", "Login"

        LOGOUT = "LOGOUT", "Logout"

        FAILED_LOGIN = "FAILED_LOGIN", "Failed Login"

        CREATE = "CREATE", "Create"

        UPDATE = "UPDATE", "Update"

        DELETE = "DELETE", "Delete"

        MARKS_UPDATE = "MARKS_UPDATE", "Marks Update"

        FEEDBACK = "FEEDBACK", "Feedback"

        STATUS_CHANGE = "STATUS_CHANGE", "Status Change"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices,
    )

    object_name = models.CharField(
        max_length=100
    )

    description = models.TextField()

    ip_address = models.GenericIPAddressField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-timestamp"
        ]

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.action}"
        )    


class Feedback(models.Model):

    trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feedback_given",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="feedback_received",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="feedback",
    )

    rating = models.PositiveSmallIntegerField()

    feedback = models.TextField()

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

        ordering = [
            "-created_at"
        ]

    def clean(self):

        from django.core.exceptions import ValidationError

        if self.rating is not None:

            if self.rating < 1 or self.rating > 5:

                raise ValidationError(
                    {
                        "rating":
                        "Rating must be between 1 and 5."
                    }
                )

    def __str__(self):

        return (
            f"{self.student.name} - "
            f"{self.course.course_name}"
        )


class MarksHistory(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="marks_history",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="marks_history",
    )

    previous_marks = models.PositiveIntegerField()

    new_marks = models.PositiveIntegerField()

    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="marks_updates",
    )

    reason = models.TextField()

    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-updated_at"
        ]

    def clean(self):

        from django.core.exceptions import ValidationError

        if not 0 <= self.new_marks <= 100:

            raise ValidationError(
                {
                    "new_marks":
                    "Marks must be between 0 and 100."
                }
            )

        if not 0 <= self.previous_marks <= 100:

            raise ValidationError(
                {
                    "previous_marks":
                    "Marks must be between 0 and 100."
                }
            )

    def __str__(self):

        return (
            f"{self.student.name} - "
            f"{self.course.course_name}"
        )