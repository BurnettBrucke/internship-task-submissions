# Python and Django Training - Day 4

## Authentication, Authorization and Bootstrap Template Design

This project is a continuation of the Student Training Portal developed during the Python and Django training.

Day 4 focuses on:

- Authentication
- Role-Based Authorization
- Secure Account Management
- Audit Logging
- Feedback Management
- Secure Marks Workflow
- Course Management
- Bootstrap Template Design
- Django ORM Queries
- Testing

---

## 1. Project Overview

The Student Training Portal is a Django-based web application used to manage:

- Students
- Trainers
- Courses
- Student marks
- Trainer feedback
- User accounts
- Audit logs

The application provides separate access and dashboards for Admin, Trainer and Student users.

---

## 2. User Roles

The application supports three roles:

1. Admin
2. Trainer
3. Student

### Role-Permission Matrix

| Feature | Admin | Trainer | Student |
|---|---|---|---|
| Admin Dashboard | Yes | No | No |
| Trainer Dashboard | Yes | Yes | No |
| Student Dashboard | Yes | Yes | Yes |
| Manage Students | Yes | Assigned Students | Own Data |
| Manage Trainers | Yes | No | No |
| Manage Courses | Yes | No | No |
| Assign Trainers to Courses | Yes | No | No |
| View Assigned Students | Yes | Yes | Own Data |
| Update Marks | Yes | Assigned Students | No |
| View Marks History | Yes | Assigned Students | Own Data |
| Add Feedback | Yes | Assigned Students | No |
| Edit Feedback | Yes | Own Feedback | No |
| View Feedback | Yes | Own Feedback | Own Visible Feedback |
| Audit Logs | Yes | No | No |
| Account Management | Yes | Own Account | Own Account |

---

## 3. Authentication

The application provides:

- User registration
- User login
- User logout
- Password change
- Password reset
- Password validation
- Email uniqueness validation
- Failed login handling
- Trainer approval
- Admin account activation/deactivation

### Password Validation

The application validates passwords using rules such as:

- Minimum 8 characters
- Uppercase letter
- Lowercase letter
- Digit
- Special character
- Password confirmation
- Password should not match username/email

---

## 4. Role-Based Authorization

Role-based access control is implemented using a reusable `role_required` decorator.

Unauthorized users are prevented from accessing restricted views.

For example:

- Admin-only pages can only be accessed by Admin users.
- Trainers can access only their assigned students.
- Students can access only their own student data.

Unauthorized access results in HTTP 403 Forbidden.

---

## 5. Dashboard Design

Separate dashboards are available for:

### Admin Dashboard

Admin can manage:

- Students
- Trainers
- Courses
- Users
- Audit logs

### Trainer Dashboard

Trainer can manage:

- Assigned students
- Marks
- Feedback
- Assigned courses

### Student Dashboard

Student can view:

- Own profile
- Own courses
- Own marks
- Marks history
- Visible feedback

Bootstrap cards, tables, badges and responsive layouts are used throughout the dashboards.

---

## 6. Course Management

Admin users can:

- Add courses
- View courses
- Edit courses
- Delete courses
- Assign trainers
- Assign students
- Activate/deactivate courses

The Trainer field in the Course form displays only users whose role is `trainer`.

---

## 7. Audit Logging

Sensitive actions are recorded in the `AuditLog` model.

The audit log stores:

- User
- Action
- Description
- Affected object
- IP address
- Timestamp

The following actions are logged:

- Login
- Logout
- Failed login
- Student creation/update/deletion
- Trainer creation/update/deletion
- Course creation/update/deletion
- Marks updates
- Feedback creation/update
- Account status changes

Audit logs are accessible only to Admin users.

---

## 8. Secure Marks Workflow

Marks are managed using `CourseMark` and `MarksHistory`.

### Marks Rules

- Marks must be between 0 and 100.
- Only authorized users can update marks.
- Trainers can update marks only for assigned students.
- Students cannot directly update marks.
- Every marks update creates a history record.

Marks history stores:

- Student
- Course
- Previous marks
- New marks
- Updated by
- Update date
- Reason for change

---

## 9. Feedback Management

The Feedback system supports:

- Rating from 1 to 5
- Comments
- Trainer ownership
- Student visibility
- Admin access

### Feedback Permissions

- Trainers can add feedback for assigned students.
- Trainers can edit only their own feedback.
- Students can view only visible feedback.
- Admin can view all feedback.

---

## 10. Account Security

Session and cookie security settings are configured for development.

Current settings include:

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_AGE = 3600
CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE are set to False for local HTTP development.

For production deployment using HTTPS, secure cookie settings should be enabled.

---

## 11. Password Reset

Django's built-in password reset functionality is implemented.

Password reset includes:

- Password reset request
- Reset email flow
- Password reset confirmation
- Password reset completion

Password reset templates are included in the project.

---

## 12. Bootstrap Template Design

The project uses reusable Bootstrap-based templates.

Common UI elements include:

- Navbar
- Messages
- Form errors
- Tables
- Cards
- Badges
- Buttons
- Pagination
- Responsive layouts

Templates extend the common base.html template to avoid repeated layout code.

---

## 13. Django ORM

Django ORM queries were practiced during Day 4.

ORM challenges covered:

- Filtering
- Ordering
- Aggregation
- Annotation
- Relationships
- ForeignKey queries
- Many-to-Many queries
- Related object queries

ORM challenge solutions are documented separately in: *orm_queries.md*

---

## 14. Testing

The project includes more than 20 tests covering important application functionality.

Testing includes:

- Authentication
- Login/logout
- Role-based authorization
- Student access control
- Trainer permissions
- Marks update permissions
- Feedback permissions
- Audit logging
- Form validation
- Account management

The test suite was executed successfully during development.

---

## 15. Security Measures

The application includes:

- Django authentication
- Role-based authorization
- Login protection
- CSRF protection
- Password validation
- Session security
- Ownership-based access control
- Permission checks on POST requests
- Audit logging
- Trainer approval
- Account activation/deactivation

Security checks are implemented at the view level and are not dependent only on hiding buttons in templates.

---

## 16. Project Structure

Training_Project/
│
├── manage.py
│
├── training_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── students/
    ├── migrations/
    ├── templates/
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    └── tests.py

## 17. Known Limitations

- Session and CSRF secure-cookie settings are configured for local HTTP development.
- Production deployment requires HTTPS and production security configuration.
- Email delivery for password reset requires proper email backend configuration in production.
- The current application is intended as a training project and may require additional production deployment hardening.

## 18. Day 4 Completion Summary

Day 4 implementation includes:

- Role-based authentication
- Separate dashboards
- Authorization and ownership checks
- Secure account management
- Password reset
- Audit logging
- Feedback workflow
- Secure marks workflow
- Marks history
- Course management
- Bootstrap templates
- Django ORM practice
- Automated testing

## 19. Git Submission

The Day 4 implementation is maintained in the internship Git repository.

Branch: *burnettbrucke-intern-task-deepika*