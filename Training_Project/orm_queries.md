# Django ORM Query Practice

## Overview

This file contains the Django ORM queries practiced using the Django shell for the Student Management project.

---

## 1. Get All Students

### Requirement
Get all students from the database.

### ORM Query
Student.objects.all()

### Output
<QuerySet [<Student: Rahul Sharma>, <Student: Aman Singh>, <Student: Neha Patel>, <Student: Deepika Vishwakarma>, <Student: Jaya Purohit>, <Student: Sanjana Dhaker>, <Student: Ruchita Prajapat>, <Student: Himanshu Gepal>, <Student: Nandini Jain>, <Student: Mahi Kushwah>, <Student: Arjun Patel>, <Student: Sayyam Dhaker>]>

### Explanation
objects.all() returns all student records from the Student table.

## 2. Get Only Active Students

### Requirement
Get students whose active status is True.

### ORM Query
Student.objects.filter(active=True)

### Output
<QuerySet [<Student: Rahul Sharma>, <Student: Neha Patel>, <Student: Deepika Vishwakarma>, <Student: Jaya Purohit>, <Student: Sanjana Dhaker>, <Student: Ruchita Prajapat>, <Student: Himanshu Gepal>, <Student: Nandini Jain>, <Student: Mahi Kushwah>, <Student: Arjun Patel>, <Student: Sayyam Dhaker>]>

### Explanation
filter(active=True) returns only active students.

## 3. Get Students with Marks >= 60

### Requirement
Find students who scored 60 or more marks.

### ORM Query
Student.objects.filter(marks__gte=60)

### Output
<QuerySet [<Student: Neha Patel>, <Student: Deepika Vishwakarma>, <Student: Jaya Purohit>, <Student: Sanjana Dhaker>, <Student: Ruchita Prajapat>, <Student: Himanshu Gepal>, <Student: Nandini Jain>]>

### Explanation
__gte means "greater than or equal to".

## 4. Get Students Whose Name Contains a Given Word

### Requirement
Find students whose name contains the letter "a".

### ORM Query
Student.objects.filter(name__icontains="a")

### Output
<QuerySet [<Student: Rahul Sharma>, <Student: Aman Singh>, <Student: Neha Patel>, <Student: Deepika Vishwakarma>, <Student: Jaya Purohit>, <Student: Sanjana Dhaker>, <Student: Ruchita Prajapat>, <Student: Himanshu Gepal>, <Student: Nandini Jain>, <Student: Mahi Kushwah>, <Student: Arjun Patel>, <Student: Sayyam Dhaker>]>

### Explanation
icontains performs a case-insensitive search.

## 5. Order Students by Marks

### Requirement
Arrange students from lowest marks to highest marks.

### ORM Query
Student.objects.order_by('marks')

### Output
<QuerySet [<Student: Aman Singh>, <Student: Sayyam Dhaker>, <Student: Arjun Patel>, <Student: Rahul Sharma>, <Student: Mahi Kushwah>, <Student: Nandini Jain>, <Student: Jaya Purohit>, <Student: Ruchita Prajapat>, <Student: Neha Patel>, <Student: Sanjana Dhaker>, <Student: Deepika Vishwakarma>, <Student: Himanshu Gepal>]>

### Explanation
order_by('marks') sorts the records in ascending order.

## 6. Get Top Three Students by Marks

### Requirement
Find the top three students based on marks.

### ORM Query
Student.objects.order_by('-marks')[:3]

### Output
<QuerySet [<Student: Himanshu Gepal>, <Student: Deepika Vishwakarma>, <Student: Sanjana Dhaker>]>

### Explanation
-marks sorts marks in descending order. [:3] selects the first three records.

## 7. Get Students from a Specific Department

### Requirement
Get students from the Computer Science department.

### ORM Query
Student.objects.filter(department__name="Computer Science")

### Output
<QuerySet [<Student: Arjun Patel>, <Student: Sayyam Dhaker>]>

### Explanation
The double underscore __ is used to access a related model field.

## 8. Get Students Enrolled in a Specific Course

### Requirement
Get students enrolled in Python Programming.

### ORM Query
Student.objects.filter(courses__course_name="Python Programming")

### Output
<QuerySet [<Student: Aman Singh>, <Student: Rahul Sharma>, <Student: Neha Patel>, <Student: Deepika Vishwakarma>, <Student: Jaya Purohit>, <Student: Sanjana Dhaker>, <Student: Ruchita Prajapat>, <Student: Himanshu Gepal>, <Student: Nandini Jain>, <Student: Mahi Kushwah>, <Student: Arjun Patel>, <Student: Sayyam Dhaker>]>

### Explanation
This query uses the Many-to-Many relationship between Student and Course.

## 9. Get All Courses for One Student

### Requirement
Get all courses enrolled by Deepika Vishwakarma.

### ORM Query
Student.objects.get(name="Deepika Vishwakarma").courses.all()

