from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    marks = models.IntegerField()
    joined_date = models.DateField()
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.course})"
