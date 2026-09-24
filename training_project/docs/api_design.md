# API Design Plan

## 1. Resources

The API will expose these resources from the Django Student Management System:

- Students
- Courses
- Enrollments
- Marks
- Feedback

The API will reuse the project's existing role-based permissions:
- Admin: administrative access
- Approved Trainer: access to assigned courses/students and their marks/feedback
- Student: access to their own permitted data and visible feedback
- Unauthenticated users: no access to protected resources

## 2. Endpoint Plan

### Students

| Method | Endpoint | Purpose | Request Data | Response Data | Permissions | Expected Status Codes |
|---|---|---|---|---|---|---|
| GET | `/api/students/` | List permitted students | Optional `search`, `department`, `course`, `status`, `result` | Student id, name, email, age, department, active status, course count | Admin: all; Trainer: permitted students; Student: own record | 200, 401, 403 |
| POST | `/api/students/` | Create a student | `name`, `email`, `age`, `active`, `department`, `courses` | Created student details and enrollments | Admin only | 201, 400, 401, 403 |
| GET | `/api/students/{id}/` | Retrieve one permitted student | Student ID | Student details, department and permitted enrollments | Admin: any; Trainer: assigned student; Student: own record | 200, 401, 403, 404 |
| PATCH | `/api/students/{id}/` | Update selected fields | Allowed student fields and optional courses | Updated student data | Admin only | 200, 400, 401, 403, 404 |
| DELETE | `/api/students/{id}/` | Delete a student | Student ID | Deletion confirmation or empty response | Admin only | 204, 401, 403, 404 |

### Courses

| Method | Endpoint | Purpose | Request Data | Response Data | Permissions | Expected Status Codes |
|---|---|---|---|---|---|---|
| GET | `/api/courses/` | List courses | Optional active-status/filter parameters | Course id, name, code, duration, duration_days, active status | Authenticated users according to access rules | 200, 401 |
| POST | `/api/courses/` | Create a course | `course_name`, `code`, `duration`, `duration_days`, `active_status` | Created course | Admin only | 201, 400, 401, 403 |
| GET | `/api/courses/{id}/` | Retrieve one course | Course ID | Course details and relevant assignments/enrollments | Authenticated user with permission | 200, 401, 403, 404 |
| PATCH | `/api/courses/{id}/` | Update selected course fields | Allowed course fields | Updated course | Admin only | 200, 400, 401, 403, 404 |
| DELETE | `/api/courses/{id}/` | Delete a course when permitted | Course ID | Deletion confirmation or empty response | Admin only, subject to related records | 204, 401, 403, 404, 409 |

### Enrollments

| Method | Endpoint | Purpose | Request Data | Response Data | Permissions | Expected Status Codes |
|---|---|---|---|---|---|---|
| GET | `/api/enrollments/` | List permitted enrollments | Optional `student`, `course` filters | Enrollment id, student, course, enrolled date, marks, progress | Admin: all; Trainer: assigned courses; Student: own enrollments | 200, 401, 403 |
| POST | `/api/enrollments/` | Enroll a student in a course | `student_id`, `course_id` | Created enrollment | Admin only | 201, 400, 401, 403, 409 |
| GET | `/api/enrollments/{id}/` | Retrieve one enrollment | Enrollment ID | Enrollment details, marks and progress | Admin; assigned Trainer; owning Student | 200, 401, 403, 404 |
| PATCH | `/api/enrollments/{id}/` | Update permitted enrollment fields | Allowed enrollment fields | Updated enrollment | Admin only; marks use the marks endpoint | 200, 400, 401, 403, 404 |
| DELETE | `/api/enrollments/{id}/` | Remove an enrollment | Enrollment ID | Deletion confirmation or empty response | Admin only | 204, 401, 403, 404 |

### Marks

