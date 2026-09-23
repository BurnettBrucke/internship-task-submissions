# API Design

## 1. Purpose

This document defines the planned API structure for the Student Training Management System.

The APIs will be implemented later using FastAPI. The API layer will reuse the existing service and business logic wherever possible.

---

## 2. Resources

The main resources planned for the API are:

- Students
- Courses
- Enrollments
- Marks
- Feedback

---

## 3. Students API

### GET `/api/students/`

**Purpose:** Retrieve a list of students.

**Method:** GET

**Request Data:** None

**Response Data:**

{
  "results": [
    {
      "id": 1,
      "name": "Student Name",
      "email": "student@example.com",
      "age": 22,
      "active": true
    }
  ]
}

**Permissions:**

- Admin: All students
- Trainer: Assigned students
- Student: Own student record

**Status Codes:**

- 200 OK
- 401 Unauthorized
- 403 Forbidden

### POST `/api/students/`

**Purpose:** Create a new student.

**Method:** POST

**Request Data:**

{
  "name": "Student Name",
  "email": "student@example.com",
  "age": 22,
  "marks": 75,
  "department_id": 1
}

**Response Data:**

{
  "id": 1,
  "name": "Student Name",
  "email": "student@example.com",
  "age": 22,
  "marks": 75,
  "active": true
}

**Permissions:**Admin only

**Status Codes:**

- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

### GET `/api/students/{id}/`

**Purpose:** Retrieve details of a specific student.

**Method:** GET

**Request Data:** Student ID in URL.

**Response Data:**

{
  "id": 1,
  "name": "Student Name",
  "email": "student@example.com",
  "age": 22,
  "marks": 75,
  "department": "Python",
  "active": true
}

**Permissions:**

- Admin
- Assigned Trainer
- The student themselves

**Status Codes:**

- 200 OK
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

### PATCH `/api/students/{id}/`

**Purpose:** Partially update student information.

**Method:** PATCH

**Request Data:**

{
  "name": "Updated Name",
  "age": 23
}

**Response Data:** Updated student object.

**Permissions:** Admin

**Student:** Own permitted fields

**Status Codes:**

- 200 OK
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

### DELETE `/api/students/{id}/`

**Purpose:** Delete a student.

**Method:** DELETE

**Request Data:** Student ID in URL.

**Response Data:** No response body required.

**Permissions:** Admin only

**Status Codes:**

- 204 No Content
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

## 4. Courses API

### GET `/api/courses/`

**Purpose:** Retrieve available courses.

**Method:** GET

**Request Data:** None

**Response Data:**

{
  "results": [
    {
      "id": 1,
      "course_name": "Python",
      "code": "PY101",
      "duration": "3 Months",
      "active": true
    }
  ]
}

**Permissions:** Authenticated users

**Status Codes:**

- 200 OK
- 401 Unauthorized

### POST `/api/courses/`

**Purpose:** Create a new course.

**Method:** POST

**Request Data:**

{
  "course_name": "Django",
  "code": "DJ101",
  "duration": "3 Months",
  "active": true,
  "trainer_id": 2
}

**Response Data:** Created course object.

**Permissions:** Admin only

**Status Codes:**

- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

### GET `/api/courses/{id}/`

**Purpose:** Retrieve details of a specific course.

**Method:** GET

**Permissions:** Authenticated users

**Status Codes:**

- 200 OK
- 401 Unauthorized
- 404 Not Found

## 5. Enrollment API

### GET `/api/enrollments/`

**Purpose:** Retrieve student-course enrollment information.

**Method:** GET

**Response Data:**

{
  "results": [
    {
      "student_id": 1,
      "course_id": 2,
      "course_name": "Django"
    }
  ]
}

**Permissions:**

- Admin: All enrollments
- Trainer: Enrollments for assigned courses/students
- Student: Own enrollments

**Status Codes:**

- 200 OK
- 401 Unauthorized
- 403 Forbidden

### POST `/api/enrollments/`

**Purpose:** Enroll a student in a course.

**Method:** POST

**Request Data:**

{
  "student_id": 1,
  "course_id": 2
}

**Response Data:** Created enrollment information.

**Permissions:** Admin only

**Status Codes:**

- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

## 6. Marks API

### GET `/api/marks/`

**Purpose:** Retrieve marks records.

**Method:** GET

**Response Data:**

{
  "results": [
    {
      "student_id": 1,
      "course_id": 2,
      "marks": 85,
      "updated_by": 3
    }
  ]
}

**Permissions:**

- Admin: All marks
- Trainer: Marks for assigned courses/students
- Student: Own marks

**Status Codes:**

- 200 OK
- 401 Unauthorized
- 403 Forbidden

### POST `/api/marks/`

**Purpose:** Create or update marks for a student.

**Method:** POST

**Request Data:**

{
  "student_id": 1,
  "course_id": 2,
  "marks": 85,
  "reason": "Monthly assessment"
}

**Response Data:**

{
  "student_id": 1,
  "course_id": 2,
  "marks": 85,
  "message": "Marks updated successfully"
}

**Permissions:**

- Admin
- Trainer assigned to the course

**Status Codes:**

- 200 OK
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

**Service Layer:**

The existing update_student_marks() service should be reused by the API instead of duplicating the marks update and history logic inside the API endpoint.

## 7. Feedback API

### GET `/api/feedback/`

**Purpose:** Retrieve feedback records.

**Method:** GET

**Response Data:**

{
  "results": [
    {
      "id": 1,
      "student_id": 1,
      "trainer_id": 2,
      "course_id": 3,
      "rating": 5,
      "comment": "Good progress",
      "is_visible": true
    }
  ]
}

**Permissions:**

- Admin: All feedback
- Trainer: Feedback related to assigned students/courses
- Student: Visible feedback belonging to them

**Status Codes:**

- 200 OK
- 401 Unauthorized
- 403 Forbidden

### POST `/api/feedback/`

**Purpose:** Create feedback for a student.

**Method:** POST

**Request Data:**

{
  "student_id": 1,
  "course_id": 2,
  "rating": 5,
  "comment": "Good progress"
}

**Response Data:** Created feedback object.

**Permissions:** Trainer assigned to the relevant course

**Status Codes:**

- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

## 8. Common API Error Response

Validation or permission errors should return a consistent structure:
{
  "detail": "Error description"
}

For validation errors, field-specific information may be returned:
{
  "errors": {
    "email": [
      "Enter a valid email address."
    ]
  }
}

## 9. Authentication

The future API should use authenticated requests.

Authentication and authorization should be applied before accessing protected resources.

**Role-based permissions should remain consistent with the existing application:**

- Admin
- Trainer
- Student

## 10. API and Service-Layer Reuse

**The API layer should focus on:**

- Request parsing
- Authentication
- Authorization
- Input validation
- Response formatting
- HTTP status codes

Business logic should remain in reusable service functions.

**For example:**

FastAPI Endpoint
       ↓
Authentication
       ↓
Permission Check
       ↓
Service Layer
       ↓
Django ORM / Database
       ↓
API Response

The marks service created in students/services.py is an example of this separation.

This approach avoids duplicating business logic when the same functionality is accessed through both web views and APIs.