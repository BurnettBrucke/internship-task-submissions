## Writting and testting ORM queries

## Get all students
student.objects.all()

output:- <QuerySet [<student: Aditya>, <student: Ankur>, <student: Aman>, <student: Ajay>, <student: mayank>, <student: Rahul>, <student: Khushi>, <student: Pavan>, <student: Ayush>, <student: Rajneesh>, <student: Aditya>, <student: Aditya>]>

This is  a query that returns all the objects/elements from the model
---------------------------------------------------------------------------

## Get only active students.
-> student.objects.filter(active=True)

output-> <QuerySet [<student: Aditya>, <student: Ankur>, <student: Aman>, <student: Ajay>, <student: mayank>, <student: Rahul>, <student: Khushi>, <student: Pavan>, <student: Ayush>, <student: Rajneesh>, <student: Aditya>, <student: Aditya>]>

This returns the QuerySet where the the student is active.
-----------------------------------------------------------------------

## Get students whose marks are greater than or equal to 60.
student.objects.filter(marks__gte=60)

output-> <QuerySet [<student: Ankur>, <student: Aman>, <student: mayank>, <student: Pavan>, <student: Aditya>, <student: Aditya>]>

This returns the data the name of the students whose marks are greater than or equal to 60
-----------------------------------------------------------------------------------------
## Get students whose names contain a given word.
->student.objects.filter(name__icontains='i')

output-> <QuerySet [<student: Aditya>, <student: Khushi>, <student: Aditya>, <student: Aditya>]>

This returns the Name of students where we have a letter "i"
--------------------------------------------------------------------
## Order student by marks
ascending=student.objects.order_by('marks')
descending=student.objects.order_by('-marks')

output-> <QuerySet [<student: Rahul>, <student: Khushi>, <student: Aditya>, <student: Ayush>, <student: Ajay>, <student: Rajneesh>, <student: Ankur>, <student: Aman>, <student: Aditya>, <student: Aditya>, <student: mayank>, <student: Pavan>]>
This returns the students on the basis of their marks by ascending or descending.
----------------------------------------------------------------------------------
## Get the top three students by marks.

top_three=student.objects.order_by('-marks')[:3]

output-> <QuerySet [<student: Pavan>, <student: mayank>, <student: Aditya>]>

This returns the top three highest marks records by slicing only three elements.
------------------------------------------------------------------------------\

## Get students from a specific department
student.objects.filter(department=2)

<QuerySet [<student: Ankur>, <student: Aditya>, <student: Aditya>]>
This returns the students from a specific department based on department id
--------------------------------------------------------------------------------

## 8. Get students enrolled in a specific course.

student.objects.filter(course='Python')

output-> <QuerySet [<student: Khushi>, <student: Pavan>, <student: Ayush>]>
This filters the student based on course.
----------------------------------------------------------------------------

## 9.Get all courses for one student

stu=student.objects.get(id=2)
stu.courses.all()

output->  <QuerySet [<Course: AI (101)>, <Course: BDE (103)>]>
This filter the student based on id in the first step , then we get all the courses from the student where he/she is enrolled
--------------------------------------------------------------------------------------

## 10. Count the total number of students.
student.objects.filter(active=True).count()

output-> 12
This counts the total number of students and we are considering only active students here.
--------------------------------------------------------------------------------------------

## 11. Calculate average marks
 from django.db.models import Avg

 student.objects.aggregate(Avg('marks'))
Out: {'marks__avg': 65.66666666666667}
------------------------------------------------------
## 12. Find the highest and lowest marks

 from django.db.models import Max,Min

 student.objects.aggregate(Max('marks'),Min('marks'))
Output: {'marks__max': 98, 'marks__min': 35}
This finds the maximu and minimum using the aggregate functions
----------------------------------------------------------------------
## 13. Count students in each department.
from django.db.models import Count

student.objects.values('department').annotate(total_student=Count('id'))

 output-> <QuerySet [{'department': 1, 'total_student': 1}, {'department': 2, 'total_student': 3}, {'department': 3, 'total_student': 4}, {'department': 4, 'total_student': 2}, {'department': 5, 'total_student': 2}]>
----------------------------------------------------------------------------------
## 14. Find departments with more than three students
student.objects.values('department').annotate(total_students=Count('id')).filter(total_students__gt=3)

Out: <QuerySet [{'department': 3, 'total_students': 4}]>

Filter the student based on department and count the departments where it is greater than 3
---------------------------------------------------------------------------------------------

## 15. Find students who do not have a profile.
 student.objects.filter(student_profile__isnull=True)
Output: <QuerySet [<student: Aman>, <student: Ajay>, <student: mayank>, <student: Rahul>, <student: Khushi>, <student: Aditya>, <student: Aditya>]>

This returns the student who are not having a profile by filtering the student and checkin whether the profile carry their data or not.
----------------------------------------------------------------------------------
## 16. Find students enrolled in more than one course.
student.objects.annotate(course_count=Count('courses')).filter(course_count__gte=1)
Output: <QuerySet [<student: Ankur>, <student: Aditya>, <student: Aditya>, <student: Aman>, <student: Ajay>, <student: Rajneesh>]>

This returns student student by counting the courses and returns them if the count is greater than 1.
-----------------------------------------------------------------------------------------------
## 17. Search students by name or email using Q objects.
 from django.db.models import Q

 search_query='Aditya'

 student.objects.filter(Q(name__icontains=search_query))
Output: <QuerySet [<student: Aditya>, <student: Aditya>, <student: Aditya>]>
This returns the name that matches the search query using icontains that checks the name irrespective of case sensitivity and Q for query comparison.

--------------------------------------------------------------------------------------
## 18. Update inactive students to active using update().
student.objects.filter(active=False).update(active=True)

Output: 0

This is simply updating the active status from false to True.

--------------------------------------------------------------------------------------
## 19. Delete records with invalid marks, if any.
 student.objects.filter(Q(marks__lt=0) | Q(marks__gte=0)).delete()
Output:  (24,
 {'student.StudentProfile': 5,
  'student.Course_students': 7,
  'student.student': 12})

 
--------------------------------------------------------------------------

## 20. Use select_related() and prefetch_related() appropriately.
### select_related()
students = student.objects.select_related("department").all()
   ...: 
   ...: for s in students:
   ...:     print(s.name, s.department)
   ...: 
output:- {Aditya AI
          Ankur Python
          Ajay Python}

### prefetch_Related()

 courses = Course.objects.prefetch_related("students")
   ...: 
   ...: for course in courses:
   ...:     print(f"Course: {course.course_name}")
   ...: 
   ...:     for s in course.students.all():
   ...:         print(f"  Student: {s.name}")
   ...: 
   ...:     print("-" * 30)
   ...: 
output:-    {Course: AI
        Student: Aditya
        ------------------------------
        Course: BDE
        ------------------------------
        Course: Python
        Student: Ankur
        Student: Ajay
        ------------------------------
        Course: Cloud
        ------------------------------
        Course: Data
        ------------------------------}