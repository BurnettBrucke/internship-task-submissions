# Student Training Portal API Design

## 1. Purpose

This document defines the planned REST API for the Student Training Portal.

The API will expose reusable resources for:

- Students
- Courses
- Enrollments
- Marks
- Feedback

The API should reuse the existing Django business rules, validation, role-based permissions, ownership restrictions, and service-layer logic.

---

## 2. Authentication and Permissions

The API will require authentication for protected resources.

### Roles

- **Administrator** — Full management access.
- **Trainer** — Access to assigned students and courses, including marks and feedback operations.
- **Student** — Access only to their own permitted information.

Ownership and assignment restrictions must be enforced at the API level as well as the Django view level.

Direct URL manipulation must not allow a user to access another user's restricted resources.

---

# 3. Students API

## GET /api/students/

### Purpose

List students that the authenticated user is permitted to view.

### Request Data

Query parameters may include:

- `search`
- `department`
- `course`
- `active`
- `result`
- `page`

### Response Data

```json
{
    "results": [
        {
            "id": 1,
            "name": "Student Name",
            "email": "student@example.com",
            "age": 21,
            "department": "Computer Science",
            "marks": 85,
            "is_active": true
        }
    ]
}