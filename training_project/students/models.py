from django.db import models
from django.utils import timezone
# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    age = models.IntegerField()
    course=models.CharField(max_length=100)
    marks=models.IntegerField()
    join_date=models.DateField()
    active_status=models.CharField( max_length=50)

    def __str__(self):
        return f"{self.name} - {self.age}-{self.course}"



