# API Design Plan

This document defines the REST API design for the Student Training Portal.

The purpose of this plan is to identify the main resources that can be exposed through an API and define the endpoints, request data, response data, permissions, and expected HTTP status codes.

This is a **design document only**. API implementation is not included in this task.

The API should reuse the existing Django models, role-based permissions, validation rules, and service-layer logic wherever possible. This prevents the API from duplicating business logic already used by the web application.

---

## 1. Resources to Expose

The following resources are suitable for API access:

| Resource    | Existing Model / Data                         | Purpose                                              |
| ----------- | --------------------------------------------- | ---------------------------------------------------- |
| Students    | `student`                                     | Manage and retrieve student information              |
| Courses     | `Course`                                      | View and manage available training courses           |
| Enrollments | `Course.students`                             | Manage student-course enrollment                     |
| Marks       | `CourseMark`, `MarksHistory`, `student.marks` | Submit marks and maintain marks history              |
| Feedback    | `Feedback`                                    | Allow trainers to create and manage student feedback |

### Resource Relationships

The main relationships between these resources are:

```text
Student
   │
   ├── Enrollments ─── Course
   │
   ├── Marks ───────── Course
   │
   └── Feedback ────── Trainer
```

A student can be enrolled in multiple courses, and a course can contain multiple students.

Marks and feedback are associated with a student and a course.

---

# 2. Authentication and Permissions

All API endpoints should require authentication.

The API should follow the same role-based access rules already used by the Student Training Portal.

The main roles are:

* **Admin**
* **Trainer**
* **Student**

The API should not bypass the existing permission rules.

Where possible, API views should reuse the existing service-layer functions such as the marks and feedback services instead of implementing the same business rules again.

### General Permission Rules

| Role    | General API Access                                                                     |
| ------- | -------------------------------------------------------------------------------------- |
| Admin   | Can access and manage permitted resources                                              |
| Trainer | Can access assigned courses/students and manage marks/feedback                         |
| Student | Can access their own student information, enrolled courses, marks and visible feedback |

### Common Status Codes

| Status Code        | Meaning                                                                |
| ------------------ | ---------------------------------------------------------------------- |
| `200 OK`           | Successful request                                                     |
| `201 Created`      | Resource successfully created                                          |
| `204 No Content`   | Resource successfully deleted                                          |
| `400 Bad Request`  | Invalid or incomplete request data                                     |
| `401 Unauthorized` | User is not authenticated                                              |
| `403 Forbidden`    | User is authenticated but does not have permission                     |
| `404 Not Found`    | Requested resource does not exist or is not available to the requester |

---

# 3. Students API

The Students API provides access to student records.

## Student Endpoints

| Method | Endpoint              | Purpose                             | Request Data                                                                     | Response Data           | Permissions                                                          | Status Codes                      |
| ------ | --------------------- | ----------------------------------- | -------------------------------------------------------------------------------- | ----------------------- | -------------------------------------------------------------------- | --------------------------------- |
| GET    | `/api/students/`      | List permitted students             | Optional filters such as `department`, `course`, `status`, `result`, `q`, `page` | List of student records | Admin: all students. Trainer: assigned students. Student: own record | `200`, `401`                      |
| POST   | `/api/students/`      | Create a student                    | `name`, `email`, `age`, `marks`, `department`, `courses`, `is_active`            | Created student record  | Admin only                                                           | `201`, `400`, `401`, `403`        |
| GET    | `/api/students/{id}/` | Retrieve one student                | No request body                                                                  | Student details         | Admin: any. Trainer: assigned student. Student: own record           | `200`, `401`, `403`, `404`        |
| PATCH  | `/api/students/{id}/` | Update selected student fields      | Fields to update                                                                 | Updated student record  | Admin only                                                           | `200`, `400`, `401`, `403`, `404` |
| DELETE | `/api/students/{id}/` | Delete a student                    | No request body                                                                  | No response body        | Admin only                                                           | `204`, `401`, `403`, `404`        |
| GET    | `/api/students/me/`   | Retrieve logged-in student's record | No request body                                                                  | Student details         | Student only                                                         | `200`, `401`, `404`               |

### Example Student Response

```json
{
    "id": 15,
    "name": "Student Name",
    "email": "student@example.com",
    "age": 22,
    "marks": 78,
    "department": 2,
    "is_active": true
}
```

---

# 4. Courses API

The Courses API provides access to the training courses available in the portal.

## Course Endpoints

