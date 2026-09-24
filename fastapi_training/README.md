# FastAPI Student Training API

A beginner-friendly FastAPI project that implements a Student CRUD API using in-memory data storage.

## Project Overview

This project is a small API-based version of the Student Training Portal.

It demonstrates:

* FastAPI application and routes
* Pydantic request and response models
* CRUD operations
* Path parameters
* Query parameters
* Input validation
* HTTP status codes
* Filtering
* Pagination
* Automatic API documentation
* Automated API testing

## Project Structure

```text
fastapi_training/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── services.py
│
├── tests/
│   ├── __init__.py
│   └── test_students.py
│
├── requirements.txt
└── README.md
```

## Installation

Make sure Python is installed on your system.

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI development server:

```powershell
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

### OpenAPI Schema

```text
http://127.0.0.1:8000/openapi.json
```

## API Endpoints

| Method | Endpoint                 | Description          | Status    |
| ------ | ------------------------ | -------------------- | --------- |
| GET    | `/health`                | Check API status     | 200       |
| GET    | `/students`              | Get all students     | 200       |
| GET    | `/students/{student_id}` | Get student by ID    | 200 / 404 |
| POST   | `/students`              | Create a new student | 201       |
| PATCH  | `/students/{student_id}` | Update student       | 200 / 404 |
| DELETE | `/students/{student_id}` | Delete student       | 204 / 404 |

## Student Validation

The API validates student data using Pydantic.

* Name: 2–100 characters
* Email: Valid email format
* Age: 16–60
* Marks: 0–100
* Active status: Boolean

Invalid input returns:

```text
422 Unprocessable Entity
```

## Filtering

Students can be filtered using query parameters.

### Filter by active status

```text
GET /students?active_status=true
```

### Filter by minimum marks

```text
GET /students?min_marks=80
```

### Combine filters

```text
GET /students?active_status=true&min_marks=80
```

## Pagination

Pagination is supported using `skip` and `limit`.

```text
GET /students?skip=0&limit=10
```

Example:

```text
GET /students?skip=2&limit=5
```

* `skip` must be 0 or greater.
* `limit` must be between 1 and 100.

## Testing

The project contains automated tests using Pytest.

Run all FastAPI tests with:

```powershell
pytest
```

### Test Coverage

The test suite contains 10 tests covering:

1. Health check
2. Get all students
3. Get student by ID
4. Student not found
5. Create student
6. Invalid email validation
7. Invalid age validation
8. Invalid marks validation
9. Update student
10. Delete student

Current test result:

```text
10 passed
```

## Data Storage

This project currently uses an **in-memory list** for student data.

There is no database connected to this FastAPI application.

Therefore, data created, updated, or deleted through the API will reset when the application restarts.

## Application Flow

The API follows a simple layered structure:

```text
Client
  ↓
FastAPI Route
  ↓
Pydantic Validation
  ↓
Service Layer
  ↓
In-Memory Student Data
  ↓
Response Model
  ↓
Client
```

## File Responsibilities

### `app/main.py`

Contains:

* FastAPI application instance
* API routes
* Path parameters
* Query parameters
* HTTP status codes
* HTTPException handling

### `app/schemas.py`

Contains Pydantic models for:

* Student creation
* Student update
* Student response
* Input validation

### `app/services.py`

Contains:

* Student data
* CRUD operations
* Filtering logic
* Pagination logic

### `tests/test_students.py`

Contains automated tests for:

* API responses
* CRUD operations
* Error handling
* Input validation

## HTTP Status Codes Used

| Status Code | Meaning                      |
| ----------- | ---------------------------- |
| 200         | Successful request           |
| 201         | Student created successfully |
| 204         | Student deleted successfully |
| 404         | Student not found            |
| 422         | Validation error             |

## Future Improvements

Possible improvements for a production version:

* Connect a database
* Add authentication and authorization
* Add database migrations
* Add centralized error handling
* Add logging
* Add environment variables
* Add more comprehensive test coverage