| Method | Endpoint | Purpose | Request Data | Response Data | Permissions | Expected Status Codes |
|---|---|---|---|---|---|---|
| GET | `/api/marks/` | List permitted marks | Optional `student`, `course`, `enrollment` filters | Enrollment id, student, course, marks | Admin: all; Trainer: assigned courses; Student: own marks | 200, 401, 403 |
| POST | `/api/marks/` | Submit or update marks | `enrollment_id`, `marks`, `reason` | Enrollment, previous marks, new marks, updater, reason | Approved Trainer assigned to course | 201, 400, 401, 403, 404 |
| GET | `/api/marks/{id}/` | Retrieve mark information | Mark/enrollment ID | Current marks and relevant history | Admin; assigned Trainer; owning Student | 200, 401, 403, 404 |
| PATCH | `/api/marks/{id}/` | Update existing marks | `marks`, `reason` | Updated marks and history information | Approved Trainer assigned to course | 200, 400, 401, 403, 404 |

Mark updates should preserve the existing `MarkHistory` behavior: previous marks, new marks, trainer and reason should be recorded.

### Feedback

| Method | Endpoint | Purpose | Request Data | Response Data | Permissions | Expected Status Codes |
|---|---|---|---|---|---|---|
| GET | `/api/feedback/` | List permitted feedback | Optional `student`, `course`, `trainer`, `visible` filters | Feedback id, student, course, trainer, rating, comment, visibility, created date | Admin: all; Trainer: permitted feedback; Student: visible feedback for self | 200, 401, 403 |
| POST | `/api/feedback/` | Create trainer feedback | `enrollment_id`, `rating`, `comment` | Created feedback with student, course, trainer, rating and comment | Approved Trainer assigned to enrollment course | 201, 400, 401, 403, 404 |
| GET | `/api/feedback/{id}/` | Retrieve one feedback record | Feedback ID | Feedback details | Admin; owning Trainer; permitted Student | 200, 401, 403, 404 |
| PATCH | `/api/feedback/{id}/` | Update feedback | `rating`, `comment`, and other allowed fields | Updated feedback | Trainer who created it; Admin according to API policy | 200, 400, 401, 403, 404 |

## 3. Common HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource successfully created |
| 204 | Resource successfully deleted with no response body |
| 400 | Invalid request or validation error |
| 401 | Authentication required |
| 403 | Authenticated user is not permitted |
| 404 | Resource does not exist or is not accessible |
| 409 | Conflict, such as duplicate student-course enrollment |

## 4. Example Response Formats

Successful list:

```json
{
  "results": [],
  "count": 0
}
```

Successful resource:

```json
{
  "id": 1,
  "name": "Student Name"
}
```

Validation error:

```json
{
  "errors": {
    "email": ["A student with this email already exists."]
  }
}
```

Permission error:

```json
{
  "detail": "You are not authorized to perform this action."
}
```

## 5. Service-Layer Reuse

The extracted service modules are intended to contain business logic rather than HTTP rendering:

- `student_service.py`
- `marks_service.py`
- `feedback_service.py`
- `dashboard_service.py`
- `permission_service.py`

Future API views should handle the HTTP request/response flow and call these services instead of duplicating business logic.

For example, the marks API should call the same marks service used by the existing Django view. This means validation, trainer-course checks, mark updates and `MarkHistory` creation can remain in one place.

This makes the extracted code easier to reuse in an API because service functions do not need to know whether the caller is an HTML view or an API endpoint. A future API can call the service and serialize its result into JSON.

## 6. Permission Helpers

Reusable permission helpers should cover:

- Admin-only actions
- Approved trainer checks
- Trainer-to-course assignment checks
- Student ownership checks
- Enrollment access checks
- Marks update permission
- Feedback ownership/edit permission

This prevents the same authorization rules from being copied into every API endpoint.

## 7. Planned API Flow

```text
HTTP Request
     |
     v
API View
     |
     v
Validation / Serializer
     |
     v
Permission Helper
     |
     v
Service Layer
     |
     v
Django Models / Database
     |
     v
Serialized API Response
```

The first API scope is therefore **students, courses, enrollments, marks and feedback**, while keeping business logic and permission rules reusable through the service layer.
