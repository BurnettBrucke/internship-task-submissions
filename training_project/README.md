# Training Project – Django Student Training Portal

A Django-based **Student Training Portal** developed as part of Python and Django Training.

The project demonstrates practical Django concepts including:

* Django project and application structure
* Models and model relationships
* Database migrations
* Django ORM
* CRUD operations
* ModelForms
* Form validation
* Django Admin
* Authentication
* Protected views
* Django messages
* Templates and template inheritance
* Dashboard statistics
* Filtering and searching
* `select_related()` and `prefetch_related()`
* Automated testing
* Service-layer separation
* Git version control

---

# Project Structure

```text
training_project/
│
├── db.sqlite3
├── manage.py
├── README.md
│
├── students/
│   ├── admin.py
│   ├── apps.py
│   ├── form.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── __init__.py
│   │
│   └── migrations/
│       ├── 0001_initial.py
│       ├── 0002_course_department_remove_student_course_and_more.py
│       └── __init__.py
│
├── templates/
│   ├── about.html
│   ├── add_student.html
│   ├── base.html
│   ├── dashboard.html
│   ├── edit_student.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── student_confirm_delete.html
│   ├── student_detail.html
│   └── student_list.html
│
└── training_project/
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── __init__.py
```

> `__pycache__` directories are generated automatically by Python and are not part of the application source code.

---

# Requirements

The project requires:

* Python 3.x
* Django
* VS Code
* Git
* SQLite

---

# Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd training_project
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

Activate the virtual environment:

```bash
venv\Scripts\activate
```

---

## 3. Install Django

```bash
pip install django
```

Verify the Django installation:

```bash
python -m django --version
```

---

# Django Project

### Project Name

```text
training_project
```

### Application Name

```text
students
```

The `students` application contains the project's models, forms, views, URLs, services, tests, migrations, and admin configuration.

The project-level `templates` directory contains the HTML templates used by the application.

---

# Database and Migrations

The project uses Django's default SQLite database:

```text
db.sqlite3
```

After making changes to models, create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

To check migration status:

```bash
python manage.py showmigrations
```

The project currently contains migrations for the initial database structure and subsequent model relationship changes.

---

# Models and Relationships

The Student Training Portal uses multiple related models.

## Department

A department can contain multiple students.

Relationship:

```text
Department
    │
    └── Many Students
```

Implemented using:

```python
ForeignKey
```

---

## Student

The Student model stores the main information about each student.

Important student information includes:

* Name
* Email
* Age
* Marks
* Joined date
* Active status
* Department
* Courses

Students are connected to departments using a `ForeignKey`.

Students are connected to courses using a `ManyToManyField`.

---

## StudentProfile

A StudentProfile contains additional information about a student, such as:

* Phone
* Address
* Date of birth

Relationship:

```text
Student
   │
   └── One StudentProfile
```

This relationship is implemented using:

```python
OneToOneField
```

---

## Course

The Course model stores course information including:

* Course name
* Course code
* Duration
* Active status

A student can be enrolled in multiple courses, and a course can contain multiple students.

Relationship:

```text
Student  ←→  Course
```

This is implemented using:

```python
ManyToManyField
```

---

# Relationship Overview

```text
Department
    │
    │ One-to-Many
    ▼
Student
    │
    ├──────────────► StudentProfile
    │                  One-to-One
    │
    │
    └──────────────► Course
                       Many-to-Many
```

Meaning:

* One Department → Many Students
* One Student → One StudentProfile
* One Student → Many Courses
* One Course → Many Students

Meaningful `related_name` values are used to make reverse relationships easier to query.

---

# Django Admin

