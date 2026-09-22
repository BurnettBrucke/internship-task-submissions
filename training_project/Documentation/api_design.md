# API Design

## 1. Overview

The Student Training Portal API will provide REST endpoints for:

- Students
- Courses
- Enrollments
- Marks
- Feedback

The API will be designed for future frontend, mobile, and third-party integration.

---

## 2. Authentication and Permissions

Authentication will use token-based authentication such as JWT.

### Roles

- **Admin:** Manage students, courses, and enrollments.
- **Trainer:** View assigned students and courses, update marks, and manage feedback.
- **Student:** View own profile, courses, marks, and visible feedback.

Unauthenticated requests return `401 Unauthorized`.

Unauthorized actions return `403 Forbidden`.

---

## 3. Students API

| Method | Endpoint | Permission | Purpose |
|---|---|---|---|
| GET | `/api/students/` | Authenticated | List students |
| GET | `/api/students/{id}/` | Authenticated | View student |
| POST | `/api/students/` | Admin | Create student |
| PUT | `/api/students/{id}/` | Admin | Update student |
| DELETE | `/api/students/{id}/` | Admin | Delete student |

### Example Request

```json
{
    "name": "Ravi Kumar",
    "email": "ravi@example.com",
    "age": 22,
    "department": 1,
    "marks": 75
}
Example Response
{
    "id": 1,
    "name": "Ravi Kumar",
    "email": "ravi@example.com",
    "marks": 75
}

### 4. Courses API

Method	Endpoint	Permission	Purpose
GET	/api/courses/	Authenticated	List courses
GET	/api/courses/{id}/	Authenticated	View course
POST	/api/courses/	Admin	Create course
PUT	/api/courses/{id}/	Admin	Update course
DELETE	/api/courses/{id}/	Admin	Delete course
Example Request
{
    "course_name": "Python",
    "code": "PY101",
    "duration": "3 Months",
    "active_status": true
}
### 5. Enrollments API

Method	Endpoint	Permission	Purpose
GET	/api/enrollments/	Authenticated	View enrollments
POST	/api/enrollments/	Admin	Enroll student
DELETE	/api/enrollments/	Admin	Remove enrollment
Example Request
{
    "student_id": 1,
    "course_id": 2
}

### 6. Marks API

Method	Endpoint	Permission	Purpose
GET	/api/students/{id}/marks/	Admin/Trainer/Student	View marks
PUT	/api/students/{id}/marks/	Assigned Trainer	Update marks
Example Request
{
    "marks": 75,
    "reason": "Monthly assessment"
}
Example Response
{
    "message": "Marks updated successfully.",
    "previous_marks": 70,
    "new_marks": 75
}

The API will reuse the existing update_student_marks() service.

### 7. Feedback API

Method	Endpoint	Permission	Purpose
GET	/api/students/{id}/feedback/	Admin/Trainer/Student	View feedback
POST	/api/students/{id}/feedback/	Assigned Trainer	Add feedback
PUT	/api/feedback/{id}/	Feedback owner	Update feedback
Example Request
{
    "course": 1,
    "feedback": "Good progress",
    "rating": 4,
    "is_visible": true
}
Example Response
{
    "message": "Feedback added successfully.",
    "feedback_id": 1
}

The API will reuse the existing create_student_feedback() service.

### 8. HTTP Status Codes
Status	Meaning
200	Successful request
201	Resource created
204	Successful deletion
400	Invalid request
401	Authentication required
403	Permission denied
404	Resource not found
409	Conflict
500	Server error

### 9. Service Layer Reuse

The API should reuse existing service-layer functions instead of duplicating business logic.

Current reusable services:

get_dashboard_data()
get_filtered_students()
update_student_marks()
create_student_feedback()
trainer_can_access_student()
Benefits
Avoids duplicate logic.
Keeps API views simple.
Maintains consistent web and API behavior.
Makes testing easier.
Improves maintainability.

### 10. API Implementation Plan

The API endpoints are currently planned and documented.

Implementation can be done later using Django REST Framework.

The existing service layer will be reused when implementing the API.