<div align="center">

🎓 Training Management Portal

A Role-Based Django Training Management System

Training Management Portal built with Django for managing students, trainers, courses, user accounts, authentication, permissions, performance, and audit activity.

Roles: Administrator · Trainer · Student

</div>

Project Type: Django Web Application
Architecture: Model-Template-View (MVT)
Database: SQLite
UI: Bootstrap
Purpose: Student, Trainer, Course and Account Management

📑 Table of Contents

Project Overview

Key Features

Technology Stack

Application Roles

Role and Permission Matrix

Project Structure

Application Workflow

Authentication and Authorization

Student Management

Course and Trainer Management

Account Management

Audit Logging

Security

Database and ORM

Installation and Setup

Running the Project

Common Django Commands

Development Notes

Future Improvements

Conclusion

📌 Project Overview

The Training Management Portal is designed to manage a training institute's day-to-day operations through a centralized web application.

The system supports:

Role-based authentication

Role-based authorization

Student CRUD operations

Trainer management and approval

Course management

Trainer-course assignment

Student performance and marks

Account activation/deactivation

Password change and password reset

Search and pagination

Audit logs

Separate dashboards for each role

Bootstrap-based responsive UI

The application follows Django's Model-Template-View (MVT) architecture.

🚀 Key Features

1. Role-Based Authentication

The system supports three application roles:

Administrator

Trainer

Student

After login, users are directed to the dashboard associated with their role.

2. Role-Based Authorization

Access to functionality is controlled according to the user's role.

Examples:

Administrators can manage students and trainers.

Trainers can access assigned students and courses.

Students can access their own information and performance.

3. Student Management

Administrators can:

Add students

View students

Search students

View student details

Edit students

Delete students

View marks and pass/fail status

Manage student active status

4. Trainer Management

The system supports:

Trainer registration

Trainer approval by administrator

Trainer activation/deactivation

Trainer-specific dashboard

Assigned course and student visibility

5. Course Management

The application supports:

Course information

Trainer assignment

Student enrollment/association

Course visibility on trainer dashboards

6. Account Management

Users can:

Change password

Request password reset

Reset password using the reset link

View account information

Administrators can:

Activate accounts

Deactivate accounts

7. Student Performance

The portal displays:

Student marks

Pass/fail result

Performance progress

Trainer-managed student performance information

8. Audit Logging

Important actions can be recorded with information such as:

User

Action

Date/time

IP address

This provides traceability for administrative activity.

9. Search and Pagination

The student listing supports:

Search by student name/email

Pagination for student records

10. Reusable Templates

Common UI components are separated into reusable templates:

Navbar

Messages

Pagination

Form errors

🛠️ Technology Stack

Technology

Purpose

Python

Programming language

Django 6.1.1

Web framework

SQLite

Development database

Django ORM

Database interaction

HTML5

Page structure

CSS

Styling

Bootstrap

Responsive UI

JavaScript

Client-side interactions

Git/GitHub

Version control

👥 Application Roles

👨‍💼 Administrator

The Administrator has system-level management responsibilities.

Main responsibilities include:

Managing students

Managing trainers

Approving trainers

Managing courses

Assigning trainers to courses

Activating/deactivating accounts

Viewing system statistics

Viewing audit logs

👨‍🏫 Trainer

The Trainer works with assigned courses and students.

Main responsibilities include:

Viewing assigned courses

Viewing students associated with assigned courses

Updating relevant student performance information

Accessing the trainer dashboard

👨‍🎓 Student

The Student has access to their own information.

Main responsibilities include:

Viewing their dashboard

Viewing their profile information

Viewing marks/performance

Viewing their result

## 🔐 Role and Permission Matrix

The following matrix describes the application's role-based access at a functional level.

| Feature / Action | Administrator | Trainer | Student |
|---|:---:|:---:|:---:|
| Login | ✅ | ✅ | ✅ |
| Logout | ✅ | ✅ | ✅ |
| View own dashboard | ✅ | ✅ | ✅ |
| View account information | ✅ | ✅ | ✅ |
| Change own password | ✅ | ✅ | ✅ |
| Request password reset | ✅ | ✅ | ✅ |
| Reset password | ✅ | ✅ | ✅ |
| View student list | ✅ | ✅ | ❌ |
| Search students | ✅ | ✅ | ❌ |
| Add student | ✅ | ❌ | ❌ |
| View student details | ✅ | ✅ | ❌ |
| Edit student | ✅ | ✅* | ❌ |
| Delete student | ✅ | ❌ | ❌ |
| View student marks | ✅ | ✅ | Own only |
| Update student performance | ✅ | ✅ | ❌ |
| View admin dashboard | ✅ | ❌ | ❌ |
| View trainer dashboard | ❌ | ✅ | ❌ |
| View student dashboard | ❌ | ❌ | ✅ |
| View trainer list | ✅ | ❌ | ❌ |
| Approve trainer | ✅ | ❌ | ❌ |
| Activate user account | ✅ | ❌ | ❌ |
| Deactivate user account | ✅ | ❌ | ❌ |
| Assign trainer to course | ✅ | ❌ | ❌ |
| View assigned courses | All relevant courses | Own assigned courses | Relevant enrollment |
| View assigned students | All relevant students | Own assigned students | ❌ |
| View audit logs | ✅ | ❌ | ❌ |

