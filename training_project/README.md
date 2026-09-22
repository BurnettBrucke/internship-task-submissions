# Student Training Portal

A Django-based Student Training Portal developed as part of the training project. The application provides role-based authentication, student and course management, marks, feedback, audit logs, dashboards, search, filtering, pagination, and automated testing.

## Technologies

* Python
* Django 5.2.10
* SQLite
* HTML, CSS, Bootstrap 5
* Django ORM
* Django ModelForms
* Django Authentication

## Features

* Role-based access for Admin, Trainer, and Student
* User registration, login, logout, password reset and password change
* Trainer approval and account management
* Student, Course, Trainer and User management
* Student-course assignments
* Marks management with update history
* Trainer feedback with ratings and visibility control
* Audit logs for important activities
* Search, filtering and pagination
* Dashboard statistics
* Form validation and Django messages
* Custom 403, 404 and 500 error pages
* Responsive Bootstrap UI
* Demo data management command
* Production settings and static file configuration

## Setup

Install Python and Django, then run:

```bash
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Application:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

## Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

The `.env` file should not be committed to the repository.

## Testing

Run the complete test suite:

```bash
python manage.py test
```

Current result:

```text
Ran 20 tests

OK
```

## Demo Data

Demo data can be created using:

```bash
python manage.py seed_demo_data
```

The command creates departments, courses, students, profiles, course assignments and other sample data for testing and demonstration.

## Production Preparation

Production configuration is available in `training_project/production.py`.

Static files can be collected using:

```bash
python manage.py collectstatic
```

Migration status can be verified using:

```bash
python manage.py makemigrations --check
python manage.py migrate --plan
```

## Project Structure

```text
training_project/
├── students/
├── templates/
├── training_project/
├── manage.py
└── README.md
```

## Learning & Practice

This project covers Django models and relationships, authentication and authorization, CRUD operations, ORM queries, ModelForms, service-layer logic, role-based access, validation, audit logging, testing and deployment preparation.

## Git

The project is maintained using Git with a dedicated internship branch.
