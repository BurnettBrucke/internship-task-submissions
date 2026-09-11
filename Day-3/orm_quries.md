# Django ORM Queries
Introduction

All the ORM commands documented in this file were written and executed in the Django Shell using:

python manage.py shell

The queries were executed against the project's database using the Django ORM. The actual output returned by the Django Shell has also been copied and pasted below each query for verification.

This document contains the ORM queries performed for the assigned tasks, along with their corresponding shell output and a brief explanation of what each query does.

Note: The queries and outputs shown in this file are the actual commands executed in the Django Shell and are not manually generated examples.
### 1. Get all students

Requirement

Get all students from the database.

#### ORM Query

## >>> Student.objects.all()

Output

## <QuerySet [<Student: Mayank Joshi>, <Student: Aditya Singh Lodhi>, <Student: Madhur Virli>, <Student: Mahima Rana>, <Student: Naman Barde>, <Student: Sachin Prajapat>, <Student: Sneha Joshi>, <Student: Kaushal kashdoriya>, <Student: Raj Rathod>, <Student: Shubham Sharma>, <Student: Shubham vyas>]>

Short Explanation

This gets all the student records from the database.

### 2. Get only active students

Requirement

Get only the students who are currently active.

#### ORM Query

## >>> Student.objects.filter(active=True)

Output

## <QuerySet [<Student: Mayank Joshi>, <Student: Aditya Singh Lodhi>, <Student: Madhur Virli>, <Student: Mahima Rana>, <Student: Naman Barde>, <Student: Sneha Joshi>, <Student: Kaushal kashdoriya>, <Student: Raj Rathod>, <Student: Shubham Sharma>, <Student: Shubham vyas>]>

Short Explanation

This filters the students and returns only the ones whose active status
is True.

### 3. Get students whose marks are greater than or equal to 60

Requirement

Get students who have marks of 60 or more.

#### ORM Query

## >>> Student.objects.filter(marks__gte=60)

Output

## <QuerySet [<Student: Mayank Joshi>, <Student: Aditya Singh Lodhi>, <Student: Madhur Virli>, <Student: Mahima Rana>, <Student: Sachin Prajapat>, <Student: Sneha Joshi>, <Student: Raj Rathod>, <Student: Shubham vyas>]>

Short Explanation

This finds students whose marks are greater than or equal to 60 using the __gte (>=).

### 4. Get students whose names contain a given word

Requirement

Find students whose names contain a specific word or part of a name.

#### ORM Query

## >>> Student.objects.filter(name__icontains="ya")

Output

## <QuerySet [<Student: Mayank Joshi>, <Student: Aditya Singh Lodhi>, <Student: Kaushal kashdoriya>, <Student: Shubham vyas>]>

Short Explanation

This searches the student names for the given word without worrying
about uppercase or lowercase letters.

### 5. Order students by marks

Requirement

Display students sorted according to their marks.

#### ORM Query

## >>> Student.objects.all().order_by('marks') 

Output

## <QuerySet [<Student: Naman Barde>, <Student: Kaushal kashdoriya>, <Student: Shubham Sharma>, <Student: Mayank Joshi>, <Student: Sneha Joshi>, <Student: Raj Rathod>, <Student: Shubham vyas>, <Student: Sachin Prajapat>, <Student: Aditya Singh Lodhi>, <Student: Mahima Rana>, <Student: Madhur Virli>]>

Short Explanation

This sorts the students based on their marks. By default, the order is
from lowest to highest.

### 6. Get the top three students by marks

Requirement

Get the top three students by marks.

#### ORM Query

## >>> Student.objects.order_by('-marks')[:3]

Output

## <QuerySet [<Student: Madhur Virli>, <Student: Mahima Rana>, <Student: Aditya Singh Lodhi>]>

Short Explanation

This sorts the students from highest to lowest marks and returns the top three for that - is used for descending.

### 7. Get students from a specific department

Requirement

Get students from a specific department.

#### ORM Query

## >>> Student.objects.filter(department__name='Information Technology')

Output

## <QuerySet [<Student: Mayank Joshi>, <Student: Madhur Virli>, <Student: Mahima Rana>]>

Short Explanation

This finds students whose department matches the department we specify.

### 8. Get students enrolled in a specific course

Requirement

Get students enrolled in a specific course.

#### ORM Query

## >>> Student.objects.filter(course__course_name ='AI&DS') 

Output

## <QuerySet [<Student: Mayank Joshi>, <Student: Madhur Virli>, <Student: Mahima Rana>, <Student: Sneha Joshi>, <Student: Raj Rathod>, <Student: Shubham Sharma>]>

Short Explanation

This finds all students who are enrolled in the specified course using the filter.

### 9. Get all courses for one student

Requirement

Get all courses for one student.

#### ORM Query

## >>> madhur = Student.objects.get(name = "Madhur Virli")
>## >> madhur.course.all()

Output

## <QuerySet [<Course: Django (DJDEV101)>, <Course: AI&DS (AIDS101)>]>

Short Explanation

This gets all the courses connected to the selected student.

### 10. Count the total number of students

Requirement

Count the total number of students.

#### ORM Query

