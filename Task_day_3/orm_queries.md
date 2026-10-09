### Requirement
Get all students.
### ORM Query 1:
Student.objects.all()

### Output:
<QuerySet [<Student: Riya>, <Student: Priya>, <Student: mahi>, <Student: Rahul>, <Student: ruhi>, <Student: kunal>, <Student: maya>, <Student: pihu>, <Student: mohit>]

### Explanation: 
This query retrieves all student records from the database.

# Query 2 — Get only active students

### Requirement
Get only active students.

Student.objects.filter(active_status=True)

# output: <QuerySet [<Student: Riya>, <Student: Priya>, <Student: mahi>, <Student: Rahul>, <Student: kunal>, <Student: pihu>, <Student: mohit>]>

## Explanation:
This query filters the Student records and returns only students whose active_status is True.

## Query 3 — Marks greater than or equal to 60

### Requirement
Get students whose marks are greater than or equal to 60.

Student.objects.filter(marks__gte=60)

# output : <QuerySet [<Student: Riya>, <Student: Priya>, <Student: mahi>, <Student: kunal>, <Student: mohit>]>
>>> 

# Explanation:
This query returns students whose marks are greater than or equal to 60. The __gte lookup means "greater than or equal to".


### Ab Query 4 — Names contain a given word
### Requirement
Get students whose marks are greater than or equal to 60.

Student.objects.filter(name__icontains='ri')

# output :
<QuerySet [<Student: Riya>, <Student: Priya>]>

# Explanation:
This query searches for students whose names contain the given word or characters. The __icontains lookup performs a case-insensitive search.

## Query 5 — Order students by marks
### Requirement
Get students whose marks are greater than or equal to 60.

Student.objects.order_by('marks')

# output :
<QuerySet [<Student: ruhi>, <Student: maya>, <Student: Rahul>, <Student: pihu>, <Student: kunal>, <Student: mahi>, <Student: Riya>, <Student: Priya>, <Student: mohit>]>
>>> 

# Explanation:
This query orders all students by their marks in ascending order, from lowest marks to highest marks.


### Query 6 — Top three students by marks
### Requirement
Get the top three students by marks.

Student.objects.order_by('-marks')[:3]

# output :
<QuerySet [<Student: mohit>, <Student: Riya>, <Student: Priya>]>

# Explanation:
This query orders students by marks in descending order using -marks and returns only the top three students using [:3].

>>> Department.objects.all()
<QuerySet [<Department: Computer Science>, <Department: Information Technology>, <Department: Electronics>]>
>>> 

## 7. Get students from a specific department
### Requirement
Get students from a specific department.

Student.objects.filter(department__name='Computer Science')

# output :
<QuerySet [<Student: Riya>, <Student: mahi>, <Student: ruhi>, <Student: pihu>, <Student: mohit>]>

# Explanation:
This query retrieves students who belong to the "Computer Science" department by filtering through the Department model using the ForeignKey relationship

## 8. Get students enrolled in a specific course
### Requirement
Get students enrolled in a specific course.

Student.objects.filter(courses__course_name='Python Development')

# output :
<QuerySet [<Student: pihu>, <Student: maya>, <Student: ruhi>, <Student: mahi>, <Student: Priya>, <Student: mohit>]>

# Explanation:
This query retrieves students enrolled in the "Python Development" course by filtering through the ManyToMany relationship between Student and Course.

## 9. Get all courses for one student

### Requirement
Get all courses for one student.

### ORM Query
Student.objects.get(name='pihu').courses.all()

# output :
<QuerySet [<Course: Python Development>, <Course: Django Development>]

# Explanation:
This query first retrieves the student named "pihu" and then uses the ManyToMany relationship to retrieve all courses assigned to that student.

## 10. Count the total number of students
### Requirement
Count the total number of students.

### ORM Query
Student.objects.count()

# output :
9

# Explanation:
This query counts the total number of student records in the database.

## 11. Calculate average marks
### Requirement
Calculate the average marks of all students.
from django.db.models import Avg

Student.objects.aggregate(Avg('marks'))
# output :
{'marks__avg': 60.55555555555556}
# Explanation:
This query calculates the average marks of all students using Django's Avg aggregation function.

## 12. Find the highest and lowest marks

### Requirement
Find the highest and lowest marks.

from django.db.models import Max, Min