| Method | Endpoint             | Purpose                   | Request Data                                   | Response Data    | Permissions         | Status Codes                      |
| ------ | -------------------- | ------------------------- | ---------------------------------------------- | ---------------- | ------------------- | --------------------------------- |
| GET    | `/api/courses/`      | List available courses    | Optional filters such as `trainer` or `active` | List of courses  | Authenticated users | `200`, `401`                      |
| POST   | `/api/courses/`      | Create a course           | `course_name`, `code`, `duration`, `trainer`   | Created course   | Admin only          | `201`, `400`, `401`, `403`        |
| GET    | `/api/courses/{id}/` | Retrieve course details   | No request body                                | Course details   | Authenticated users | `200`, `401`, `404`               |
| PATCH  | `/api/courses/{id}/` | Update course information | Fields to update                               | Updated course   | Admin only          | `200`, `400`, `401`, `403`, `404` |
| DELETE | `/api/courses/{id}/` | Delete a course           | No request body                                | No response body | Admin only          | `204`, `401`, `403`, `404`        |

### Example Course Response

```json
{
    "id": 3,
    "course_name": "Python and Django",
    "code": "PY-DJ",
    "duration": 12,
    "active_status": true,
    "trainer": 7
}
```

---

# 5. Enrollments API

Enrollment connects a student with a course through the course-student many-to-many relationship.

The enrollment API provides separate endpoints for adding and removing students from courses instead of requiring the complete student record to be updated.

## Enrollment Endpoints

| Method | Endpoint                                  | Purpose                            | Request Data    | Response Data                  | Permissions                                                | Status Codes                      |
| ------ | ----------------------------------------- | ---------------------------------- | --------------- | ------------------------------ | ---------------------------------------------------------- | --------------------------------- |
| GET    | `/api/students/{id}/courses/`             | List courses enrolled by a student | No request body | List of courses                | Admin: any. Trainer: assigned student. Student: own record | `200`, `401`, `403`, `404`        |
| POST   | `/api/students/{id}/courses/`             | Enroll a student in a course       | `course_id`     | Updated enrollment/course data | Admin only                                                 | `201`, `400`, `401`, `403`, `404` |
| DELETE | `/api/students/{id}/courses/{course_id}/` | Remove a student from a course     | No request body | No response body               | Admin only                                                 | `204`, `401`, `403`, `404`        |

### Example Enrollment Request

```json
{
    "course_id": 3
}
```

### Example Enrollment Response

```json
{
    "student_id": 15,
    "course_id": 3,
    "status": "enrolled"
}
```

---

# 6. Marks API

The Marks API allows authorized trainers to submit or update marks for students enrolled in their courses.

Marks updates should follow the same validation and ownership rules used by the existing Django application.

The existing marks service can be reused by the API layer so that the API does not duplicate the business logic.

## Marks Endpoints

| Method | Endpoint                            | Purpose                | Request Data                                     | Response Data                         | Permissions                                                                       | Status Codes                      |
| ------ | ----------------------------------- | ---------------------- | ------------------------------------------------ | ------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------- |
| POST   | `/api/marks/`                       | Submit or update marks | `student_id`, `course_id`, `new_marks`, `reason` | Updated marks and history information | Trainer only; trainer must be assigned to the course and student must be enrolled | `201`, `400`, `401`, `403`, `404` |
| GET    | `/api/students/{id}/marks-history/` | View marks history     | Optional `page`                                  | List of marks history records         | Admin: all. Trainer: assigned students. Student: own record                       | `200`, `401`, `403`, `404`        |

### Example Marks Request

```json
{
    "student_id": 15,
    "course_id": 3,
    "new_marks": 82,
    "reason": "Updated after final assessment"
}
```

### Example Marks Response

```json
{
    "student_id": 15,
    "course_id": 3,
    "marks": 82,
    "updated_by": 7,
    "reason": "Updated after final assessment"
}
```

### Marks Permission Rules

A trainer can update marks only when:

1. The authenticated user has the `trainer` role.
2. The trainer is assigned to the requested course.
3. The student is enrolled in that course.
4. The marks value passes validation.
5. A reason is supplied when required by the existing marks workflow.

Students cannot directly update their own marks.

---

# 7. Feedback API

The Feedback API provides communication between trainers and students.

Trainers can create feedback for students assigned to their courses. Students can view feedback that has been marked as visible to them.

The API should reuse the existing feedback service so that ownership, validation, and visibility rules remain consistent with the web application.

## Feedback Endpoints

| Method | Endpoint                       | Purpose                       | Request Data                                   | Response Data            | Permissions                                                                 | Status Codes                      |
| ------ | ------------------------------ | ----------------------------- | ---------------------------------------------- | ------------------------ | --------------------------------------------------------------------------- | --------------------------------- |
| GET    | `/api/students/{id}/feedback/` | List feedback for a student   | No request body                                | List of feedback records | Admin: all. Trainer: permitted feedback. Student: visible feedback for self | `200`, `401`, `403`, `404`        |
| POST   | `/api/students/{id}/feedback/` | Create feedback for a student | `course_id`, `rating`, `comment`, `is_visible` | Created feedback record  | Trainer only; trainer must be assigned to the course/student                | `201`, `400`, `401`, `403`, `404` |
| PATCH  | `/api/feedback/{id}/`          | Update existing feedback      | `rating`, `comment`, `is_visible`              | Updated feedback record  | Trainer who created the feedback                                            | `200`, `400`, `401`, `403`, `404` |

