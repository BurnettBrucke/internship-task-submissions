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

# Day 4 – Task 3 ORM Challenges

## 21: Count Assigned Students for Each Trainer

### ORM Query
from django.db.models import Count

trainer_student_count = User.objects.filter(
    profile__role='trainer'
).annotate(
    assigned_student_count=Count(
        'assigned_courses__students',
        distinct=True
    )
).values(
    'username',
    'assigned_student_count'
).order_by('username')

list(trainer_student_count)

### Output
[
    {'username': 'Trainer_1', 'assigned_student_count': 6},
    {'username': 'Trainer_2', 'assigned_student_count': 13},
    {'username': 'Trainer_3', 'assigned_student_count': 14},
    {'username': 'Trainer_4', 'assigned_student_count': 7},
    {'username': 'Trainer_5', 'assigned_student_count': 10},
    {'username': 'Trainer_6', 'assigned_student_count': 13},
    {'username': 'Trainer_7', 'assigned_student_count': 10}
]

### Explaination
- profile__role='trainer' → only trainers are selected.
- assigned_courses__students → follows the trainer → course → student relationship.
- Count() → counts assigned students.
- distinct=True → avoids duplicate students when a student is enrolled in multiple courses.
- annotate() → adds the calculated count to each trainer.

## 22: Find Students with No Visible Feedback

### ORM Query
students_without_visible_feedback = Student.objects.filter(
    feedbacks__is_visible=False
).values(
    'name',
    'email'
).distinct()

list(students_without_visible_feedback)

### Output
[
    {'name': 'Rahul Sharma', 'email': 'rahul@gmail.com'},
    {'name': 'Aman Singh', 'email': 'aman@gmail.com'},
    {'name': 'Neha Patel', 'email': 'neha@gmail.com'},
    {'name': 'Jaya Purohit', 'email': 'jaya@gmail.com'},
    {'name': 'Sanjana Dhaker', 'email': 'sanjana@gmail.com'},
    {'name': 'Ruchita Prajapat', 'email': 'ruchita@gmail.com'},
    {'name': 'Himanshu Gepal', 'email': 'himanshu@gmail.com'},
    {'name': 'Mahi Kushwah', 'email': 'mahii@gmail.com'},
    {'name': 'Arjun Sharma', 'email': 'arjun@gmail.com'},
    {'name': 'Sayyam Dhaker', 'email': 'sayyam@gmail.com'},
    {'name': 'Ravi Dubey', 'email': 'ravi@gmail.com'},
    {'name': 'Amit Yadav', 'email': 'amit@gmail.com'},
    {'name': 'Gita Sharma', 'email': 'gita@gmail.com'},
    {'name': 'Ritu Jat', 'email': 'ritu@gmail.com'}
]

### Explaination
- feedbacks__is_visible=False → finds students having feedback marked invisible.
- distinct() → prevents duplicate students.

## 23: Find Trainers Who Have Not Submitted Feedback

### ORM Query
trainers_without_feedback = User.objects.filter(
    profile__role='trainer',
    given_feedbacks__isnull=True
).values(
    'username'
)

list(trainers_without_feedback)

### Output
[
    {'username': 'Trainer_2'},
    {'username': 'Trainer_3'},
    {'username': 'Trainer_4'},
    {'username': 'Trainer_5'},
    {'username': 'Trainer_6'},
    {'username': 'Trainer_7'}
]

### Explaination
- profile__role='trainer' → selects trainers.
- given_feedbacks__isnull=True → finds trainers who have not created any feedback.
- given_feedbacks comes from the Feedback.trainer relationship.

## 24: Get the Five Latest Audit Actions

### ORM Query
latest_audit_actions = AuditLog.objects.select_related(
    'user'
).order_by(
    '-timestamp'
).values(
    'action',
    'description',
    'user__username',
    'timestamp'
)[:5]

list(latest_audit_actions)

### Output
[
    {
        'action': 'Trainer Added',
        'description': 'Trainer Trainer_7 was added successfully.',
        'user__username': 'admin'
    },
    {
        'action': 'Student Updated',
        'description': 'Student Arjun Sharma was updated successfully.',
        'user__username': 'admin'
    },
    {
        'action': 'User Login',
        'description': 'User admin logged in successfully.',
        'user__username': 'admin'
    },
    {
        'action': 'User Logout',
        'description': 'User Trainer_1 logged out successfully.',
        'user__username': 'Trainer_1'
    },
    {
        'action': 'User Login',
        'description': 'User Trainer_1 logged in successfully.',
        'user__username': 'Trainer_1'
    }
]

### Explaination
- select_related('user') → fetches related user efficiently.
- order_by('-timestamp') → newest records first.
- [:5] → returns only five records.

## 25: Find Users with More Than Three Failed Login Attempts

### ORM Query
from django.db.models import Count, Q

users_with_failed_attempts = User.objects.annotate(
    failed_attempt_count=Count(
        'auditlog',
        filter=Q(auditlog__action__icontains='Failed Login')
    )
).filter(
    failed_attempt_count__gt=3
).values(
    'username',
    'failed_attempt_count'
)