The application registers its models with Django Admin.

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
/admin/
```

The admin panel can be used to manage:

* Students
* Departments
* Courses
* Student profiles
* User accounts

---

# Student CRUD Operations

The application supports complete CRUD operations for students.

CRUD means:

```text
Create
Read
Update
Delete
```

## Student List

Displays all students.

URL:

```text
/students/
```

The list includes information such as:

* Student name
* Email
* Department
* Marks
* Active status
* Pass/Fail status
* Course information
* Available actions

---

## Student Details

Displays information about one specific student.

URL:

```text
/students/<id>/
```

The individual student is retrieved using:

```python
get_object_or_404()
```

This prevents the application from returning an unhandled error when the requested student does not exist.

---

## Add Student

URL:

```text
/students/add/
```

A Django `ModelForm` is used to create a new student.

After successful submission, the user is redirected to the student list.

---

## Edit Student

URL:

```text
/students/<id>/edit/
```

The existing student is loaded and displayed using a `ModelForm`.

After successfully updating the student, the user is redirected back to the student list.

---

## Delete Student

URL:

```text
/students/<id>/delete/
```

The application does not immediately delete the student.

Instead, a confirmation page is displayed first:

```text
student_confirm_delete.html
```

The user can then confirm or cancel the deletion.

---

# Student Form Validation

The Student form validates user input before saving data.

Important validation rules include:

| Field  | Validation                |
| ------ | ------------------------- |
| Name   | Cannot be empty           |
| Email  | Must be a valid email     |
| Age    | Must be between 16 and 60 |
| Marks  | Must be between 0 and 100 |
| Course | Cannot be empty           |

Invalid submissions display validation errors on the form.

The form uses Django's validation system through:

```python
form.is_valid()
```

Successful forms can then be saved using:

```python
form.save()
```

---

# Pass / Fail Logic

Student results are determined using the following rule:

```text
Marks >= 40 → Pass
Marks < 40  → Fail
```

Boundary values are especially important:

```text
0   → Fail
40  → Pass
100 → Pass
```

---

# Dashboard

The project includes a Student Training Portal dashboard.

URL:

```text
/dashboard/
```

The dashboard provides an overview of the student database.

It includes:

* Total students
* Total active students
* Total departments
* Total courses
* Average student marks
* Highest-scoring student
* Recently joined students

This gives the user a quick summary of the current training portal data.

---

# Student Filtering and Search

The Student List supports filtering and searching.

Available filters include:

### Department

Filter students based on their department.

### Course

Filter students based on enrolled courses.

### Active Status

Filter students based on whether they are active or inactive.

### Pass / Fail Status

Filter students according to their marks.

```text
Marks >= 40 → Pass
Marks < 40  → Fail
```

### Search

Students can be searched using information such as:

* Student name
* Student email
* Course name

The application also displays a clear message when no students match the selected filters or search criteria.

---

# Authentication

The project includes basic Django user authentication.

## Registration

URL:

```text
/register/
```

New users can create an account.

---

## Login

URL:

```text
/login/
```

Users can log in using their Django account.

After successful login, the user is redirected to the student list.

---

## Logout

URL:

```text
/logout/
```

The user is logged out and redirected to the login page.

---

# Protected Pages

Django's authentication system is used to protect student-related pages.

The project uses:

```python
@login_required
```

Unauthenticated users attempting to access protected pages are redirected to the login page.

The home page remains publicly accessible.

### Access Rules

| Page                     | Access          |
| ------------------------ | --------------- |
| `/`                      | Public          |
| `/about/`                | Public          |
| `/students/`             | Logged-in users |
| `/students/add/`         | Logged-in users |
| `/students/<id>/edit/`   | Logged-in users |
| `/students/<id>/delete/` | Logged-in users |
| `/dashboard/`            | Logged-in users |

The navigation bar also displays the currently logged-in username.

---

# Django Messages

Django's messages framework is used to provide feedback after important actions.

Examples include messages for:

* Student added successfully
* Student updated successfully
* Student deleted successfully
* Successful login
* Successful logout
* Registration success
* Form validation errors

---

# Templates

The project uses Django templates instead of returning HTML directly from views.

A common base template is used:

```text
templates/base.html
```

Other pages extend the base template using Django template inheritance.

Example structure:

```text
base.html
    │
    ├── home.html
    ├── about.html
    ├── dashboard.html
    ├── student_list.html
    ├── student_detail.html
    ├── add_student.html
    ├── edit_student.html
    ├── student_confirm_delete.html
    ├── login.html
    └── register.html