Student.objects.aggregate(
    highest_marks=Max('marks'),
    lowest_marks=Min('marks')
)
# output :
{'highest_marks': 96, 'lowest_marks': 17}
# Explanation:
This query uses Django's Max and Min aggregation functions to find the highest and lowest marks among all students.

### Query 13. Count students in each department
### Requirement
Count the number of students in each department.

from django.db.models import Count

Department.objects.annotate(
    student_count=Count('students')
).values('name', 'student_count')
# output :
<QuerySet [{'name': 'Computer Science', 'student_count': 5}, {'name': 'Information Technology', 'student_count': 2}, {'name': 'Electronics', 'student_count': 2}]

# Explanation:
Count('students') counts the students belonging to each department.
annotate() adds the calculated student count to each department.

### Query 14. Find departments with more than three students
### Requirement
Find departments that have more than 3 students.

Department.objects.annotate(
    student_count=Count('students')
).filter(
    student_count__gt=3
).values('name', 'student_count')

# output :
<QuerySet [{'name': 'Computer Science', 'student_count': 5}]

# Explanation:
The query counts students in each department and filters only those departments where the student count is greater than 3.
In the current data, only the Computer Science department has more than 3 students.

### Query 15. Find students who do not have a profile
### Requirement
Find students who do not have a StudentProfile.

Student.objects.filter(profile__isnull=True)
# output :
<QuerySet [<Student: mahi>, <Student: ruhi>, <Student: pihu>, <Student: mohit>]

# Explanation:
profile__isnull=True finds students for whom no related StudentProfile record exists.
In the current data, mahi, ruhi, pihu, and mohit do not have a profile.

### Query 16.Find students enrolled in more than one course
### Requirement
Find students who are enrolled in more than one course.

Student.objects.annotate(
    course_count=Count('courses')
).filter(
    course_count__gt=1
)
# output :
<QuerySet [<Student: Riya>, <Student: mahi>, <Student: ruhi>, <Student: pihu>, <Student: mohit>, <Student: Rahul>, <Student: maya>, <Student: kunal>]>

# Explanation:
Count('courses') counts the courses associated with each student.
filter(course_count__gt=1) returns only students who are enrolled in more than one course.

### Query 17.Search students by name or email using Q objects
### Requirement
Search students whose name or email contains a given word.

Student.objects.filter(
    Q(name__icontains='ri') |
    Q(email__icontains='ri')
)
# output :
<QuerySet [<Student: Riya>, <Student: Priya>]>

# Explanation:
Q objects are used to combine multiple conditions.
The | operator represents OR, so the query searches for students whose name or email contains ri, without considering letter case.

### Query 18.Update inactive students to active using update()
### Requirement
Update all inactive students and make them active using update().

Student.objects.filter(active_status=False).update(active_status=True)
# output :
>>> Student.objects.filter(active_status=False).update(active_status=True)
2
>>> 
# Explanation:
filter(active_status=False) selects all inactive students.
update(active_status=True) changes their status to active directly in the database.
The output 2 means that 2 student records were updated.

### Query 19.Delete records with invalid marks
### Requirement

Find and delete student records having invalid marks, i.e. marks less than 0 or greater than 100.

Student.objects.filter(
    Q(marks__lt=0) | Q(marks__gt=100)
)
# output :
Delete records with invalid marks
Requirement

Find and delete student records having invalid marks, i.e. marks less than 0 or greater than 100.

Student.objects.filter(
    Q(marks__lt=0) | Q(marks__gt=100)
)
# Explanation:
The query checks for students whose marks are less than 0 or greater than 100.
The output is an empty QuerySet, which means there are no students with invalid marks, so no records were deleted.

### Query 20.Use select_related() and prefetch_related() appropriately
### Requirement

Use select_related() and prefetch_related() to efficiently retrieve related data.

Student.objects.select_related(
    'department'
).prefetch_related(
    'courses'
)
# output :
<QuerySet [<Student: Riya>, <Student: Priya>, <Student: mahi>, <Student: Rahul>, <Student: ruhi>, <Student: kunal>, <Student: maya>, <Student: pihu>, <Student: mohit>]>

# Explanation:
select_related('department') is used for the ForeignKey relationship between Student and Department. It retrieves the related department using a SQL JOIN.
prefetch_related('courses') is used for the ManyToMany relationship between Student and Course. It retrieves related courses efficiently using separate queries.
This helps reduce unnecessary database queries when accessing related data.
