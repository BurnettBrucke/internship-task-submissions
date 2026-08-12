# Django ORM Query Practice

This document lists Django ORM queries, outputs, and explanations for various common operations, executed using the Django interactive shell (`python manage.py shell`).

---

### 1. Get all students

* **Requirement:** Get all students.
* **ORM Query:**
  ```python
  from students.models import Student
  students = Student.objects.all()
  print(students)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Rahul (Python)>, <Student: Priya (Python)>, <Student: Amit (Python)>, <Student: Sneha (Python)>, <Student: Karan (Python)>, <Student: Riya (Python)>, <Student: Neha (Python)>, <Student: Rohit (Python)>, <Student: Ankit (Python)>, <Student: Pooja (Python)>]>
  ```
* **Explanation:** Retrieves a `QuerySet` containing all records from the `Student` table.

---

### 2. Get only active students

* **Requirement:** Get only active students.
* **ORM Query:**
  ```python
  active_students = Student.objects.filter(active_status=True)
  print(active_students)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Rahul (Python)>, <Student: Priya (Python)>, <Student: Sneha (Python)>, <Student: Karan (Python)>, <Student: Riya (Python)>, <Student: Neha (Python)>, <Student: Ankit (Python)>, <Student: Pooja (Python)>]>
  ```
* **Explanation:** Filters the database records, returning only those students whose `active_status` field is set to `True`.

---

### 3. Get students whose marks are greater than or equal to 60

* **Requirement:** Get students whose marks are greater than or equal to 60.
* **ORM Query:**
  ```python
  passing_students = Student.objects.filter(marks__gte=60)
  print(passing_students)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Rahul (Python)>, <Student: Priya (Python)>, <Student: Sneha (Python)>, <Student: Karan (Python)>, <Student: Riya (Python)>, <Student: Ankit (Python)>, <Student: Pooja (Python)>]>
  ```
* **Explanation:** Uses the field lookup helper `__gte` (Greater Than or Equal to) to filter the queryset based on the `marks` field.

---

### 4. Get students whose names contain a given word

* **Requirement:** Get students whose names contain a given word (e.g., `"ya"`).
* **ORM Query:**
  ```python
  matching_students = Student.objects.filter(name__icontains='ya')
  print(matching_students)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Priya (Python)>, <Student: Riya (Python)>]>
  ```
* **Explanation:** Performs a case-insensitive substring search in the database using the `__icontains` lookup on the `name` column.

---

### 5. Order students by marks

* **Requirement:** Order students by marks.
* **ORM Query:**
  * **Ascending Order:**
    ```python
    ordered_asc = Student.objects.order_by('marks')
    print(ordered_asc)
    ```
  * **Descending Order:**
    ```python
    ordered_desc = Student.objects.order_by('-marks')
    print(ordered_desc)
    ```
* **Output (Ascending):**
  ```python
  <QuerySet [<Student: Amit (Python)>, <Student: Rohit (Python)>, <Student: Neha (Python)>, <Student: Riya (Python)>, <Student: Priya (Python)>, <Student: Pooja (Python)>, <Student: Rahul (Python)>, <Student: Karan (Python)>, <Student: Sneha (Python)>, <Student: Ankit (Python)>]>
  ```
* **Explanation:** The `order_by()` method sorts the resulting records. A raw field name sorts ascending, while prefixing the field with `-` sorts descending.

---

### 6. Get the top three students by marks

* **Requirement:** Get the top three students by marks.
* **ORM Query:**
  ```python
  top_three = Student.objects.order_by('-marks')[:3]
  print(top_three)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Ankit (Python)>, <Student: Sneha (Python)>, <Student: Karan (Python)>]>
  ```
* **Explanation:** Orders the students in descending order of `marks` and then applies Python slicing (`[:3]`), which Django translates into a SQL `LIMIT 3` clause.

---

### 7. Get students from a specific department

* **Requirement:** Get students from a specific department (e.g., `"Computer Science"`).
* **ORM Query:**
  ```python
  cs_students = Student.objects.filter(department__name='Computer Science')
  print(cs_students)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Neha (Python)>, <Student: Ankit (Python)>]>
  ```
* **Explanation:** Uses the double-underscore `__` syntax to traverse the ForeignKey relation from `Student` to `Department` and filters by the department's `name` attribute.

---

### 8. Get students enrolled in a specific course

