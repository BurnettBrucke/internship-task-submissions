# Training Project - Django Student Management System

## Overview

This project was created as part of the Burnett Brucke internship training.

The project is a Django-based Student Management System that demonstrates CRUD operations, model relationships, Django ORM, authentication, templates, forms, search/filtering, dashboard and testing.

---

## Technology Used

- Python
- Django
- SQLite
- HTML
- Django Templates

---

## Project Structure

Training_Project/

│
├── students/

│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── Training_Project/

│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
├── orm_queries.md
└── README.md

---

# Tasks Completed

## Task 1 - Student CRUD Operations

Implemented complete CRUD functionality for Student records.

### Features Implemented

- Student List page
- Student Detail page
- Add Student
- Edit Student
- Delete Student
- Delete confirmation
- ModelForm for Add/Edit
- Form validation
- Success and error messages
- `get_object_or_404()` for student records
- Redirect after successful operations
- Navigation between student pages

### URLs

- `/students/` - Student List
- `/students/add/` - Add Student
- `/students/<id>/` - Student Detail
- `/students/<id>/edit/` - Edit Student
- `/students/<id>/delete/` - Delete Student

---

## Task 2 - Model Relationships

Implemented the required Django model relationships.

### Relationships Implemented

- Department → Student: ForeignKey
- Student → StudentProfile: OneToOneField
- Student ↔ Course: ManyToManyField

### Features Implemented

- Added `related_name`
- Added `on_delete` behavior
- Added meaningful `__str__()` methods
- Created and applied migrations
- Registered models in Django Admin
- Added sample departments, courses, students and profiles

---

## Task 3 - Django ORM Queries

Practiced Django ORM operations using Django Shell.

### ORM Operations Covered

- Retrieve and filter students
- Search students
- Filter by marks
- Order students
- Count records
- Aggregate marks
- Find highest-scoring student
- Work with Department relationships
- Work with Course relationships
- Update records
- Delete records
- Use `Q` objects
- Use `annotate()`
- Use `select_related()`
- Use `prefetch_related()`

A total of **20 ORM queries** were completed and documented in:

`orm_queries.md`

---

## Task 4 - User Authentication

Implemented Django user authentication.

### Features Implemented

- User Registration
- User Login
- User Logout
- Protected pages
- Display logged-in username
- Django built-in User model
- `login_required`
- Authentication functions
- Django messages
- Login/Register/Logout navigation
- Login and logout redirects

Student management pages are protected and require user login.

---

## Task 5 - Student Training Portal

Combined all features into a Student Training Portal.

### Dashboard Features

- Total Students
- Total Active Students
- Total Departments
- Total Courses
- Average Student Marks
- Highest-Scoring Student
- Recently Joined Students

### Student List Features

- Student Name
- Email
- Department
- Course Count
- Marks
- Pass/Fail Status
- Active/Inactive Status
- View Action
- Edit Action
- Delete Action

### Search and Filtering

- Search by Name
- Search by Email
- Search by Course
- Filter by Department
- Filter by Course
- Filter by Active/Inactive Status
- Filter by Pass/Fail Status
- No-records message

### Template Features

- Base template
- Template inheritance
- Navigation bar
- Django messages
- Student data table
- Named URLs
- Reverse URL resolution

---

# Testing Completed

Implemented **15 test cases** covering:

1. Student list
2. Student detail
3. Student creation
4. Invalid form submission
5. Student update
6. Student deletion
7. Login page
8. Successful login
9. Protected page redirect
10. Department relationship
11. One-to-one profile relationship
12. Many-to-many course relationship
13. Search functionality
14. Department filter
15. Dashboard totals

---

# Key Django Concepts Learned

- Django Project and App
- URL Routing
- Views
- Templates
- Template Inheritance
- Models
- ForeignKey
- OneToOneField
- ManyToManyField
- Database Migrations
- Django Admin
- ModelForm
- Form Validation
- CRUD Operations
- Django ORM
- QuerySets
- Q Objects
- Aggregation and Annotation
- Authentication
- `login_required`
- Django Messages
- Search and Filtering
- Django Testing

---

# Learning Outcome

By completing this project, I gained practical experience in developing a complete Django web application.

I learned how models, views, URLs, templates, forms, database operations and authentication work together.

I also learned how to implement model relationships, write ORM queries, create a dashboard, add search and filtering, protect pages with authentication, and test Django functionality.

---

# Project Status

**All Day 3 assigned Django training tasks have been completed successfully.**