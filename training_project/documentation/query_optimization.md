# Query Optimization — Day 5, Task 2

## Overview

As part of Day 5 Task 2, important QuerySets from the Django project were inspected using:

```python
print(queryset.query)
```

The purpose was to review the generated SQL and verify the use of appropriate Django ORM optimization techniques such as:

* `select_related()`
* `prefetch_related()`
* `distinct()`
* `count()`

Five important QuerySets were inspected.

---

## 1. Trainer Dashboard — Trainer Courses

The trainer dashboard retrieves the courses assigned to the logged-in trainer.

### QuerySet

```python
courses = (
    Course.objects
    .filter(trainer=trainer)
    .prefetch_related("students")
)
```

`Course.trainer` is a `ForeignKey`, while `Course.students` is a `ManyToManyField`.

The `students` relationship is therefore prefetched using:

```python
.prefetch_related("students")
```

### Generated SQL

```sql
SELECT "student_course"."id",
       "student_course"."course_name",
       "student_course"."code",
       "student_course"."duration",
       "student_course"."active_status",
       "student_course"."trainer_id"
FROM "student_course"
INNER JOIN "auth_user"
ON ("student_course"."trainer_id" = "auth_user"."id")
WHERE "auth_user"."username" = bhumi
```

The inspected SQL confirms that Django uses an `INNER JOIN` between `Course` and `User` through the trainer ForeignKey.

---

## 2. Trainer Dashboard — Assigned Students

The trainer dashboard also retrieves students enrolled in courses assigned to the trainer.

### QuerySet

```python
assigned_students = (
    student.objects
    .filter(courses__trainer=trainer)
    .distinct()
)
```

The query traverses the student's ManyToMany relationship with courses and then the course's trainer ForeignKey.

`distinct()` is used to avoid duplicate students when a student is enrolled in multiple courses assigned to the same trainer.

### Generated SQL

```sql
SELECT DISTINCT
       "student_student"."id",
       "student_student"."user_id",
       "student_student"."name",
       "student_student"."email",
       "student_student"."age",
       "student_student"."course",
       "student_student"."marks",
       "student_student"."joined_date",
       "student_student"."active",
       "student_student"."department_id"
FROM "student_student"
INNER JOIN "student_course_students"
ON ("student_student"."id" = "student_course_students"."student_id")
INNER JOIN "student_course"
ON ("student_course_students"."course_id" = "student_course"."id")
INNER JOIN "auth_user"
ON ("student_course"."trainer_id" = "auth_user"."id")
WHERE "auth_user"."username" = bhumi
```

The generated SQL confirms the use of `SELECT DISTINCT` and the joins required to traverse the relationships.

---

## 3. Student Dashboard — Course Marks

The student dashboard retrieves the marks associated with the student's courses.

### QuerySet

```python
marks = (
    student_obj.course_marks
    .select_related("course", "updated_by")
)
```

`CourseMark` contains ForeignKey relationships to:

* `Course`
* `User` through `updated_by`

Therefore, `select_related()` is used.

### Generated SQL

```sql
SELECT "student_coursemark"."id",
       "student_coursemark"."course_id",
       "student_coursemark"."student_id",
       "student_coursemark"."marks",
       "student_coursemark"."updated_by_id",
       "student_coursemark"."updated_at",
       "student_course"."id",
       "student_course"."course_name",
       "student_course"."code",
       "student_course"."duration",
       "student_course"."active_status",
       "student_course"."trainer_id",
       "auth_user"."id",
       "auth_user"."password",
       "auth_user"."last_login",
       "auth_user"."is_superuser",
       "auth_user"."username",
       "auth_user"."first_name",
       "auth_user"."last_name",
       "auth_user"."email",
       "auth_user"."is_staff",
       "auth_user"."is_active",
       "auth_user"."date_joined"
FROM "student_coursemark"
INNER JOIN "student_course"
ON ("student_coursemark"."course_id" = "student_course"."id")
LEFT OUTER JOIN "auth_user"
ON ("student_coursemark"."updated_by_id" = "auth_user"."id")
WHERE "student_coursemark"."student_id" = 16
```

The SQL confirms that Django uses JOINs to retrieve the related `Course` and `User` records together with the `CourseMark` records.

---

## 4. Student Dashboard — Feedback

The student dashboard retrieves feedback belonging to the student.

### QuerySet

```python
feedback = (
    student_obj.feedback_received
    .select_related("course", "trainer")
)
```

`Feedback.course` and `Feedback.trainer` are ForeignKey relationships, so `select_related()` is used.

### Generated SQL