### 📝 Permission Notes

- `*` Trainer editing is restricted to functionality permitted for trainer-managed student information, such as marks/feedback.
- Students are restricted to their own information where ownership-based access is applied.
- Authentication and authorization are separate: a user must first be authenticated and then authorized.
- Backend authorization is the actual security boundary.


## 📁 Project Structure

A simplified structure of the project is:

```text
training_project/
│
├── manage.py
│
├── training_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── student/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── decorators.py
│   ├── validators.py
│   └── ...
│
├── templates/
│   ├── base.html
│   │
│   ├── includes/
│   │   ├── navbar.html
│   │   ├── messages.html
│   │   ├── pagination.html
│   │   └── form_errors.html
│   │
│   ├── dashboards/
│   │   ├── admin_dashboard.html
│   │   ├── trainer_dashboard.html
│   │   └── student_dashboard.html
│   │
│   ├── registration/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── password_change.html
│   │   ├── password_change_done.html
│   │   ├── password_reset_form.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   └── password_reset_complete.html
│   │
│   ├── students/
│   │   ├── student_list.html
│   │   ├── student_detail.html
│   │   └── student_form.html
│   │
│   └── audit_logs.html
│
└── db.sqlite3
```

The general request-response workflow is:

Browser
   |
   | HTTP Request
   v
urls.py
   |
   v
Authentication / Authorization
   |
   v
views.py
   |
   +------------------+
   |                  |
   v                  v
forms.py           Django ORM
   |                  |
   v                  v
Validation        Database
   |                  |
   +--------+---------+
            |
            v
        Context Data
            |
            v
        Template
            |
            v
        HTTP Response
            |
            v
         Browser

Django middleware works around the request/response cycle and provides functionality such as sessions, authentication, CSRF protection, messages, and security processing.

🔑 Authentication and Authorization

Authentication

Authentication answers:

"Who is the user?"

The project uses Django's authentication system for:

Login

Logout

Password management

User sessions

Authorization

Authorization answers:

"What is the authenticated user allowed to do?"

The project uses user roles and role-based checks to restrict access.

Example:

User logs in
     |
     v
Authentication successful
     |
     v
Read UserProfile role
     |
     +---- admin -----> Admin Dashboard
     |
     +---- trainer ---> Trainer Dashboard
     |
     +---- student ---> Student Dashboard

🎓 Student Management

The student management workflow follows CRUD principles.

Create

Admin
  ↓
Add Student
  ↓
StudentForm
  ↓
Validation
  ↓
Save Student
  ↓
Database

Read

Student List
  ↓
ORM Query
  ↓
Search / Pagination
  ↓
Template

Update

Edit Student
  ↓
Load existing Student
  ↓
StudentForm(instance=student)
  ↓
Validate
  ↓
Save changes

Delete

Admin
  ↓
Delete
  ↓
POST request + CSRF
  ↓
Delete Student
  ↓
Redirect

📚 Course and Trainer Management

👨‍🏫 Trainer Approval

Trainer Registration
        ↓
Pending Trainer
        ↓
Administrator
        ↓
Approve Trainer
        ↓
Trainer becomes approved

Course-Trainer Assignment

Administrator
      ↓
Select Course
      ↓
Select Trainer
      ↓
Assign Trainer
      ↓
Course updated
      ↓
Trainer Dashboard

👨‍🏫 Trainer Course Workflow

Trainer Login
      ↓
Trainer Dashboard
      ↓
Assigned Courses
      ↓
Students associated with courses
      ↓
Student performance information

👤 Account Management

Change Password

Authenticated User
      ↓
Change Password
      ↓
Validate current/new password
      ↓
Update password
      ↓
Success page

Password Reset

Forgot Password
      ↓
Enter email
      ↓
Django password-reset flow
      ↓
Reset link
      ↓
Token validation
      ↓
New password

Account Activation

Administrator
      ↓
Select account
      ↓
Activate
      ↓
User.is_active = True

Account Deactivation

Administrator
      ↓
Select account
      ↓
Deactivate
      ↓
User.is_active = False

