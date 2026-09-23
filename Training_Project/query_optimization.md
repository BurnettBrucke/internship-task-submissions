# Query Optimization and Performance Review

## 1. Objective

The purpose of this review is to identify potential N+1 query problems, inspect important QuerySets, and apply Django ORM optimizations using:

- `select_related()`
- `prefetch_related()`
- `count()`
- `exists()`
- `annotate()`
- `values()` / `values_list()`
- Query inspection using `QuerySet.query`

---

## 2. Important QuerySets Inspected

### QuerySet 1 — Basic Student Query

students = Student.objects.all()

**Generated SQL:**
    SELECT ...
    FROM "students_student"

This is a basic query that retrieves student records.

### QuerySet 2 — Student Course Count

**Before optimization:**
    students = Student.objects.annotate(
        course_count=Count('courses')
    )

Django generated a LEFT OUTER JOIN with the student-course intermediate table and used COUNT() to calculate the number of courses for each student.

This avoids executing a separate course-count query for every student.

### QuerySet 3 — Students Assigned to a Trainer

assigned_students = Student.objects.filter(
    courses__trainer=1
).distinct()

**The generated SQL uses joins between:**

Student
   ↓
Student-Course relationship
   ↓
Course
   ↓
Course-Trainer relationship

distinct() prevents duplicate student records when a student is assigned to multiple courses handled by the same trainer.

### QuerySet 4 — Active Courses for a Student

active_courses = Course.objects.filter(
    students__user__username="demo_student",
    active=True
)

**The generated SQL joins:**

Course
   ↓
Student-Course relationship
   ↓
Student
   ↓
User

and filters only active courses belonging to the selected student.

### QuerySet 5 — Feedback with Related Objects

feedback = Feedback.objects.select_related(
    'student',
    'trainer',
    'course'
)

**The generated SQL uses joins to fetch:**

- Feedback
- Student
- Trainer
- Course

in the same main query.

This is useful because these relationships are ForeignKey relationships and can be optimized with select_related().

## 3. Before and After Optimization

#### Before

students = Student.objects.annotate(
    course_count=Count('courses')
)

This QuerySet calculates the course count using a SQL aggregation.

However, if the template also accesses related department, user, or individual courses, additional queries may be generated for those relationships.

#### After

students = Student.objects.select_related(
    'department',
    'user'
).prefetch_related(
    'courses'
).annotate(
    course_count=Count('courses')
)

#### Improvements

**select_related() is used for:**

- Student -> Department ForeignKey
- Student -> User OneToOne relationship

It uses SQL joins to retrieve related objects together with the student query.

**prefetch_related() is used for:**

- Student -> Courses ManyToMany relationship

It retrieves related courses efficiently using additional query processing instead of repeatedly querying courses for every student.

## 4. N+1 Query Review

An N+1 query problem can occur when the application first retrieves a list of objects and then performs an additional query for each object to access related data.

#### For example:

students = Student.objects.all()

for student in students:
    print(student.department.name)

Without appropriate optimization, this can result in repeated database queries.

#### Using:

Student.objects.select_related('department')
allows Django to fetch the related department data using a SQL join.

#### For ManyToMany relationships such as courses:

Student.objects.prefetch_related('courses')
can reduce repeated queries when accessing courses for multiple students.

## 5. Relationship Optimization Used in the Project

| Relationship         | Type       | Optimization         |
| -------------------- | ---------- | -------------------- |
| Student → Department | ForeignKey | `select_related()`   |
| Student → User       | OneToOne   | `select_related()`   |
| Student → Courses    | ManyToMany | `prefetch_related()` |
| Feedback → Student   | ForeignKey | `select_related()`   |
| Feedback → Trainer   | ForeignKey | `select_related()`   |
| Feedback → Course    | ForeignKey | `select_related()`   |

## 6. Query Inspection

**Generated SQL was inspected using:**

print(queryset.query)

**The following important QuerySets and query patterns were inspected:**

- Basic Student Query
- Student Course Count using annotate(Count('courses'))
- Students Assigned to a Trainer
- Active Courses for a Student
- Feedback with Related Objects

**The optimized Student List Query was also reviewed to verify the use of:**

- select_related('department', 'user')
- prefetch_related('courses')
- annotate(Count('courses'))

This helped verify how Django ORM relationships and optimization techniques are translated into SQL queries.

## 7. Conclusion

The project already uses several Django ORM optimization techniques, including:

- select_related()
- prefetch_related()
- annotate()
- Count()
- exists()
- distinct()

These techniques reduce unnecessary database queries and help prevent N+1 query problems.

The query inspection also provides a clearer understanding of how Django ORM operations are converted into SQL.