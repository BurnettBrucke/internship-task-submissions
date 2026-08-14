# Student Training Portal (Django & FastAPI)

The **Student Training Portal** is a production-ready, role-based student management web application built with **Django 6** and a companion **FastAPI** microservice. Styled with modern **Bootstrap 5** templates, static CSS, custom glassmorphism components, and dynamic micro-interactions.

---

## Key Features

- **Role-Based Access Control**: Tailored dashboards for Administrators, Trainers, and Students.
- **Enrollment-Based Course Marks**: Relational `Enrollment` model (`Student --< Enrollment >-- Course`) providing course-specific grades, historical score tracking (`MarksHistory`), and feedback (`Feedback`).
- **Student Directory & Pagination**: Multi-criterion search and filtering with preserved pagination parameters.
- **Security & Lockout**: Cache-backed brute-force lockout, safe `next` parameter validation, POST-only account status toggling & logout, custom 403, 404, and 500 pages.
- **FastAPI Microservice**: Separate RESTful API with validation, filtering, pagination, and Swagger UI (`/docs`).
- **Production Ready**: Environment variable configuration, static file collection, and production deployment settings (`settings_prod.py`).

---

## Role & Permission Matrix

| Role | Student Directory | Edit Marks | Add Feedback | User Management | Audit Logs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Administrator** | Full Access (Read/Write) | Full Access | Read Only | Full Access (Approve/Toggle) | Full Access (Read) |
| **Trainer** | Assigned Students Only | Assigned Courses Only | Assigned Students Only | Access Denied | Access Denied |
| **Student** | Own Profile Only | Read Only (Own) | Own Visible Feedback Only | Access Denied | Access Denied |

---

## Non-Production Demo Credentials

The project includes an idempotent demo seed command (`seed_demo_data`) that populates initial data with the following pre-configured credentials:

| Role | Username | Password | Scope |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `AdminPass123!` | System Administrator with full access |
| **Trainer** | `trainer1` | `TrainerPass123!` | Trainer assigned to Full-Stack Web & Cloud courses |
| **Trainer** | `trainer2` | `TrainerPass123!` | Trainer assigned to Data Science & Python courses |
| **Student** | `student1` | `StudentPass123!` | Enrolled Student with personal profile & grade view |

---

## Quickstart & Commands Guide

### 1. Requirements Installation

```bash
# Navigate to training_project
cd training_project

# Install requirements
pip install -r requirements.txt
```

### 2. Database & Migrations

```bash
# Migration cleanliness check
python manage.py makemigrations --check --dry-run

# Run database migrations
python manage.py migrate
```

### 3. Load Idempotent Sample Seed Data

```bash
# Seed 20+ students, 5 courses, 5 departments, enrollments, marks, feedback, and demo accounts
python manage.py seed_demo_data
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 5. Run Django Server

```bash
python manage.py runserver
```
Access Django Portal at `http://127.0.0.1:8000/`.

---

## Running FastAPI Project

```bash
# Navigate to fastapi_training directory
cd fastapi_training

# Run FastAPI dev server with uvicorn
uvicorn app.main:app --reload --port 8001
```

- **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8001/docs`
- **ReDoc API Documentation**: `http://127.0.0.1:8001/redoc`

---

## Running Test Suites

### Django Tests
```bash
python manage.py test
```

### FastAPI Pytest
```bash
cd fastapi_training
python -m pytest
```

---

## Deployment Security Checks

```bash
python manage.py check --deploy --settings=training_project.settings_prod
```
