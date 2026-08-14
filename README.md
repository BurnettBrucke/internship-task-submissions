# BurnettBrucke Internship - Day 5 Student Training Portal Submission

This repository contains the completed Day 5 Student Training Portal project, featuring a Django web application and a FastAPI REST microservice.

---

## Workspace Projects

1. **`tejasva-chadha/training_project/`**: Django 6 Web Application with role-based dashboards, Enrollment-centric course marks, feedback, audit logs, security controls, static styling, and full test suite.
2. **`tejasva-chadha/fastapi_training/`**: FastAPI REST API microservice with validation, filtering, pagination, and pytest suite.

---

## Quickstart Instructions

### 1. Django Training Portal

```bash
cd tejasva-chadha/training_project

# Run migrations
python manage.py migrate

# Seed safe demo data (20+ students, 5 courses, demo accounts)
python manage.py seed_demo_data

# Run Django development server
python manage.py runserver
```
Portal URL: `http://127.0.0.1:8000/`

**Demo Credentials**:
- **Admin**: `admin` / `AdminPass123!`
- **Trainer**: `trainer1` / `TrainerPass123!`
- **Student**: `student1` / `StudentPass123!`

### 2. FastAPI Microservice

```bash
cd tejasva-chadha/fastapi_training

# Run FastAPI server
uvicorn app.main:app --reload --port 8001
```
- **Swagger Documentation**: `http://127.0.0.1:8001/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8001/redoc`

---

## Test Suites

```bash
# Run Django test suite (70+ tests)
cd tejasva-chadha/training_project
python manage.py test

# Run FastAPI pytest suite (15 tests)
cd tejasva-chadha/fastapi_training
python -m pytest
```