📝 Audit Logging

Audit logging provides a record of important system actions.

Conceptually:

User Action
    ↓
View processes action
    ↓
Action succeeds
    ↓
Audit record created
    ↓
Database

An audit record can contain:

User
Action
Created At
IP Address

Administrators can access the audit log interface.

🛡️ Security

The project uses Django's built-in security mechanisms and application-level authorization.

Authentication

Django authentication is used to identify users.

Password Hashing

Passwords are handled through Django's password system rather than storing plain-text passwords.

Password Validation

The project uses Django's built-in password validators along with a custom strong-password validator.

CSRF Protection

POST forms use Django CSRF protection.

Example:

{% csrf_token %}

Session Management

Django sessions maintain authenticated user state.

🔹 Role-Based Authorization

Backend checks prevent unauthorized roles from accessing protected views.

Ownership-Based Access

Where applicable, users are restricted to resources belonging to them.

Account Activation

The is_active status can be used to prevent inactive accounts from normal authentication.

🗄️ Database and ORM

The project uses Django ORM to communicate with the database.

Instead of directly writing SQL for normal application operations, Django QuerySets are used.

Examples:

Student.objects.all()

Student.objects.filter(active=True)

Student.objects.count()

The general flow is:

Python Code
    ↓
Django ORM
    ↓
SQL Query
    ↓
SQLite Database

Model Relationships

The project uses different Django relationship types.

One-to-One

Used for the relationship between a Django user and its profile.

User
  |
  | OneToOne
  v
UserProfile

ForeignKey

Used where multiple records can reference a single related record, such as students belonging to a department.

Department
    |
    +---- Student
    +---- Student
    +---- Student

Many-to-Many

Used for course/student associations.

Course  <------>  Student

A course can have multiple students and a student can be associated with multiple courses.

🎨 Templates and UI

The project uses template inheritance to avoid repeated HTML.

The common layout is:

base.html
   |
   +-- navbar.html
   +-- messages.html
   |
   +-- Page-specific content

Pages extend the base template and provide their own content.

Reusable components include:

navbar.html

messages.html

pagination.html

form_errors.html

Bootstrap is used for responsive layouts, forms, tables, alerts, cards, badges, navigation, and modals.

⚙️ Installation and Setup

1. Clone the project

git clone <repository-url>
cd training_project

2. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

3. Install dependencies

If a requirements.txt file is available:

pip install -r requirements.txt

Otherwise install Django:

pip install django

4. Apply migrations

python manage.py makemigrations
python manage.py migrate

5. Create an admin/superuser if required

python manage.py createsuperuser

6. Run the development server

python manage.py runserver

Open:

http://127.0.0.1:8000/

▶️ Running the Project

Start the development server:

python manage.py runserver

Useful pages include:

/login/
/register/

/dashboard/admin/
/dashboard/trainer/
/dashboard/student/

/students/
/students/add/

/courses/<id>/assign-trainer/

/account-information/

/password-change/
/password-reset/

/admin/audit-logs/
/admin/trainers/

💻 Common Django Commands

Start server

python manage.py runserver

Check project configuration

python manage.py check

Create migrations

python manage.py makemigrations

Apply migrations

python manage.py migrate

Create superuser

python manage.py createsuperuser

Open Django shell

python manage.py shell

🧪 Development Notes

For development, the project uses SQLite and Django's console email backend.

The console email backend is useful for testing password-reset emails locally because the email content is displayed in the terminal instead of being sent through a production email provider.

For production deployment:

Move the secret key to environment variables.

Set DEBUG = False.

Configure ALLOWED_HOSTS.

Use a production-ready database where appropriate.

Configure a real email backend.

Configure secure cookies and HTTPS.

Review static/media file deployment.

Review all authorization rules and production security settings.

🔮 Future Improvements

Possible future enhancements include:

REST API using Django REST Framework

Automated unit and integration tests

Advanced reporting and analytics

Trainer/student notification system

Email notifications for trainer approval

Advanced filtering and sorting

Production database such as PostgreSQL

Docker deployment

CI/CD pipeline

More granular Django permissions

Attendance management

Course completion tracking

✅ Conclusion

The Training Management Portal demonstrates a complete Django web application with:

Authentication

Authorization

Role-based dashboards

CRUD operations

Django ORM

Model relationships

Forms and validation

Course and trainer management

Student performance management

Account management

Password management

Audit logging

Search and pagination

Reusable templates

Security controls

The main architectural flow is:

User
 ↓
Authentication
 ↓
Authorization
 ↓
URL
 ↓
View
 ↓
Form / ORM
 ↓
Database
 ↓
Template
 ↓
Response

This structure keeps the application organized and makes individual features easier to maintain and extend.