* **Requirement:** Get students enrolled in a specific course (e.g., `"Intro to Programming"`).
* **ORM Query:**
  ```python
  course_students = Student.objects.filter(courses__course_name='Intro to Programming')
  print(course_students)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Rahul (Python)>, <Student: Priya (Python)>, <Student: Riya (Python)>, <Student: Neha (Python)>, <Student: Rohit (Python)>, <Student: Ankit (Python)>, <Student: Pooja (Python)>]>
  ```
* **Explanation:** Performs a join operation through the many-to-many relationship `courses` to filter students based on their enrolled course names.

---

### 9. Get all courses for one student

* **Requirement:** Get all courses for one student (e.g., `"Rahul"`).
* **ORM Query:**
  ```python
  student = Student.objects.filter(name='Rahul').first()
  courses = student.courses.all()
  print(courses)
  ```
* **Output:**
  ```python
  <QuerySet [<Course: Basic Circuit Analysis (EE101)>, <Course: Web Development Bootcamp (CS303)>, <Course: Applied Machine Learning (CS404)>, <Course: Database Management Systems (CS202)>]>
  ```
* **Explanation:** Obtains a specific student instance and uses the reverse/related manager `.courses` with `.all()` to retrieve the set of related `Course` records.

---

### 10. Count the total number of students

* **Requirement:** Count the total number of students.
* **ORM Query:**
  ```python
  total_count = Student.objects.count()
  print(total_count)
  ```
* **Output:**
  ```python
  10
  ```
* **Explanation:** Executes an optimized SQL `SELECT COUNT(*)` query rather than fetching all records into Python memory.

---

### 11. Calculate average marks

* **Requirement:** Calculate average marks.
* **ORM Query:**
  ```python
  from django.db.models import Avg
  avg_marks = Student.objects.aggregate(Avg('marks'))
  print(avg_marks)
  ```
* **Output:**
  ```python
  {'marks__avg': 69.2}
  ```
* **Explanation:** Uses `aggregate()` along with Django's `Avg` aggregate function to compute the arithmetic mean of the `marks` field across all student records.

---

### 12. Find the highest and lowest marks

* **Requirement:** Find the highest and lowest marks.
* **ORM Query:**
  ```python
  from django.db.models import Max, Min
  extreme_marks = Student.objects.aggregate(highest=Max('marks'), lowest=Min('marks'))
  print(extreme_marks)
  ```
* **Output:**
  ```python
  {'highest': 95, 'lowest': 35}
  ```
* **Explanation:** Calculates the minimum and maximum values of the `marks` column in a single SQL aggregation query.

---

### 13. Count students in each department

* **Requirement:** Count students in each department.
* **ORM Query:**
  ```python
  from django.db.models import Count
  from students.models import Department
  dept_counts = Department.objects.annotate(student_count=Count('students'))
  for d in dept_counts:
      print(f"{d.name}: {d.student_count}")
  ```
* **Output:**
  ```text
  Computer Science: 2
  Electrical Engineering: 5
  Mechanical Engineering: 3
  ```
* **Explanation:** Annotates each department record with the count of related students. `students` is the `related_name` defined on the `Student.department` ForeignKey.

---

### 14. Find departments with more than three students

* **Requirement:** Find departments with more than three students.
* **ORM Query:**
  ```python
  from django.db.models import Count
  large_depts = Department.objects.annotate(student_count=Count('students')).filter(student_count__gt=3)
  print(large_depts)
  ```
* **Output:**
  ```python
  <QuerySet [<Department: Electrical Engineering>]>
  ```
* **Explanation:** Annotates departments with their student counts, and then filters that annotated value (`student_count__gt=3`), translating to SQL `GROUP BY` and `HAVING` clauses.

---

### 15. Find students who do not have a profile

* **Requirement:** Find students who do not have a profile.
* **ORM Query:**
  ```python
  no_profile_students = Student.objects.filter(profile__isnull=True)
  print(no_profile_students)
  ```
* **Output:**
  ```python
  <QuerySet []>
  ```
* **Explanation:** Performs an outer join to the OneToOne `StudentProfile` relation (accessed using the `related_name='profile'`) and checks if the association is null using `profile__isnull=True`. Since all seeded students have profiles, an empty queryset is returned.

---

### 16. Find students enrolled in more than one course