```

The base template provides common elements such as navigation and page structure.

---

# URL Structure

The project uses named URLs to avoid hard-coded paths.

Main URLs include:

| URL                      | Description           |
| ------------------------ | --------------------- |
| `/`                      | Home page             |
| `/about/`                | About page            |
| `/dashboard/`            | Student dashboard     |
| `/students/`             | Student list          |
| `/students/<id>/`        | Student details       |
| `/students/add/`         | Add student           |
| `/students/<id>/edit/`   | Edit student          |
| `/students/<id>/delete/` | Delete student        |
| `/register/`             | User registration     |
| `/login/`                | User login            |
| `/logout/`               | User logout           |
| `/admin/`                | Django administration |

---

# Service Layer

The application contains:

```text
students/services.py
```

The service layer is used to keep reusable business or data-processing logic separate from the views.

This helps avoid putting all application logic into a single view and makes the code easier to maintain.

---

# Django Concepts Learned

This project provided practical experience with:

### Django Fundamentals

* Django project structure
* Django applications
* Settings
* URL routing
* Views
* Templates
* Template inheritance
* Template context
* Template loops
* Template conditions

### Database

* Django models
* Model fields
* Model relationships
* `ForeignKey`
* `OneToOneField`
* `ManyToManyField`
* `related_name`
* `__str__()`
* SQLite
* Migrations
* `makemigrations`
* `migrate`

### CRUD

* Create
* Read
* Update
* Delete
* `get_object_or_404()`
* Redirects
* Confirmation pages

### Forms

* ModelForms
* Form validation
* `form.is_valid()`
* `form.save()`
* Custom validation
* Validation error display

### ORM

* QuerySets
* `filter()`
* `get()`
* `exclude()`
* `order_by()`
* `count()`
* `aggregate()`
* `annotate()`
* `Q` objects
* `update()`
* `delete()`
* `select_related()`
* `prefetch_related()`

### Authentication

* Django User model
* Registration
* Login
* Logout
* `login_required`
* Authentication redirects
* Django messages
* Logged-in username

### Application Design

* Service layer
* Named URLs
* Reverse URL resolution
* Separation of responsibilities
* Template inheritance

### Testing

* Django TestCase
* Model testing
* Form testing
* View testing
* Boundary testing
* Validation testing

---

# Problems Faced and Solutions

## Model and Database Synchronization

Changes to models require migrations before they can be reflected in the database.

Solution:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Form Validation

User input needs to be validated before being stored in the database.

The project uses Django ModelForms and validation rules for fields such as age, marks, email, name, and course.

---

## Related Models

Introducing departments, profiles, and courses required understanding Django relationships.

The project uses:

```text
ForeignKey
OneToOneField
ManyToManyField
```

---

## Authentication

Student pages need to be protected from unauthenticated access.

Django's built-in authentication system and:

```python
@login_required
```

are used to restrict access.

---

## Filtering and Search

The student list combines multiple filters and search conditions.

The filtering system supports department, course, active status, pass/fail status, and text-based searching.

---

# Git

Git is used to track changes to the project.

View the commit history:

```bash
git log --oneline
```

Check the current working tree:

```bash
git status
```

Add changes:

```bash
git add .
```

Create a commit:

```bash
git commit -m "Update student training portal"
```

---

# How to Run

From the directory containing `manage.py`:

## 1. Activate the virtual environment

```bash
venv\Scripts\activate
```

## 2. Apply migrations

```bash
python manage.py migrate
```

## 3. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

# Main Application Pages

After starting the server, the main pages can be accessed through:

```text
/
```

```text
/about/
```

```text
/dashboard/
```

```text
/students/
```

```text
/students/add/
```

```text
/login/
```

```text
/register/
```

The Django administration panel is available at:

```text
/admin/
```

---

# Project Status

The Student Training Portal brings together the major concepts covered during the Django training tasks:

```text
Django Fundamentals
        ↓
Models & Migrations
        ↓
Model Relationships
        ↓
CRUD Operations
        ↓
ModelForms & Validation
        ↓
Django ORM
        ↓
Authentication
        ↓
Dashboard
        ↓
Filtering & Search
        ↓
Testing
```

The project serves as a practical demonstration of building a database-driven Django application with authentication, relationships, CRUD functionality, ORM operations, and a user-facing student dashboard.
