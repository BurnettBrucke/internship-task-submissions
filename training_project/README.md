# Student Training Portal

## About Project

Student Training Portal ek Django based web application hai.

Is project ka use students, trainers aur admin ko manage karne ke liye kiya gaya hai.

The application provides role-based access, student management, enrollment,
feedback, marks management, audit logging and authentication features.

---

## Technologies Used

- Python
- Django 5.1.4
- SQLite
- HTML
- Bootstrap
- Django Templates

---

## User Roles

The application supports three roles:

### Admin

Admin can:

- Manage students
- Add students
- Edit students
- Delete students
- View audit logs
- Access admin dashboard

### Trainer

Trainer can:

- View assigned students
- Give feedback
- View feedback
- Update student marks
- View marks history
- Access trainer dashboard

### Student

Student can:

- Access student dashboard
- View permitted information
- View feedback
- Access their own student information

---

## Main Features

### 1. Authentication

Users can:

- Register
- Login
- Logout
- Change password
- Reset password

Authentication is handled using Django authentication.

---

### 2. Student Management

Authorized users can:

- View students
- Add students
- Edit students
- Delete students
- View student details

Student information includes:

- Name
- Email
- Age
- Department
- Assigned Trainer
- Joined Date
- Active Status

---

### 3. Enrollment

Students can be associated with courses through enrollments.

Enrollment contains:

- Student
- Course
- Enrollment Date
- Status
- Marks

Enrollment status supports:

- Enrolled
- Completed
- Dropped

A student cannot have duplicate enrollment for the same course.

---

### 4. Search and Filtering

Student records support searching and filtering.

Search can be performed using available student information.

Filters are preserved while navigating through pagination.

---

### 5. Pagination

Student records are displayed using pagination.

Search and filter parameters are preserved when moving between pages.

---

### 6. Feedback

Trainers can provide feedback for their assigned students.

Feedback includes:

- Enrollment
- Rating
- Comments
- Visibility to student
- Created date
- Updated date

Rating validation allows values from 1 to 5.

---

### 7. Marks Management

Student marks can be updated by authorized users.

Marks support values between:

- 0
- 100

The application also maintains marks history containing:

- Previous marks
- New marks
- Updated by
- Reason
- Updated date

---

### 8. Audit Logs

Important application activities are recorded using audit logs.

Supported actions include:

- LOGIN
- LOGOUT
- FAILED_LOGIN
- CREATE
- UPDATE
- DELETE
- MARKS_UPDATE
- FEEDBACK

Audit logs store:

- User
- Action
- Description
- IP address
- Timestamp

---

### 9. Role Based Access Control

Access is restricted according to the user's role.

The application prevents users from accessing functionality that is not
allowed for their role.

Ownership restrictions are also applied where required.

---

## Form Validation

Forms contain server-side validation.

Examples include:

- Empty name validation
- Age validation
- Email validation
- Password strength validation
- Duplicate email validation
- Marks validation
- Rating validation
- Empty feedback validation

Password validation includes:

- Minimum 8 characters
- Uppercase character
- Lowercase character
- Digit
- Special character
- Username restriction
- Email restriction

---

## Security

The project includes:

- Django authentication
- CSRF protection
- Role-based authorization
- Ownership restrictions
- Password validation
- Custom 403 page
- Custom 404 page
- Custom 500 page
- Secure session cookies in production
- Secure CSRF cookies in production
- HSTS configuration in production
- X-Frame-Options protection
- Content type protection
- Environment-based secret key
- Environment-based DEBUG setting
- Environment-based allowed hosts

Production security settings are enabled when:

```text
DJANGO_DEBUG=False