* **Requirement:** Find students enrolled in more than one course.
* **ORM Query:**
  ```python
  from django.db.models import Count
  multi_course_students = Student.objects.annotate(course_count=Count('courses')).filter(course_count__gt=1)
  print(multi_course_students)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Rahul (Python)>, <Student: Priya (Python)>, <Student: Amit (Python)>, <Student: Sneha (Python)>, <Student: Karan (Python)>, <Student: Riya (Python)>, <Student: Neha (Python)>, <Student: Rohit (Python)>, <Student: Ankit (Python)>, <Student: Pooja (Python)>]>
  ```
* **Explanation:** Annotates each student with the count of relation records in the many-to-many field `courses` using `Count('courses')` and filters for students having a count strictly greater than 1.

---

### 17. Search students by name or email using Q objects

* **Requirement:** Search students by name or email using Q objects.
* **ORM Query:**
  ```python
  from django.db.models import Q
  search_query = 'priya'
  matching_students = Student.objects.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))
  print(matching_students)
  ```
* **Output:**
  ```python
  <QuerySet [<Student: Priya (Python)>]>
  ```
* **Explanation:** Uses Django's `Q` object to implement logical `OR` queries. It filters the table where either the name contains `'priya'` OR the email contains `'priya'`.

---

### 18. Update inactive students to active using update()

* **Requirement:** Update inactive students to active using update().
* **ORM Query:**
  ```python
  updated_count = Student.objects.filter(active_status=False).update(active_status=True)
  print(updated_count)
  ```
* **Output:**
  ```python
  2
  ```
* **Explanation:** Finds all inactive students and updates their `active_status` to `True` using the `.update()` method. This translates directly to a single SQL `UPDATE` statement and returns the number of affected rows.

---

### 19. Delete records with invalid marks, if any

* **Requirement:** Delete records with invalid marks, if any.
* **ORM Query:**
  ```python
  from django.db.models import Q
  deleted_info = Student.objects.filter(Q(marks__lt=0) | Q(marks__gt=100)).delete()
  print(deleted_info)
  ```
* **Output:**
  ```python
  (0, {'students.Student': 0})
  ```
* **Explanation:** Filters for records where marks are invalid (either `< 0` or `> 100`) using logical `Q` objects, and calls `.delete()`. It returns the total number of deleted objects and a dictionary containing deletions per model.

---

### 20. Use select_related() and prefetch_related() appropriately

* **Requirement:** Use select_related() and prefetch_related() appropriately.
* **ORM Query:**
  ```python
  # 1. select_related for single-value relations (ForeignKey, OneToOne)
  students_with_dept_and_profile = Student.objects.select_related('department', 'profile').all()
  
  # 2. prefetch_related for many-to-many (ManyToMany, Reverse ForeignKey)
  students_with_courses = Student.objects.prefetch_related('courses').all()
  ```
* **Explanation:**
  * `select_related()` uses SQL `JOIN` to retrieve related objects in the same database query. This is appropriate for ForeignKey and OneToOne fields (e.g., `department`, `profile`).
  * `prefetch_related()` executes a separate SQL query for each relation and does the joining in Python, which is appropriate for ManyToMany fields (e.g., `courses`) or reverse relationships.
  * Using both avoids the N+1 query problem, drastically reducing the number of database queries.

---

## Day 4 - Task 3 ORM Challenges (13-22)

### 13. Count assigned students for each trainer

* **Requirement:** Count assigned students for each trainer.
* **ORM Query:**
  ```python
  from django.contrib.auth.models import User
  from django.db.models import Count

  trainers = User.objects.filter(profile__role='trainer').annotate(
      assigned_students_count=Count('assigned_courses__students', distinct=True)
  )
  for trainer in trainers:
      print(f"Trainer: {trainer.username}, Assigned Students: {trainer.assigned_students_count}")
  ```
* **Explanation:** Annotates each User having the role 'trainer' with the count of distinct students enrolled in courses assigned to them (`assigned_courses__students`).

---

### 14. Find students with no visible feedback

* **Requirement:** Find students with no visible feedback.
* **ORM Query:**
  ```python
  from students.models import Student

  students_no_visible_feedback = Student.objects.exclude(feedbacks__is_visible=True).distinct()
  print(students_no_visible_feedback)
  ```
* **Explanation:** Retrieves students by excluding any student that has at least one feedback marked as visible (`is_visible=True`).

---

