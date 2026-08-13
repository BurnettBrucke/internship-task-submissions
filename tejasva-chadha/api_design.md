# API Planning Document - Student Training Portal API

This document details the RESTful API architecture and endpoint specifications for the Student Training Portal. It defines resources, endpoints, HTTP methods, request/response models, authorization rules, and status codes in preparation for API integration (e.g., FastAPI / Django REST Framework).

---

## 1. Resources Exposed Through API

The following core domain entities are exposed through the API:
1. **Students** (`/api/students/`): Student profiles, marks, departments, enrolled courses, and active status.
2. **Courses** (`/api/courses/`): Training courses, duration, codes, active status, and assigned trainers.
3. **Enrollments** (`/api/students/{id}/courses/`): Association between students and courses.
4. **Marks** (`/api/marks/`): Marks updates, score tracking, and historical audit logs.
5. **Feedback** (`/api/feedback/`): Performance evaluations and ratings given by trainers to students.
6. **Health & System Status** (`/api/health/`): Operational status and health check.

---

## 2. Service Layer & API Boundary Rationale

### Why extract logic into `services.py` for API preparation?
1. **Framework Agnostic Logic**: Pure Python service functions (`update_student_marks`, `create_feedback`, `filter_students`) operate on data models independent of Django Web HTML rendering (templates, request cookies).
2. **Reusability across HTML Views & API Routers**: Both standard Django template views and FastAPI/DRF API endpoint handlers can invoke identical service methods.
3. **Single Responsibility**: Service handlers manage transaction boundaries (`@transaction.atomic`), audit logging, and domain state validation cleanly away from HTTP transport routing.
4. **Simplified Validation & Testing**: Service boundaries allow unit testing of core business rules without spinning up HTTP test clients or mocking HTTP request contexts.

---

## 3. Endpoints Matrix Overview

| Method | Endpoint Path | Resource / Action | Minimum Allowed Role |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/health` | Application health check | Public / Anonymous |
| **GET** | `/api/students/` | List permitted students (filter/paginate) | Trainer / Admin |
| **POST** | `/api/students/` | Create a new student | Admin |
| **GET** | `/api/students/{id}/` | Retrieve single student details | Owner Student / Trainer / Admin |
| **PATCH** | `/api/students/{id}/` | Partial update student record | Trainer (marks only) / Admin (all) |
| **DELETE** | `/api/students/{id}/` | Delete student record | Admin |
| **GET** | `/api/courses/` | List available courses | Authenticated User |
| **POST** | `/api/courses/` | Create a new course | Admin |
| **POST** | `/api/marks/` | Submit or update student marks | Assigned Trainer / Admin |
| **GET** | `/api/feedback/` | List feedback entries | Owner Student / Trainer / Admin |
| **POST** | `/api/feedback/` | Submit new student feedback | Assigned Trainer |

---

## 4. Detailed Endpoint Specifications

### 4.1 Health Check Endpoint
- **Method:** `GET`
- **Endpoint:** `/api/health/`
- **Purpose:** Monitor application status and system metrics.
- **Permissions:** None (Public)
- **Request Parameters:** None
- **Response Payload (`200 OK`):**
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-08-12T15:15:00Z",
    "database": "connected"
  }
  ```

---

### 4.2 List Students
- **Method:** `GET`
- **Endpoint:** `/api/students/`
- **Purpose:** Retrieve a paginated list of students filtered by department, course, active status, or search query.
- **Permissions:** Admin or Trainer (Trainers only see students enrolled in their assigned courses).
- **Query Parameters:**
  - `q` (string, optional): Search term for student name, email, department name.
  - `department` (integer, optional): Department ID filter.
  - `course` (integer, optional): Course ID filter.
  - `active_status` (string, optional): `'active'` or `'inactive'`.
  - `skip` (integer, default: 0): Offset pagination index.
  - `limit` (integer, default: 10): Items per page limit.
- **Response Payload (`200 OK`):**
  ```json
  {
    "total": 24,
    "skip": 0,
    "limit": 10,
    "results": [
      {
        "id": 1,
        "name": "Rahul Verma",
        "email": "rahul@example.com",
        "age": 22,
        "department": { "id": 1, "name": "Computer Science" },
        "courses": [
          { "id": 101, "course_name": "Python Web Development", "code": "PY-101" }
        ],
        "marks": 88,
        "active_status": true,
        "joined_date": "2026-01-15"
      }
    ]
  }
  ```
- **Expected Status Codes:** `200 OK`, `401 Unauthorized`, `403 Forbidden`.

---