list(users_with_failed_attempts)

### Output
[]

### Explaination
The query checks the audit logs associated with users and counts records whose action contains "Failed Login".

failed_attempt_count__gt=3 means:

failed attempts > 3

The current database returned an empty list, which means no user matched this condition based on the currently stored audit-log data.

## 26: Find Marks Updated During the Current Week

### ORM Query
from django.utils import timezone
from datetime import timedelta

today = timezone.localdate()

start_of_week = today - timedelta(days=today.weekday())

marks_updated_this_week = CourseMark.objects.filter(
    updated_at__date__gte=start_of_week,
    updated_at__date__lte=today
).values(
    'student__name',
    'course__course_name',
    'marks',
    'updated_by__username',
    'updated_at'
).order_by('-updated_at')

list(marks_updated_this_week)

### Output
[
    {
        'student__name': 'Deepika Vishwakarma',
        'course__course_name': 'Data Science',
        'marks': 90,
        'updated_by__username': 'Trainer_1'
    }
]

### Explaination
- timezone.localdate() → gets the current local date.
- today.weekday() → determines the current day's position in the week.
- start_of_week → calculates the beginning of the current week.
- updated_at__date__gte → includes records from the start of the week.
- updated_at__date__lte → includes records up to today.

## 27: Calculate Average Feedback Rating by Trainer

### ORM Query
from django.db.models import Avg

trainer_average_rating = User.objects.filter(
    profile__role='trainer'
).annotate(
    average_rating=Avg('given_feedbacks__rating')
).values(
    'username',
    'average_rating'
).order_by('username')

list(trainer_average_rating)

### Output
[
    {'username': 'Trainer_1', 'average_rating': 5.0},
    {'username': 'Trainer_2', 'average_rating': None},
    {'username': 'Trainer_3', 'average_rating': None},
    {'username': 'Trainer_4', 'average_rating': None},
    {'username': 'Trainer_5', 'average_rating': None},
    {'username': 'Trainer_6', 'average_rating': None},
    {'username': 'Trainer_7', 'average_rating': None}
]

### Explaination
- Avg() calculates the average feedback rating.
- given_feedbacks is the reverse relationship from Feedback.trainer.
- None means that the trainer currently has no feedback records.

## 28: Find Courses with Average Marks Below 50

### ORM Query
course_average_marks = Course.objects.annotate(
    average_marks=Avg('course_marks__marks')
).filter(
    average_marks__lt=50
).values(
    'course_name',
    'average_marks'
).order_by('course_name')

list(course_average_marks)

### Output
[]

### Explaination
- Avg('course_marks__marks') calculates the average marks for each course.
- average_marks__lt=50 filters courses whose average marks are below 50.
- Empty result means no course currently has an average below 50.

## 29: Find Inactive Users Who Previously Logged In

### ORM Query
inactive_users_previously_logged_in = User.objects.filter(
    is_active=False,
    last_login__isnull=False
).values(
    'username',
    'last_login'
)

list(inactive_users_previously_logged_in)

### Output
[
    {
        'username': 'Trainer_2',
        'last_login': '2026-09-17 09:26:25'
    },
    {
        'username': 'Trainer_4',
        'last_login': '2026-09-17 09:39:21'
    }
]

### Explaination
- is_active=False → user is currently inactive.
- last_login__isnull=False → user has logged in at least once previously.
- Therefore, the query identifies inactive accounts that have a previous login history.

## 30: Find Enrolled Students with No Marks

### ORM Query
enrolled_students_no_marks = Student.objects.filter(
    courses__isnull=False,
    course_marks__isnull=True
).distinct().values(
    'name',
    'email'
)

list(enrolled_students_no_marks)

### Output
[
    {'name': 'Aman Singh', 'email': 'aman@gmail.com'},
    {'name': 'Jaya Purohit', 'email': 'jaya@gmail.com'},
    {'name': 'Rahul Sharma', 'email': 'rahul@gmail.com'},
    {'name': 'Neha Patel', 'email': 'neha@gmail.com'},
    {'name': 'Sanjana Dhaker', 'email': 'sanjana@gmail.com'},
    {'name': 'Ruchita Prajapat', 'email': 'ruchita@gmail.com'},
    {'name': 'Himanshu Gepal', 'email': 'himanshu@gmail.com'},
    {'name': 'Mahi Kushwah', 'email': 'mahii@gmail.com'},
    {'name': 'Sayyam Dhaker', 'email': 'sayyam@gmail.com'},
    {'name': 'Ritu Jat', 'email': 'ritu@gmail.com'},
    {'name': 'Gita Sharma', 'email': 'gita@gmail.com'},
    {'name': 'Amit Yadav', 'email': 'amit@gmail.com'},
    {'name': 'Arjun Sharma', 'email': 'arjun@gmail.com'}
]

### Explaination
- courses__isnull=False → student is enrolled in at least one course.
- course_marks__isnull=True → student has no CourseMark record.
- distinct() → prevents duplicate students when multiple courses are involved.

