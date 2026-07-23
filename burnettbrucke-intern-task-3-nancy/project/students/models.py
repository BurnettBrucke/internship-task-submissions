from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Student(models.Model):
    """Represents a single student record."""

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(60)]
    )
    course = models.CharField(max_length=150)
    marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.course})"

    @property
    def result_status(self):
        """Return 'Pass' when marks are 40 or above, otherwise 'Fail'."""
        return "Pass" if self.marks >= 40 else "Fail"