### Example Feedback Request

```json
{
    "course_id": 3,
    "rating": 4,
    "comment": "Good progress in the course.",
    "is_visible": true
}
```

### Example Feedback Response

```json
{
    "id": 12,
    "student_id": 15,
    "course_id": 3,
    "trainer_id": 7,
    "rating": 4,
    "comment": "Good progress in the course.",
    "is_visible": true
}
```

### Feedback Permission Rules

A trainer can create feedback only when:

1. The user has the `trainer` role.
2. The trainer is assigned to the course.
3. The student is enrolled in the course.
4. The feedback rating passes validation.
5. The feedback belongs to the authenticated trainer when editing.

Students can only view feedback that is marked as visible.

---

# 8. Permission Summary

The following table summarizes the main permissions across the API.

| Operation          | Admin |                   Trainer |          Student |
| ------------------ | ----: | ------------------------: | ---------------: |
| List students      |   Yes |         Assigned students |       Own record |
| Create student     |   Yes |                        No |               No |
| Update student     |   Yes |                        No |               No |
| Delete student     |   Yes |                        No |               No |
| List courses       |   Yes |                       Yes |              Yes |
| Create course      |   Yes |                        No |               No |
| Update course      |   Yes |                        No |               No |
| Delete course      |   Yes |                        No |               No |
| Manage enrollments |   Yes |                        No |               No |
| Update marks       |    No | Assigned students/courses |               No |
| View marks         |   Yes |         Assigned students |        Own marks |
| Create feedback    |    No | Assigned students/courses |               No |
| Edit feedback      |    No |              Own feedback |               No |
| View feedback      |   Yes |        Permitted feedback | Visible feedback |

---

# 9. Validation and Permission Rules

The API should not create a second set of business rules.

The following existing project logic should be reused:

* `@role_required(...)` for role-based access.
* Marks service functions for trainer/course/student ownership checks.
* Feedback service functions for feedback ownership and validation.
* Existing Django forms/model validation where appropriate.
* Existing course enrollment relationships when checking whether a student belongs to a course.

This keeps the web application and future API consistent.

For example:

```text
Web Request
     │
     ▼
Django View
     │
     ▼
Marks / Feedback Service
     │
     ▼
Database
```

The future API can use the same service layer:

```text
API Request
     │
     ▼
API View / ViewSet
     │
     ▼
Marks / Feedback Service
     │
     ▼
Database
```

Therefore, the business logic does not need to be rewritten for the API.

---

# 10. Status Code Conventions

The API should use standard HTTP status codes consistently.

| Status             | Usage                                                                  |
| ------------------ | ---------------------------------------------------------------------- |
| `200 OK`           | Successful GET or PATCH request                                        |
| `201 Created`      | Successful POST request that creates a resource                        |
| `204 No Content`   | Successful DELETE request                                              |
| `400 Bad Request`  | Invalid input, missing required data, or validation failure            |
| `401 Unauthorized` | Authentication is required or credentials are invalid                  |
| `403 Forbidden`    | User is authenticated but does not have the required role or ownership |
| `404 Not Found`    | Resource does not exist or is not available to the requester           |

---

# 11. Pagination and Filtering

List endpoints should support pagination when the number of records becomes large.

For example:

```text
GET /api/students/?page=1
```

Student listing can also support filters similar to the existing web application:

```text
GET /api/students/?department=2
GET /api/students/?course=3
GET /api/students/?status=active
GET /api/students/?result=pass
GET /api/students/?q=Aditya
```

A paginated response can follow this structure:

```json
{
    "count": 25,
    "next": "/api/students/?page=2",
    "previous": null,
    "results": []
}
```

This keeps the future API conceptually consistent with the pagination and filtering already used by the Django application.

---

# 12. API Design Summary

The planned API exposes five main resources:

1. **Students**
2. **Courses**
3. **Enrollments**
4. **Marks**
5. **Feedback**

Each endpoint defines:

* HTTP method
* URL
* Purpose
* Request data
* Response data
* Permission rules
* Expected status codes

The API is designed around the existing Student Training Portal rather than creating a separate business-logic layer.

The main principle is:

> **The API should be another interface to the existing application logic, not a second implementation of that logic.**

When API implementation is added later, Django REST Framework can be used to expose these resources while continuing to use the existing Django models, role permissions, validation, and service functions.
