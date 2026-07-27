from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    (many-to-many)."""

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    duration_weeks = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    """Represents a single student record."""

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
