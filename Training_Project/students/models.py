from django.db import models

class Student(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    course = models.CharField(max_length=100)
    marks = models.IntegerField()
    joined_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
