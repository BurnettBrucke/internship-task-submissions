# Training Project – Django Student Management System

A Django-based Student Management System developed as part of Python and Django Training.

The project demonstrates Django fundamentals including models, migrations, admin panel, templates, URL routing, ModelForms, form validation, and database operations.

---

## Project Structure

```text
training_project/
│
├── manage.py
│
├── training_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── students/
│   ├── migrations/
│   ├── templates/
│   │   └── students/
│   │       ├── student_list.html
│   │       └── student_form.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
│
└── db.sqlite3
```

---

# Requirements

* Python 3.x
* Django
* VS Code
* Git

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

Verify the installation:

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

The `students` application contains the Student model, admin configuration, views, URLs, forms, templates, and tests.

---

# Database and Migrations

Create migrations after making changes to the models:

```bash
python manage.py makemigrations
```

Apply migrations to the database:

```bash
python manage.py migrate
```

The project uses Django's default SQLite database:

```text
db.sqlite3
```

---

# Student Model

The `Student` model contains the following fields:

| Field         | Description             |
| ------------- | ----------------------- |
| `name`        | Student name            |
| `email`       | Student email           |
| `age`         | Student age             |
| `course`      | Student course          |
| `marks`       | Student marks           |
| `joined_date` | Date the student joined |
| `active`      | Student active status   |

A meaningful `__str__()` method is used to provide a readable representation of Student objects in Django Admin.

---

# Django Admin

The Student model is registered in the Django admin panel.

Create a superuser using:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the admin panel at:

```text
/admin/
```

The admin panel can be used to:

* Add students
* View students
* Update students
* Delete students
* Manage student information

---

# Student List

The student list page displays all students from the database.

The page includes:

* Student name
* Email
* Age
* Course
* Marks
* Joined date
* Active status
* Pass/Fail status
* Total student count
* Active student information

### Pass/Fail Rule

```text
Marks >= 40 → Pass
Marks < 40  → Fail
```

The student list is rendered using Django templates, template loops, and template conditions.

---

# Student Form

A Django `ModelForm` is used to add new students.

The Add Student page is available at:

```text
/students/add/
```

The form validates the submitted information before saving it to the database.

### Validation Rules

| Field  | Validation                |
| ------ | ------------------------- |
| Name   | Cannot be empty           |
| Email  | Must be a valid email     |
| Age    | Must be between 16 and 60 |
| Marks  | Must be between 0 and 100 |
| Course | Cannot be empty           |

Invalid form submissions display validation errors on the page.

After successful submission, the user is redirected to:

```text
/students/
```

---

# URLs

The project contains the following required pages:

| URL              | Description           |
| ---------------- | --------------------- |
| `/`              | Home page             |
| `/about/`        | About page            |
| `/students/`     | Student list          |
| `/students/add/` | Add student           |
| `/admin/`        | Django administration |

---

# Running the Project

From the directory containing `manage.py`, run:

```bash
python manage.py runserver
```

The development server will be available at:

```text
http://127.0.0.1:8000/
```

---

# Testing

The Django application is tested against normal and edge-case inputs.

### Student Model

* Student creation
* Student retrieval
* Student information validation
* Active status

### Student List

* Display all students
* Display total student count
* Display active students
* Pass/Fail calculation

### Student Form

* Empty name
* Invalid email
* Age below 16
* Age above 60
* Marks below 0
* Marks above 100
* Empty course
* Valid student submission
* Validation error display
* Successful redirect

### Marks Boundary Testing

The following values are specifically tested:

```text
0   → Fail
40  → Pass
100 → Pass
```

---

# Django Concepts Learned

This project provided practical experience with:

* Django project structure
* Django applications
* URL routing
* Views
* Templates
* Template context
* Template loops
* Template conditions
* Django models
* Model fields
* `__str__()`
* Migrations
* `makemigrations`
* `migrate`
* Django Admin
* Superuser
* SQLite database
* ModelForms
* Form validation
* GET requests
* POST requests
* `form.is_valid()`
* `form.save()`
* Redirects
* Django messages

---

# Problems Faced

### Model and Database Synchronization

Changes to the Student model require migrations before they can be reflected in the database.

### Form Validation

Input validation was required to ensure that age, marks, email, name, and course values followed the specified requirements.

### Template Rendering

The project uses Django templates rather than placing HTML directly inside views. Data is passed from views to templates using context.

### Pass/Fail Logic

The student list uses a marks boundary of `40` to determine whether a student has passed or failed.

---

# Git

Git is used to track changes to the Django project.

View commit history using:

```bash
git log --oneline
```

# How to Run

```bash
# Activate virtual environment
venv\Scripts\activate

# Apply migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Then visit:

```text
/
```

or:

```text
/students/
```

to access the application.