### Output
<QuerySet [<Course: Django Development (DJ102)>, <Course: Data Science (DS103)>, <Course: Machine Learning (ML104)>, <Course: Python Programming (PY101)>, <Course: Web Development (WD105)>]>

### Explanation
The courses related name is used to access all courses of a student.

## 10. Count Total Students

### Requirement
Find the total number of students.

### ORM Query
Student.objects.count()

### Output
12

### Explanation
count() returns the number of records in the QuerySet.

## 11. Find Average Marks

### Requirement
Calculate the average marks of all students.

### ORM Query
Student.objects.aggregate(Avg('marks'))

### Output
{'marks__avg': 67.5}

### Explanation
Avg() calculates the average value of the marks field.

## 12. Find Highest and Lowest Marks

### Requirement
Find the highest and lowest marks.

### ORM Query
Student.objects.aggregate(Min('marks'), Max('marks'))

### Output
{'marks__min': 35, 'marks__max': 94}

### Explanation
Min() returns the lowest value and Max() returns the highest value.

## 13. Count Students in Each Department

### Requirement
Find the number of students in every department.

### ORM Query
Department.objects.annotate(
    student_count=Count('students')
).values('name', 'student_count')

### Output
<QuerySet [{'name': 'Computer Science', 'student_count': 2}, {'name': 'Information technology', 'student_count': 0}, {'name': 'Data Science', 'student_count': 0}]>

### Explanation
annotate() adds a calculated field to each department. Count() counts the students related to each department.

## 14. Departments with More Than Three Students

### Requirement
Find departments that have more than three students.

### ORM Query
Department.objects.annotate(
    student_count=Count('students')
).filter(student_count__gt=3)

### Output
<QuerySet []>

### Explanation
__gt=3 means greater than 3. The empty QuerySet means no department currently has more than three students.

15. Students Without a Profile

### Requirement
Find students who do not have a StudentProfile.

### ORM Query
Student.objects.filter(profile__isnull=True)

### Output
<QuerySet [<Student: Rahul Sharma>, <Student: Jaya Purohit>, <Student: Sanjana Dhaker>, <Student: Ruchita Prajapat>, <Student: Mahi Kushwah>, <Student: Arjun Patel>, <Student: Sayyam Dhaker>]>

### Explanation
isnull=True finds records where the related profile does not exist.

## 16. Students Enrolled in More Than One Course

### Requirement
Find students who are enrolled in more than one course.

### ORM Query
Student.objects.annotate(
    course_count=Count('courses')
).filter(course_count__gt=1)

### Output
<QuerySet [<Student: Rahul Sharma>, <Student: Aman Singh>, <Student: Neha Patel>, <Student: Deepika Vishwakarma>, <Student: Jaya Purohit>, <Student: Sanjana Dhaker>, <Student: Ruchita Prajapat>, <Student: Himanshu Gepal>, <Student: Nandini Jain>, <Student: Mahi Kushwah>, <Student: Arjun Patel>, <Student: Sayyam Dhaker>]>

### Explanation
Count('courses') counts courses for every student. __gt=1 selects students with more than one course.

## 17. Search Students by Name or Email using Q Objects

### Requirement
Search for a student using either name or email.

### ORM Query
Student.objects.filter(
    Q(name__icontains="Deepika") |
    Q(email__icontains="Deepika")
)

### Output
<QuerySet [<Student: Deepika Vishwakarma>]>

### Explanation
Q objects are used to create complex queries. The | operator means OR.

## 18. Update Inactive Students to Active

### Requirement
Update all inactive students and make them active.

### ORM Query
Student.objects.filter(active=False).update(active=True)

### Output
1

### Explanation
update() changes the selected records directly in the database. The output 1 means one inactive student was updated.

#19. Delete Records with Invalid Marks

### Requirement
Check for students whose marks are below 0 or above 100.

### ORM Query
Student.objects.filter(
    Q(marks__lt=0) | Q(marks__gt=100)
)

### Output
<QuerySet []>

### Explanation
No students had invalid marks, so no records were deleted. Valid marks are between 0 and 100.

## 20. Use select_related() and prefetch_related()

### Requirement
Fetch students along with their related department and courses efficiently.

### ORM Query
Student.objects.select_related(
    'department'
).prefetch_related(
    'courses'
).all()

### Output
<QuerySet [<Student: Rahul Sharma>, <Student: Aman Singh>, <Student: Neha Patel>, <Student: Deepika Vishwakarma>, <Student: Jaya Purohit>, <Student: Sanjana Dhaker>, <Student: Ruchita Prajapat>, <Student: Himanshu Gepal>, <Student: Nandini Jain>, <Student: Mahi Kushwah>, <Student: Arjun Patel>, <Student: Sayyam Dhaker>]>

### Explanation
- select_related() is useful for ForeignKey and OneToOne relationships.

- prefetch_related() is useful for Many-to-Many and reverse relationships.

- Here, department is a ForeignKey, so select_related() is used, while courses is a Many-to-Many relationship, so prefetch_related() is used.