```sql
SELECT "student_feedback"."id",
       "student_feedback"."course_id",
       "student_feedback"."student_id",
       "student_feedback"."trainer_id",
       "student_feedback"."rating",
       "student_feedback"."comment",
       "student_feedback"."is_visible",
       "student_feedback"."created_at",
       "student_feedback"."updated_at",
       "student_course"."id",
       "student_course"."course_name",
       "student_course"."code",
       "student_course"."duration",
       "student_course"."active_status",
       "student_course"."trainer_id",
       "auth_user"."id",
       "auth_user"."password",
       "auth_user"."last_login",
       "auth_user"."is_superuser",
       "auth_user"."username",
       "auth_user"."first_name",
       "auth_user"."last_name",
       "auth_user"."email",
       "auth_user"."is_staff",
       "auth_user"."is_active",
       "auth_user"."date_joined"
FROM "student_feedback"
INNER JOIN "student_course"
ON ("student_feedback"."course_id" = "student_course"."id")
INNER JOIN "auth_user"
ON ("student_feedback"."trainer_id" = "auth_user"."id")
WHERE "student_feedback"."student_id" = 16
ORDER BY "student_feedback"."created_at" DESC
```

The generated SQL confirms that the related course and trainer are retrieved through SQL JOINs.

---

## 5. Audit Logs

The audit log page retrieves audit logs together with the user who performed the action.

### QuerySet

```python
logs = AuditLog.objects.select_related("user")
```

`AuditLog.user` is a ForeignKey, so `select_related()` is appropriate.

### Generated SQL

```sql
SELECT "student_auditlog"."id",
       "student_auditlog"."user_id",
       "student_auditlog"."action",
       "student_auditlog"."action_type",
       "student_auditlog"."description",
       "student_auditlog"."content_type_id",
       "student_auditlog"."object_id",
       "student_auditlog"."ip_address",
       "student_auditlog"."created_at",
       "auth_user"."id",
       "auth_user"."password",
       "auth_user"."last_login",
       "auth_user"."is_superuser",
       "auth_user"."username",
       "auth_user"."first_name",
       "auth_user"."last_name",
       "auth_user"."email",
       "auth_user"."is_staff",
       "auth_user"."is_active",
       "auth_user"."date_joined"
FROM "student_auditlog"
LEFT OUTER JOIN "auth_user"
ON ("student_auditlog"."user_id" = "auth_user"."id")
```

The `LEFT OUTER JOIN` is appropriate because the `AuditLog.user` field allows `NULL`.

---

# `select_related()` and `prefetch_related()`

The queries inspected demonstrate the following usage:

| Query           | Optimization                             | Relationship |
| --------------- | ---------------------------------------- | ------------ |
| Trainer courses | `prefetch_related("students")`           | ManyToMany   |
| Course marks    | `select_related("course", "updated_by")` | ForeignKey   |
| Feedback        | `select_related("course", "trainer")`    | ForeignKey   |
| Audit logs      | `select_related("user")`                 | ForeignKey   |

`select_related()` is used for ForeignKey relationships where related objects can be retrieved through SQL JOINs.

`prefetch_related()` is used for the ManyToMany `Course.students` relationship.

---

# `count()` and `distinct()`

The trainer dashboard uses:

```python
assigned_students.count()
```

to obtain the number of assigned students without using `len()` on the QuerySet.

The assigned-student QuerySet uses:

```python
.distinct()
```

to prevent duplicate student records when the same student is connected to multiple courses assigned to the trainer.

The trainer dashboard course count was also changed from:

```python
len(courses)
```

to:

```python
courses.count()
```

so that the database performs the count rather than relying on the QuerySet length.

---

# Before/After Optimization Documentation

A clear optimization in the project is the student course marks QuerySet.

### Before

```python
marks = student_obj.course_marks.all()
```

The related `course` and `updated_by` objects are not loaded with the initial QuerySet.

If those related objects are accessed while displaying multiple marks, additional database queries may be required.

### After

```python
marks = (
    student_obj.course_marks
    .select_related("course", "updated_by")
)
```

The generated SQL was inspected and confirmed to contain JOINs for both related objects:

```sql
INNER JOIN "student_course"
ON ("student_coursemark"."course_id" = "student_course"."id")

LEFT OUTER JOIN "auth_user"
ON ("student_coursemark"."updated_by_id" = "auth_user"."id")
```

This prepares the related `Course` and `User` objects together with the `CourseMark` records and reduces unnecessary related-object queries.

> Note: A numerical before/after query count was not recorded for this comparison, so this document does not claim a specific number of queries saved.

---

# Summary

Five important QuerySets were inspected using Django's generated SQL:

1. Trainer course QuerySet
2. Trainer assigned-student QuerySet
3. Student course-mark QuerySet
4. Student feedback QuerySet
5. Audit log QuerySet

The inspection confirmed the use of:

* `select_related()` for ForeignKey relationships
* `prefetch_related()` for ManyToMany relationships
* `distinct()` for duplicate prevention
* `count()` for database-side counting

The generated SQL was reviewed directly using Django's QuerySet SQL representation.
