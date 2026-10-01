# FastAPI Student Management API

A small REST API built with **FastAPI** as part of the Python and Django internship training program.

The project rebuilds a small portion of the Django Student Management System as an API and demonstrates FastAPI fundamentals, Pydantic validation, CRUD operations, filtering, pagination, service-layer separation, and API testing.

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
│   └── test_api.py
│
├── api_design.md
├── requirements.txt
└── README.md
```

## Technologies Used

* Python 3.13
* FastAPI
* Uvicorn
* Pydantic
* Pytest
* HTTPX

## Setup

Create and activate a virtual environment, then install the required packages:

```bash
pip install -r requirements.txt
```

## Running the API

From the `fastapi_training` directory:

```bash
python -m uvicorn app.main:app --reload
```

The API runs at:

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

## API Endpoints

| Method | Endpoint                 | Purpose                |
| ------ | ------------------------ | ---------------------- |
| GET    | `/health`                | Check API health       |
| GET    | `/students`              | List students          |
| GET    | `/students/{student_id}` | Get a specific student |
| POST   | `/students`              | Create a student       |
| PATCH  | `/students/{student_id}` | Update a student       |
| DELETE | `/students/{student_id}` | Delete a student       |

## Filtering

Students can be filtered by active status:

```text
GET /students?active=true
```

```text
GET /students?active=false
```

Students can also be filtered by minimum marks:

```text
GET /students?min_marks=80
```

Filters can be combined:

```text
GET /students?active=true&min_marks=80
```

## Pagination

The student list supports `skip` and `limit` query parameters.

Example:

```text
GET /students?skip=0&limit=2
```

Another example:

```text
GET /students?skip=2&limit=2
```

`skip` controls how many records are skipped, while `limit` controls the maximum number of records returned.

## Validation

Pydantic models are used to validate request data.

### Student fields

| Field    | Validation         |
| -------- | ------------------ |
| `name`   | 2–100 characters   |
| `email`  | Valid email format |
| `age`    | 16–60              |
| `marks`  | 0–100              |
| `active` | Boolean            |

Invalid request data returns HTTP `422 Unprocessable Entity`.

## HTTP Status Codes

The API uses appropriate HTTP status codes:

* `200 OK` — Successful GET, PATCH operations
* `201 Created` — Successful student creation
* `204 No Content` — Successful student deletion
* `404 Not Found` — Student does not exist
* `422 Unprocessable Entity` — Invalid request data

## Service Layer

Data-handling logic is separated into `services.py`.

The API routes in `main.py` are responsible for handling HTTP requests and responses, while student operations are handled by the service layer.

This separation keeps the API code cleaner and makes the application easier to extend later.

## Testing

Automated API tests are written using Pytest and FastAPI's `TestClient`.

Run the test suite with:

```bash
python -m pytest
```

Current test result:

```text
14 passed
```

The tests cover:

* Health endpoint
* Student listing
* Student retrieval
* Missing student handling
* Student creation
* Input validation
* Student updates
* Student deletion
* Active-status filtering
* Minimum-marks filtering
* Pagination
* Invalid pagination

## API Design

The planned API resources and endpoint structure for the larger student management system are documented in:

```text
api_design.md
```

The design covers:

* Students
* Courses
* Enrollments
* Marks
* Feedback

## Learning Objectives

This project was created to practice:

* FastAPI application setup
* Route decorators
* Path parameters
* Query parameters
* Request bodies
* Pydantic models
* Response models
* HTTP status codes
* CRUD APIs
* Validation
* Filtering
* Pagination
* Service-layer architecture
* Automatic OpenAPI documentation
* API testing with Pytest

## Project Status

**Task 3 — FastAPI Introduction and First API: Completed**

The project currently contains a working FastAPI student API with CRUD operations, validation, filtering, pagination, service-layer separation, automatic documentation, API planning, and automated tests.
