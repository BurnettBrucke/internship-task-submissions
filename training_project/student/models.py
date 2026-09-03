from django.db import models

# Create your models here.
class student(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    age=models.PositiveIntegerField()
    course=models.CharField(max_length=20)
    marks=models.PositiveIntegerField()
    joined_date=models.DateField(auto_now_add=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return "{self.name}-{self.course}"


