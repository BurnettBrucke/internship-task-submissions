# FastAPI Student Management API

A beginner-friendly Student Management REST API built using FastAPI.

This project was created as part of FastAPI training to understand API
development, Pydantic validation, request/response handling, filtering,
pagination, HTTP status codes, Swagger documentation, and API testing.

---

## Features

- Health check API
- Get all students
- Get student by ID
- Create a new student
- Update student details
- Delete a student
- Student validation using Pydantic
- Email validation
- Age validation: 16–60
- Marks validation: 0–100
- Active/inactive student filtering
- Minimum marks filtering
- Pagination using skip and limit
- Combined filters
- 404 handling for missing students
- Proper HTTP status codes
- Automatic Swagger documentation
- Automatic ReDoc documentation
- API testing using Pytest and TestClient

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- HTTPX
- Email Validator

---

## Project Structure

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
├── README.md
└── venv/

---

## Installation

### 1. Create virtual environment
python -m venv venv

### 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

**If PowerShell blocks script execution:**
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

**Then activate again:**
.\venv\Scripts\Activate.ps1

### 3. Install dependencies
pip install -r requirements.txt

### Run the Application

**Start the FastAPI development server:**
uvicorn app.main:app --reload

### The application will run at:
http://127.0.0.1:8000

---

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

**Open:** http://127.0.0.1:8000/docs

Swagger allows you to test all API endpoints directly from the browser.

### ReDoc

**Open:** http://127.0.0.1:8000/redoc

ReDoc provides another automatically generated API documentation interface.

---

## API Endpoints

### 1. Health Check

#### GET /health
Checks whether the API is running.

**Example response:**

{
    "status": "healthy",
    "message": "Student API is running"
}

**Status code:** 200 OK

### 2. Get All Students

#### GET /students
Returns all students.

**Example:** GET /students

### 3. Filter Active Students

#### GET /students?active=true
Returns only active students.

**Example**: GET /students?active=true

**For inactive students:** GET /students?active=false

### 4. Filter by Minimum Marks

#### GET /students?min_marks=80
Returns students whose marks are greater than or equal to 80.

**Example:** GET /students?min_marks=80

### 5. Pagination

The API supports pagination using skip and limit.

**Example:** GET /students?skip=0&limit=2

**Meaning:**

- skip=0 → start from the first record
- limit=2 → return maximum 2 records

**Validation:**

- skip must be greater than or equal to 0
- limit must be greater than or equal to 1

### 6. Combined Filters

Multiple query parameters can be used together.

**Example:** GET /students?active=true&min_marks=80

**This returns students who:**
- are active
- have marks greater than or equal to 80

### 7. Get Student by ID

#### GET /students/{student_id}

**Example:** GET /students/1

- If the student exists, student details are returned.

- If the student does not exist:

{
    "detail": "Student not found"
}

**Status code:** 404 Not Found

### 8. Create Student

#### POST /students

**Example request body:**

{
    "name": "Neha",
    "email": "neha@example.com",
    "age": 23,
    "marks": 91,
    "active": true
}

**Successful response:** 201 Created

### 9. Update Student

#### PATCH /students/{student_id}

**Example:** PATCH /students/1

**Request body:**

{
    "marks": 95
}

**Successful response:** 200 OK

**If the student does not exist:** 404 Not Found

### 10. Delete Student

#### DELETE /students/{student_id}

**Example:** DELETE /students/1

**Successful response:** 204 No Content

**If the student does not exist:** 404 Not Found

---

## Validation

Student data is validated using Pydantic models.

### Name

- Minimum length: 2 characters
- Maximum length: 100 characters

### Email

A valid email format is required.

### Age

16 <= age <= 60

### Marks

0 <= marks <= 100

**Invalid request data returns:** 422 Unprocessable Entity

---

## Testing

The project uses Pytest and FastAPI's TestClient.

**Run all tests using:** pytest -v

**The project currently contains 20 API tests covering:**

- Health check
- Get students
- Get student by ID
- Student not found
- Create student
- Invalid email
- Invalid age
- Invalid marks
- Update student
- Delete student
- Active student filtering
- Inactive student filtering
- Minimum marks filtering
- Pagination
- Pagination boundary
- Update non-existing student
- Delete non-existing student
- Combined filters
- Invalid skip
- Invalid limit

**Expected result:** 20 passed

---

## Architecture

The project separates API routes, validation schemas, and data handling.

### main.py

**Contains:**

- FastAPI application instance
- API routes
- Query parameters
- Path parameters
- Request handling
- Response models

### schemas.py

**Contains Pydantic models for:**

- Student creation
- Student update
- Student response

### services.py

**Contains:**

- In-memory student data
- Get operations
- Create operation
- Update operation
- Delete operation
- Filtering
- Pagination
- 404 handling

### test_students.py

Contains automated API tests using Pytest and TestClient.

---

## Django vs FastAPI

| Feature           | Django                             | FastAPI                            |
| ----------------- | ---------------------------------- | ---------------------------------- |
| Type              | Full web framework                 | Modern API-focused framework       |
| API Development   | Usually Django REST Framework      | Built into FastAPI                 |
| ORM               | Django ORM included                | No built-in ORM                    |
| Admin Panel       | Built-in                           | Not built-in                       |
| Templates         | Built-in                           | Not primarily focused on templates |
| Validation        | Forms/serializers depending on use | Pydantic                           |
| API Documentation | Additional tools commonly used     | Automatic Swagger/ReDoc            |
| Async Support     | Supported                          | Strong async support               |
| Learning Curve    | Broader framework                  | Lightweight for API development    |

---

## When to use Django

Django is useful when building a complete web application that needs features such as:

- Authentication
- Admin panel
- Database ORM
- Templates
- Full web application structure

---

## When to use FastAPI

FastAPI is useful when the main requirement is building:

- REST APIs
- Backend services
- Microservices
- High-performance APIs
- APIs consumed by web or mobile applications
- Machine learning model APIs

---

## Learning Outcomes

### Through this project, I learned:

- FastAPI application structure
- API routing
- Path parameters
- Query parameters
- Request bodies
- Pydantic models
- Response models
- Data validation
- HTTP status codes
- Filtering
- Pagination
- Service-layer separation
- Swagger and ReDoc
- Automated API testing
- Difference between Django and FastAPI

---