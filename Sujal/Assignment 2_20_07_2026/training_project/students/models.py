from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    age=models.IntegerField()
    course=models.CharField(max_length=100)
    marks=models.FloatField()
    joined_date=models.DateField()
    active=models.BooleanField(default=True )
