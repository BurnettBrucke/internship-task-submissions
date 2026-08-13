# FastAPI Student Training API

A modern, high-performance RESTful API built with **FastAPI** and **Pydantic** for managing student training data.

---

## Features

- **Pydantic Validation**: Strict schema validation for emails, age (16-60), marks (0-100), and name length (2-100 characters).
- **Service Layer Architecture**: Business logic and data management isolated in `app/services.py`.
- **Filtering & Pagination**: Query parameters for `is_active`, `min_marks`, `skip`, and `limit`.
- **Automated Interactive Docs**: Swagger UI (`/docs`) and ReDoc (`/redoc`) generated automatically by OpenAPI standard.
- **Full Test Suite**: 15 comprehensive automated test cases covering valid flows, edge cases, validation errors, and 404 handling.

---

## Project Structure

```
fastapi_training/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI routes & application configuration
│   ├── schemas.py     # Pydantic data schemas & input validators
│   └── services.py    # Business logic & in-memory data management
├── tests/
│   ├── __init__.py
│   └── test_main.py   # Pytest test suite (15 test cases)
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

---

## Requirements & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application Server
Start the Uvicorn ASGI server with hot-reload enabled:
```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

---

## API Endpoints Reference

| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Application health check & status | `200 OK` |
| `GET` | `/students` | List students (filters: `is_active`, `min_marks`, `skip`, `limit`) | `200 OK` |
| `GET` | `/students/{student_id}` | Retrieve details of a student by ID | `200 OK` / `404 Not Found` |
| `POST` | `/students` | Create a new student record | `201 Created` / `422 Unprocessable` |
| `PATCH` | `/students/{student_id}` | Partially update student fields | `200 OK` / `404 Not Found` / `422 Unprocessable` |
| `DELETE` | `/students/{student_id}` | Delete a student record by ID | `204 No Content` / `404 Not Found` |

---

## Interactive Documentation

- **Swagger UI**: Visit `http://127.0.0.1:8000/docs` to interactively test endpoints, view request body schemas, and response types.
- **ReDoc**: Visit `http://127.0.0.1:8000/redoc` for clean, human-friendly API schema specifications.

---

## Running Automated Tests

Run `pytest` to execute all 15 test cases:

```bash
pytest
```
Or for verbose test output:
```bash
pytest -v
```