## >>> Student.objects.count()

Output

## 11

Short Explanation

This counts the total number of Student records in the database.

### 11. Calculate average marks

Requirement

Calculate the average marks of all students.

#### ORM Query

## >>> from django.db.models import Avg
## >>> Student.objects.aggregate(average= Avg("marks"))

Output

## {'average': 71.18181818181819}

Short Explanation

This calculates the average marks of all students.

### 12. Find the highest and lowest marks

Requirement

Find the highest and lowest marks among all students.

#### ORM Query

## >>> from django.db.models import Max , Min
## >>> Student.objects.aggregate(lowest= Min("marks"), highest = Max("marks"))

Output

## {'highest': 99, 'lowest': 34}

Short Explanation

This finds the highest and lowest marks in the Student records by using the django min and max.

### 13. Count students in each department

Requirement

Count how many students are in each department.

#### ORM Query

## >>> departments = Department.objects.annotate(total_students = Count("students"))
## >>> for department in departments:
## .     print(f"{department.name} : {department.total_students}")

Output

## Computer Science : 2
## Information Technology : 3
## Management : 3
## Lifelong Learning : 2
## Mechanical Engineering : 1

Short Explanation

This adds a student count to each department so we can see how many students belong to it.

### 14. Find departments with more than three students

Requirement

Find departments that have more than three students.

#### ORM Query

## >>> department = Department.objects.annotate(total_students= Count("students")).filter(total_students__gt=3)
## >>> for department in departments:
## ...     print(f"{department.name} : {department.total_students}") 

Output

## <QuerySet []>

Short Explanation

This counts the students in each department and keeps only departments with more than three students using the annotate groups the value and then filter it usinf the __gt.

### 15. Find students who do not have a profile

Requirement

Find students who do not have a StudentProfile.

#### ORM Query

## >>> Student.objects.filter(    
## ...     profile__isnull=True)

Output

## <QuerySet [<Student: Madhur Virli>, <Student: Naman Barde>, <Student: Sachin Prajapat>, <Student: Sneha Joshi>, <Student: Shubham Sharma>, <Student: Shubham vyas>]>

Short Explanation

This finds students whose profile relationship is empty.

### 16. Find students enrolled in more than one course

Requirement

Find students who are enrolled in more than one course.

#### ORM Query

##  >> Student.objects.annotate(total_courses=Count("course")).filter(total_courses__gt=1)

Output

## <QuerySet [<Student: Madhur Virli>]>

Short Explanation

This counts each student's courses and returns only students with more than one course.

### 17. Search students by name or email using Q objects

Requirement

Search for students when the given text appears in either their name or email.

#### ORM Query

## >>> Student.objects.filter(Q(name__icontains="ya")|Q(email__icontains="ya"))

Output

## <QuerySet [<Student: Mayank Joshi>, <Student: Aditya Singh Lodhi>, <Student: Kaushal kashdoriya>, <Student: Shubham vyas>]>

Short Explanation

This uses a Q object to search the name and email fields with an OR condition.

### 18. Update inactive students to active using update()

Requirement

Change all inactive students to active.

#### ORM Query

## >>> Student.objects.filter(active="False").update(active="True") 

Output

## 1

Short Explanation

This finds inactive students and changes their active status to True.

### 19. Delete records with invalid marks, if any

Requirement

Delete students who have invalid marks.

#### ORM Query

## >>> Student.objects.filter(marks__lt=0).delete()

Output

## (0, {})

Short Explanation

This removes student records that have marks below the valid minimum.

### 20. Use select_related() and prefetch_related() appropriately

Requirement

Use select_related() and prefetch_related() for related student data.

#### ORM Query for select_related()

### >>> students = Student.objects.select_related("department")
### >>> 
### >>> for student in students:
### ...     print(student.name, student.department.name)



Output of select_realted()

### Mayank Joshi Information Technology
### Aditya Singh Lodhi Computer Science
### Madhur Virli Information Technology
### Mahima Rana Information Technology
### Naman Barde Management                 
### Sachin Prajapat Management
### Sneha Joshi Computer Science
### Kaushal kashdoriya Lifelong Learning
### Raj Rathod Management
### Shubham Sharma Mechanical Engineering
### Shubham vyas Lifelong Learning

#### ORM Query for perfetch_related()

### >>> students = Student.objects.prefetch_related("course")
### >>> for student in students:
### ...     print(student.name)
### ...     for course in student.course.all():
### ...         print(course.course_name)

Ouput of  perfetch_related()

### Mayank Joshi
### AI&DS
### Aditya Singh Lodhi
### Python Developer
### Madhur Virli
### Django
### AI&DS
### Mahima Rana
### AI&DS
### SQL
### Naman Barde
### Java
### Sachin Prajapat
### Web Development
### Sneha Joshi
### Python Developer
### AI&DS
### SQL
### Kaushal kashdoriya
### Django
### Java
### Raj Rathod
### AI&DS
### Shubham Sharma
### AI&DS
### Web Development
### Shubham vyas
### Web Development


Short Explanation

select_related() is useful for ForeignKey or OneToOne relationships, while prefetch_related() is useful for ManyToMany relationships.