1. Get all students.
>>> Student.objects.all()
<QuerySet [<Student: vikas - 23-python, sql>, 
            <Student: govind - 24-python, sql, django>, <Student: rohit - 23-python>,
            <Student: nihal - 30-ML>, 
            <Student: kamal - 29-sql>, 
            <Student: ravi - 31-python, sql, django, ML>, <Student: rahul - 31-python, sql, django>, <Student: arun - 32-django, ML>, 
            <Student: vikas gurjar - 24-python, sql, django, ML>, 
            <Student: dev - 19-python, sql>]>

use for loop in self.cource.all() 
courses=(course.course_name for course in self.course.all())
pass courses in __str___()

2. Get only active students
>>>Student.objects.filter(active_status='pass')
[<Student: vikas - 23-python, sql>, <Student: govind - 24-python, sql, django>, <Student: rohit - 23-python>, <Student: nihal - 30-ML>, <Student: kamal - 29-sql>, <Student: ravi - 31-python, sql, django, ML>, <Student: rahul - 31-python, sql, django>, <Student: arun - 32-django, ML>, <Student: vikas gurjar - 24-python, sql, django, ML>]>

3.Get students whose marks are greater than or equal to 60.
>>> Student.objects.filter(marks__gte=80)
<QuerySet [<Student: kamal - 29-sql>, <Student: vikas gurjar - 24-python, sql, django, ML>]>

4. Get students whose names contain a given word.
>>> Student.objects.filter(name__contains='a')
<QuerySet [<Student: vikas - 23-python, sql>, <Student: nihal - 30-ML>, <Student: kamal - 29-sql>, <Student: ravi - 31-python, sql, django, ML>, <Student: rahul - 31-python, sql, django>, <Student: arun - 32-django, ML>, <Student: vikas gurjar - 24-python, sql, django, ML>]>
>>> 

5. Order students by marks
>>> Student.objects.all().order_by('marks')
<QuerySet [<Student: dev - 19-python, sql>, <Student: rohit - 23-python>, <Student: vikas - 23-python, sql>, <Student: arun - 32-django, ML>, <Student: govind - 24-python, sql, django>, <Student: nihal - 30-ML>, <Student: ravi - 31-python, sql, django, ML>, <Student: rahul - 31-python, sql, django>, <Student: kamal - 29-sql>, <Student: vikas gurjar - 24-python, sql, django, ML>]>
for descending use order_by(-marks)

6. Get the top three students by marks
>>> Student.objects.all().order_by('-marks')[:3]        
<QuerySet [<Student: vikas gurjar - 24-python, sql, django, ML>, <Student: kamal - 29-sql>, <Student: nihal - 30-ML>]>

7. Get students from a specific department.
>>> students = Student.objects.filter(department__name='ds')
>>> print(students)
<QuerySet [<Student: vikas - 23-python, sql>, <Student: kamal - 29-sql>, <Student: dev - 19-python, sql>]>
>>> 
or for dept in Department.objects.all():
        print(dept.students.filter(name__icontains='ds'))

8. Get students enrolled in a specific course.
<QuerySet [<Student: vikas - 23-python, sql>, <Student: kamal - 29-sql>, <Student: dev - 19-python, sql>]>
>>> Student.objects.filter(course__course_name='python')
<QuerySet [<Student: vikas - 23-python, sql>, <Student: govind - 24-python, sql, django>, <Student: rohit - 23-python>, <Student: ravi - 31-python, sql, django, ML>, <Student: rahul - 31-python, sql, django>, <Student: vikas gurjar - 24-python, sql, django, ML>, <Student: dev - 19-python, sql>]>
course = many to many field in student model
__course_name = course model field fro filter 
'python'=course of which student you want 


9. Get all courses for one student.
>>> Course.objects.filter(students__name='vikas')
<QuerySet [<Course: python>, <Course: sql>]>
>>> 
run quesry on course model and filter student by name 
here students is related_name

10. Count the total number of students.
>>> Student.objects.count()
    10

11. Calculate average marks
>>> Student.objects.aggregate(Avg('marks'))
{'marks__avg': 71.1}
>>> 

12. Find the highest and lowest marks
>>> highest=Student.objects.aggregate(Max('marks'))
>>> lowest=Student.objects.aggregate(Min('marks')) 
>>> print(highest,lowest)
{'marks__max': 90} {'marks__min': 35}
>>> 

13. Count students in each department
>>> dept=Department.objects.annotate(total=Count('students'))
>>> for i in dept:
...     print(i.name,i.total)
...
cse 3
aiml 4
ds 3
>>> 
.annotate() = add extra calculated value with every object ,db mai nhi hoti bas query result mai save hoti hai 

14. Find departments with more than three students
>>> dept=Department.objects.annotate(total=Count('students'))
>>> for i in dept:
...     if i.total>3:
...             print(i.name,i.total)
...
aiml 4
>>>
15. Find students who do not have a profile
>>> std=Student.objects.filter(profile__isnull=True)
>>> for i in std:
...     print(i.name)
... 
govind
rohit
kamal
rahul
dev
>>> 
__isnull=True is return list of object that has no profile 

16. Find students enrolled in more than one course.
>>> std=Student.objects.annotate(total=Count('course'))
>>> for i in std:
...     if i.total>1:
...             print(i.name,i.total)
... 
govind 3
rahul 3
ravi 4
arun 2
vikas gurjar 4
vikas 2
dev 2
>>> 
use .annotate() function to count course of individual course

17. Search students by name or email using Q objects.
>>> Student.objects.filter(Q(name='vikas')|Q(email='vk@gmail.com'))
<QuerySet [<Student: vikas - 23-python, sql>, <Student: vikas gurjar - 24-python, sql, django, ML>]>
>>>
uses Q object that is ussed to write complex query with AND , OR , NOT operator

18. Update inactive students to active using update().
>>> Student.objects.filter(active_status='fail').update(active_status='pass')
1
>>> 
it means one student is update if we get all fail student we get empty query set 

19. Delete records with invalid marks, if any.
>>> Student.objects.filter(Q(marks__lt=0)|Q(marks__gt=100)).delete()
(0, {})
>>>  
becouse all marks are valid

20. Use select_related() and prefetch_related() appropriately.
>>> students=Student.objects.select_related('department')
>>> for i in students:
...     print(i.name,i.department.name)
... 
vikas ds
govind cse
rohit cse
nihal aiml
kamal ds
ravi aiml
rahul cse
arun aiml
vikas gurjar aiml
dev ds
>>> 
use of select_related
output to same hai but queries mai performace bad gya .all() se bhi rha tha ye to 

>>> depts=Department.objects.prefetch_related("students")
>>> for i in depts:
...     print(i.name)
...     for j in i.students.all():
...             print(j.name)
... 
cse:
govind
rohit
rahul

aiml:
nihal
ravi
arun
vikas gurjar

ds:
vikas
kamal
dev
>>>
 prefetch_related() mai dept waise student agye yehi hi reverse foreign key hai 
 