### 4.3 Create Student
- **Method:** `POST`
- **Endpoint:** `/api/students/`
- **Purpose:** Register a new student in the portal.
- **Permissions:** Admin only.
- **Request Body:**
  ```json
  {
    "name": "Ananya Roy",
    "email": "ananya@example.com",
    "age": 23,
    "department_id": 2,
    "course_ids": [101, 102],
    "marks": 75,
    "joined_date": "2026-08-10"
  }
  ```
- **Response Payload (`201 Created`):**
  ```json
  {
    "id": 25,
    "name": "Ananya Roy",
    "email": "ananya@example.com",
    "age": 23,
    "department_id": 2,
    "marks": 75,
    "active_status": true,
    "joined_date": "2026-08-10"
  }
  ```
- **Expected Status Codes:** `201 Created`, `400 Bad Request` (validation failure), `401 Unauthorized`, `403 Forbidden`.

---

### 4.4 Retrieve Student Details
- **Method:** `GET`
- **Endpoint:** `/api/students/{id}/`
- **Purpose:** Fetch single student profile details, marks history, and visible feedback.
- **Permissions:** Admin, Assigned Trainer, or Owner Student.
- **Response Payload (`200 OK`):**
  ```json
  {
    "id": 1,
    "name": "Rahul Verma",
    "email": "rahul@example.com",
    "age": 22,
    "department": "Computer Science",
    "marks": 88,
    "joined_date": "2026-01-15",
    "active_status": true,
    "profile": {
      "phone": "+91-9876543210",
      "address": "Delhi, India",
      "date_of_birth": "2004-05-12"
    }
  }
  ```
- **Expected Status Codes:** `200 OK`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

---

### 4.5 Update Student (Partial Update)
- **Method:** `PATCH`
- **Endpoint:** `/api/students/{id}/`
- **Purpose:** Update fields of a student. Trainers can only update `marks`. Admin can update all attributes.
- **Permissions:** Admin or Assigned Trainer.
- **Request Body (Trainer - Marks Only):**
  ```json
  {
    "marks": 92
  }
  ```
- **Response Payload (`200 OK`):**
  ```json
  {
    "id": 1,
    "name": "Rahul Verma",
    "marks": 92,
    "updated_at": "2026-08-12T15:15:00Z"
  }
  ```
- **Expected Status Codes:** `200 OK`, `400 Bad Request` (invalid marks range 0-100), `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

---

### 4.6 Delete Student
- **Method:** `DELETE`
- **Endpoint:** `/api/students/{id}/`
- **Purpose:** Permanently remove a student record.
- **Permissions:** Admin only.
- **Response Payload (`204 No Content`):** Empty body.
- **Expected Status Codes:** `204 No Content`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

---

### 4.7 List Courses
- **Method:** `GET`
- **Endpoint:** `/api/courses/`
- **Purpose:** List training courses with assigned trainers.
- **Permissions:** Authenticated users.
- **Response Payload (`200 OK`):**
  ```json
  [
    {
      "id": 101,
      "course_name": "Python Web Development",
      "code": "PY-101",
      "duration_weeks": 12,
      "active_status": true,
      "assigned_trainer": { "id": 5, "username": "trainer_alex" }
    }
  ]
  ```
- **Expected Status Codes:** `200 OK`, `401 Unauthorized`.

---

### 4.8 Submit / Update Marks
- **Method:** `POST`
- **Endpoint:** `/api/marks/`
- **Purpose:** Submit marks change with audit trail and historical tracking.
- **Permissions:** Assigned Trainer or Admin.
- **Request Body:**
  ```json
  {
    "student_id": 1,
    "course_id": 101,
    "new_marks": 92,
    "reason": "Mid-term reassessment"
  }
  ```
- **Response Payload (`200 OK`):**
  ```json
  {
    "status": "success",
    "student_id": 1,
    "previous_marks": 88,
    "new_marks": 92,
    "timestamp": "2026-08-12T15:15:00Z"
  }
  ```
- **Expected Status Codes:** `200 OK`, `400 Bad Request`, `403 Forbidden`, `404 Not Found`.

---

### 4.9 Create Feedback
- **Method:** `POST`
- **Endpoint:** `/api/feedback/`
- **Purpose:** Add evaluation feedback for a student in a course.
- **Permissions:** Assigned Trainer.
- **Request Body:**
  ```json
  {
    "student_id": 1,
    "course_id": 101,
    "rating": 5,
    "comments": "Exceptional code quality and team contribution.",
    "is_visible": true
  }
  ```
- **Response Payload (`201 Created`):**
  ```json
  {
    "id": 12,
    "student_id": 1,
    "course_id": 101,
    "trainer_id": 5,
    "rating": 5,
    "comments": "Exceptional code quality and team contribution.",
    "is_visible": true,
    "created_at": "2026-08-12T15:15:00Z"
  }
  ```
- **Expected Status Codes:** `201 Created`, `400 Bad Request` (rating out of range 1-5), `403 Forbidden`.