### 15. Find trainers who have not submitted feedback

* **Requirement:** Find trainers who have not submitted feedback.
* **ORM Query:**
  ```python
  from django.contrib.auth.models import User

  trainers_no_feedback = User.objects.filter(profile__role='trainer').exclude(feedbacks_given__isnull=False)
  print(trainers_no_feedback)
  ```
* **Explanation:** Filters User accounts with the 'trainer' role and excludes those who have at least one record in the reverse relation `feedbacks_given` (null=False).

---

### 16. Get the five latest audit actions

* **Requirement:** Get the five latest audit actions.
* **ORM Query:**
  ```python
  from students.models import AuditLog

  latest_five_audits = AuditLog.objects.all().order_by('-timestamp')[:5]
  print(latest_five_audits)
  ```
* **Explanation:** Queries all `AuditLog` records, orders them descending by their creation timestamp, and uses slicing to limit the query to the top 5 records.

---

### 17. Find users with more than three failed login attempts

* **Requirement:** Find users with more than three failed login attempts.
* **ORM Query:**
  ```python
  from django.contrib.auth.models import User
  from django.db.models import Count, Q

  users_many_failed_logins = User.objects.annotate(
      failed_login_count=Count('audit_logs', filter=Q(audit_logs__action='failed_login'))
  ).filter(failed_login_count__gt=3)
  print(users_many_failed_logins)
  ```
* **Explanation:** Annotates each User with the count of their associated `AuditLog` entries where the action is `'failed_login'` (using conditional aggregation `filter=Q(...)`), and filters for those with count > 3.

---

### 18. Find marks updated during the current week

* **Requirement:** Find marks updated during the current week.
* **ORM Query:**
  ```python
  from django.utils import timezone
  from datetime import timedelta
  from students.models import MarksHistory

  # Assuming week starts from Monday
  now = timezone.now()
  start_of_week = now - timedelta(days=now.weekday())
  start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

  marks_updated_this_week = MarksHistory.objects.filter(timestamp__gte=start_of_week)
  print(marks_updated_this_week)
  ```
* **Explanation:** Calculates the datetime representing the start of the current week (Monday at 00:00:00) and queries `MarksHistory` records created on or after that timestamp.

---

### 19. Calculate average feedback rating by trainer

* **Requirement:** Calculate average feedback rating by trainer.
* **ORM Query:**
  ```python
  from django.contrib.auth.models import User
  from django.db.models import Avg

  trainer_avg_ratings = User.objects.filter(profile__role='trainer').annotate(
      avg_feedback_rating=Avg('feedbacks_given__rating')
  )
  for trainer in trainer_avg_ratings:
      print(f"Trainer: {trainer.username}, Avg Rating: {trainer.avg_feedback_rating}")
  ```
* **Explanation:** Filters trainer users and aggregates the `rating` field of all feedback entries submitted by each trainer (`feedbacks_given__rating`).

---

### 20. Find courses with average marks below 50

* **Requirement:** Find courses with average marks below 50.
* **ORM Query:**
  ```python
  from students.models import Course
  from django.db.models import Avg

  courses_low_marks = Course.objects.annotate(
      avg_student_marks=Avg('students__marks')
  ).filter(avg_student_marks__lt=50)
  print(courses_low_marks)
  ```
* **Explanation:** Joins courses to their enrolled students (`students`), aggregates the average of the student marks (`Avg('students__marks')`), and filters courses where this average is less than 50.

---

### 21. Find inactive users who previously logged in

* **Requirement:** Find inactive users who previously logged in.
* **ORM Query:**
  ```python
  from django.contrib.auth.models import User

  inactive_previously_logged_in = User.objects.filter(
      is_active=False,
      last_login__isnull=False
  )
  print(inactive_previously_logged_in)
  ```
* **Explanation:** Queries Users whose account status is inactive (`is_active=False`) and who have a non-null `last_login` timestamp (indicating they logged in successfully at least once in the past).

---

### 22. Find enrolled students with no marks

* **Requirement:** Find enrolled students with no marks.
* **ORM Query:**
  ```python
  from students.models import Student

  # If marks is nullable
  enrolled_no_marks = Student.objects.filter(marks__isnull=True)
  print(enrolled_no_marks)
  ```
* **Explanation:** Filters the `Student` model for records where the `marks` field is null (meaning no grades have been entered yet).
