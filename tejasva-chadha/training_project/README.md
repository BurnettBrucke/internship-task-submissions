# Student Training Portal

The **Student Training Portal** is a production-ready, role-based student management web application built with **Django 6** and styled with modern **Bootstrap 5** templates, static CSS, custom glassmorphism components, and dynamic micro-interactions.

---

## Key Features

- **Role-Based Access Control**: Tailored dashboards for Administrators, Trainers, and Students.
- **Student Directory & Filtering**: Search by query, department, course, active status, and pass/fail grades with pagination.
- **Marks Management & Audit Trail**: Role-scoped grade updates, complete historical tracking (`MarksHistory`), and detailed security logs (`AuditLog`).
- **Feedback System**: Assigned trainers can submit 1–5 star ratings and qualitative feedback visible to students.
- **Security & Brute-Force Lockout**: Consecutive failure tracking with temporary account lockouts, custom 403, 404, and 500 pages, and double-submission prevention.
- **Production Ready**: Environment variable support, static file collection, and production settings template (`settings_prod.py`).

---

## Role & Permission Matrix

| Role | Student Directory | Edit Marks | Add Feedback | User Management | Audit Logs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Administrator** | Full Access (Read/Write) | Yes | Read Only | Full Access (Approve/Toggle) | Full Access (Read) |
| **Trainer** | Assigned Students Only | Assigned Only | Assigned Students Only | Access Denied | Access Denied |
| **Student** | Own Profile Only | Read Only (Own) | Own Visible Feedback Only | Access Denied | Access Denied |

---

## Demo Credentials

The project includes a seed data management command (`seed_data`) that populates initial data with the following pre-configured demo credentials:

| Role | Username | Password | Access / Scope |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `Admin@123` | System Administrator with full access |
| **Trainer** | `trainer1` | `Trainer@123` | Trainer assigned to Web Dev & Cloud courses |
| **Trainer** | `trainer2` | `Trainer@123` | Trainer assigned to Data Science & Python courses |
| **Student** | `student1` | `Student@123` | Enrolled Student with personal profile & grade view |

---

## Quickstart & Setup Guide

### 1. Environment Setup

```bash
# Navigate to the project directory
cd training_project

# Activate your virtual environment (if using one)
# source venv/bin/activate  (Linux/macOS)
# venv\Scripts\activate     (Windows)

# Install requirements (Django)
pip install django
```

### 2. Database & Migrations

```bash
# Run database migrations
python manage.py migrate
```

### 3. Load Sample Seed Data

```bash
# Seed 20+ students, 5 courses, 5 departments, feedback, marks history, and demo accounts
python manage.py seed_data
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser to access the portal.

---

## Release & Deployment Checklist

### Production Configuration

1. **Environment Variables**: Copy `.env.example` to `.env` and fill in secrets:
   ```env
   DJANGO_SECRET_KEY=your-strong-production-secret-key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,127.0.0.1
   ```

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Production Settings**:
   Run with `settings_prod.py`:
   ```bash
   python manage.py check --settings=training_project.settings_prod
   ```

4. **Run Full Test Suite**:
   ```bash
   python manage.py test
   ```

---

## Security & Session Controls

* **`SESSION_COOKIE_HTTPONLY`** (`True`): Protects session cookies from client-side script inspection.
* **`SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE`**: Set to `True` in production HTTPS environments.
* **Login Lockout**: Locks account for 5 minutes after 5 consecutive failed attempts.
