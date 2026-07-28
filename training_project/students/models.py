from django.db import models
from django.utils import timezone
from datetime import timedelta
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

# course model
class Course(models.Model):
     course_name=models.CharField(max_length=50)
     code=models.CharField(max_length=10)
     duration=models.DurationField(default=timedelta(minutes=30))
     active_status=models.CharField(max_length=15)

     def __str__(self):
                return f"{self.course_name}"


class Department(models.Model):
      name=models.CharField(max_length=20)
      description=models.CharField(max_length=150)

      def __str__(self):
                      return f"{self.name}"



# student model
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,
                              related_name='student',
                              null=True,
                              blank=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    course=models.ManyToManyField(Course,
                                  related_name='students')
    marks=models.IntegerField()
    join_date=models.DateField()
    active_status=models.CharField( max_length=50)
    department=models.ForeignKey(Department,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,
                                 related_name='students')


    def __str__(self):
        courses=', '.join(course.course_name for course in self.course.all())
        return f"{self.name} -{courses}"

# create student profile(one to one relation)
class StudentProfile(models.Model):
    phone=models.IntegerField(null=True,
                                     blank=True,)
    address=models.CharField(max_length=150,null=True,
                                     blank=True,)
    DoB=models.DateField(null=True,blank=True,)
    student=models.OneToOneField(Student,
                                 on_delete=models.CASCADE,
                                 related_name='profile')


    @property
    def age(self):
           if not self.DoB:
                  return None
           today=date.today()
           age=today.year-self.DoB.year
           if (today.month,today.day)<(self.DoB.month,self.DoB.day):
                  age-=1
           return age

    def __str__(self):
            return f"{self.phone} - {self.address}-{self.DoB}"


# userprofile
class UserProfile(models.Model):
       user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
       role=models.CharField(max_length=20,choices=
                             [('ADMIN','Admin'),
                              ('TRAINER','Trainer'),
                              ('STUDENT','Student')])

       def __str__(self):
              return f"{self.user.username}-{self.role}"


class TrainerCourse(models.Model):
       trainer=models.ForeignKey(UserProfile,
                                 on_delete=models.CASCADE,
                                 limit_choices_to={"role":"TRAINER"},
                                 related_name='assigned_course')

       course=models.ForeignKey(Course,
                                on_delete=models.CASCADE,
                                related_name='assigned_trainer')

       def __str__(self):
              return f'{self.trainer.user.username}--{self.course.course_name}'
    