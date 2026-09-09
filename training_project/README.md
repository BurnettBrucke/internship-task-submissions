# Student Training Portal

A Django-based Student Training Portal developed as part of the training project. The application provides authentication, student CRUD operations, dashboard statistics, search, filtering, Django ORM queries, and automated testing.

## Technologies

* Python
* Django 5.2.10
* SQLite
* HTML/CSS
* Django ORM
* Django ModelForm
* Django Authentication

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install Django:

```bash
pip install django
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Run server:

```bash
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

## URLs

* `/` - Home
* `/about/` - About
* `/register/` - Registration
* `/login/` - Login
* `/logout/` - Logout
* `/dashboard/` - Dashboard
* `/students/` - Student List
* `/students/add/` - Add Student
* `/students/<id>/` - Student Details
* `/students/<id>/edit/` - Edit Student
* `/students/<id>/delete/` - Delete Student

## Authentication

Django built-in authentication is used for registration, login and logout.

Dashboard and student management pages are protected using `login_required`.

## Models & Relationships

The project contains:

* **Department**
* **Course**
* **Student**
* **StudentProfile**

Relationships:

* Department → Student: `ForeignKey`
* Student ↔ Course: `ManyToManyField`
* Student → StudentProfile: `OneToOneField`

## Features

* Student CRUD operations
* Dashboard statistics
* Search by name, email and course
* Department and course filtering
* Active/Inactive filtering
* Pass/Fail filtering
* Student form validation
* Django messages
* Template inheritance
* Business logic separated into `services.py`

## ORM Queries

Django ORM is used for:

* CRUD operations
* Filtering and searching
* `Q` queries
* `Avg()` and `Max()`
* Counting records
* Relationship queries
* Recently joined students

Detailed queries are available in `orm_queries.md`.

## Testing

The project contains **20 automated tests** covering CRUD, authentication, dashboard, search, filters, relationships and form validation.

Run tests:

```bash
python manage.py test students
```

Result:

```text
Ran 20 tests

OK
```

## Problems Faced & Topics Learned

Practiced Django models, relationships, migrations, ORM, ModelForms, authentication, CRUD, search/filtering, template inheritance, service layer, Django messages and automated testing.

## Git Commit ID

Final commit ID will be added after the final changes are committed and pushed.

## Pending Work

* Add final commit ID to README
