# Secure Task Manager API

A FastAPI-based Task Management API with JWT authentication, role-based authorization, task ownership, validation, filtering, searching, sorting, pagination, and automated testing.

---

## Features

- User registration
- User login
- JWT authentication
- Current-user endpoint
- Protected task endpoints
- Task CRUD operations
- Task ownership
- Admin access
- User/Admin authorization
- Search tasks
- Filter by priority
- Filter by completion status
- Pagination
- Task sorting
- Request validation using Pydantic
- HTTP error handling
- Automated tests using pytest and FastAPI TestClient

---

## Project Structure

```text
fastapi_secure_task_manager/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   └── security.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── store.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── roles.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── .env
├── .env.example
├── .gitignore
├── readme.md
└── requirements.txt
```

---

# 1. Project Setup

Open a terminal and move into the project directory:

```bash
cd fastapi_secure_task_manager
```

---

# 2. Virtual Environment Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(venv)
```

---

# 3. Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

# 4. Environment Configuration

Create a `.env` file in the project root.

Example:

```env
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The `.env` file contains configuration values used by the application.

Do not commit the actual `.env` file to Git.

Use `.env.example` as a template:

```env
JWT_SECRET_KEY=change-this-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# 5. Start the FastAPI Server

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will normally run at:

```text
http://127.0.0.1:8000
```

---

# 6. API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger UI can be used to test the API endpoints directly.

---

# 7. API Endpoints

## Authentication Endpoints

| Method | Endpoint                | Description                 | Authentication |
| ------ | ----------------------- | --------------------------- | -------------- |
| POST   | `/api/v1/auth/register` | Register a new user         | No             |
| POST   | `/api/v1/auth/login`    | Login and receive JWT token | No             |
| GET    | `/api/v1/auth/me`       | Get current user            | Yes            |

---

## Task Endpoints

| Method | Endpoint                  | Description   | Authentication |
| ------ | ------------------------- | ------------- | -------------- |
| POST   | `/api/v1/tasks`           | Create a task | Yes            |
| GET    | `/api/v1/tasks`           | List tasks    | Yes            |
| GET    | `/api/v1/tasks/{task_id}` | Get a task    | Yes            |
| PUT    | `/api/v1/tasks/{task_id}` | Update a task | Yes            |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task | Yes            |

---

# 8. Authentication

The API uses JWT Bearer authentication.

After a successful login, the API returns an access token.

Example response:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer",
  "expires_in": 1800
}
```

Protected endpoints require the token in the request header:

```text
Authorization: Bearer <access_token>
```

In Swagger UI, use the **Authorize** button to provide the token.

---

# 9. Authorization Rules

The API supports two roles:

* `user`
* `admin`

| Action                     | Normal User | Admin |
| -------------------------- | ----------- | ----- |
| Create task                | Yes         | Yes   |
| View own tasks             | Yes         | Yes   |
| View another user's tasks  | No          | Yes   |
| Update own task            | Yes         | Yes   |
| Update another user's task | No          | Yes   |
| Delete own task            | Yes         | Yes   |
| Delete another user's task | No          | Yes   |

Each task contains an `owner_id` which identifies the user who created the task.

---

# 10. Task Creation

Example request:

```http
POST /api/v1/tasks
```

Request body:

```json
{
  "title": "Learn FastAPI",
  "description": "Complete Task CRUD",
  "priority": "high",
  "completed": false
}
```

Example response:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Complete Task CRUD",
  "priority": "high",
  "completed": false,
  "owner_id": 1
}
```

---

# 11. Task Search

Tasks can be searched using the `search` query parameter.

Example:

```text
GET /api/v1/tasks?search=python
```

The search can check task titles and descriptions.

---

# 12. Task Filtering

Tasks can be filtered by priority.

Example:

```text
GET /api/v1/tasks?priority=high
```

Supported priorities:

```text
low
medium
high
```

Tasks can also be filtered by completion status.

Example:

```text
GET /api/v1/tasks?completed=true
```

or:

```text
GET /api/v1/tasks?completed=false
```

---

# 13. Pagination

The task list endpoint supports pagination.

Example:

```text
GET /api/v1/tasks?page=1&limit=10
```

Parameters:

* `page` - Page number
* `limit` - Number of tasks per page

Validation:

```text
page >= 1
limit >= 1
limit <= 100
```

---

# 14. Sorting

Tasks can be sorted using the `sort_by` query parameter.

Example:

```text
GET /api/v1/tasks?sort_by=title
```

Supported fields:

```text
title
priority
completed
```

---

# 15. Request Validation

Pydantic schemas are used to validate request data.

Examples of invalid requests include:

* Empty task title
* Invalid email
* Invalid task priority
* Invalid completion value
* Short or invalid password
* Invalid query parameters

Validation errors return:

```text
422 Unprocessable Entity
```

---

# 16. HTTP Status Codes

| Status Code | Meaning                                        |
| ----------- | ---------------------------------------------- |
| 200         | Successful request                             |
| 201         | Resource created                               |
| 204         | Resource deleted successfully                  |
| 401         | Authentication required or invalid credentials |
| 403         | Authenticated but not authorized               |
| 404         | Resource not found                             |
| 409         | Conflict, such as duplicate username           |
| 422         | Validation error                               |

---

# 17. Running Automated Tests

The project uses:

* `pytest`
* FastAPI `TestClient`

Run all tests:

```bash
pytest -q
```

Or:

```bash
python -m pytest -q
```

---

# 18. Automated Test Cases

The project contains 15 automated tests covering:

1. Register new user successfully
2. Duplicate username should fail
3. Invalid email should fail
4. Short password should fail
5. Correct login returns token
6. Wrong password returns 401
7. `/auth/me` works with a valid token
8. Protected endpoint without token returns 401
9. User creates a task
10. User views own tasks
11. User cannot update another user's task
12. Admin can view another user's task
13. Admin can delete another user's task
14. Invalid priority should fail validation
15. Unknown task ID returns 404

---

# 19. Test Result

The complete automated test suite currently passes:

```text
15 passed
```

Example output:

```text
...............                        [100%]

15 passed, 2 warnings
```

The warnings are dependency deprecation warnings and do not represent failed tests.

---

# 20. Project Architecture

The project follows a layered structure:

```text
Client
   |
   v
API Routers
   |
   v
Authentication / Dependencies
   |
   v
Pydantic Schemas
   |
   v
Service Layer
   |
   v
Data Store
```

### API Layer

Handles HTTP requests, responses, status codes, and routing.

### Dependencies

Handles authentication and access-related dependencies.

### Schemas

Defines request and response structures using Pydantic.

### Service Layer

Contains application logic for users and tasks.

### Core

Contains configuration, security, and error-related functionality.

### Data Layer

Contains the current in-memory data store.

### Tests

Contains automated API tests.

---

# 21. Data Storage

The current project uses an in-memory Python dictionary for storing users and tasks.

Example:

```python
users = {}
tasks = {}
```

Because the application currently uses in-memory storage, data will be lost when the server restarts.

A future version can replace this with a persistent database such as:

* SQLite
* PostgreSQL
* MySQL

---

# 22. Complete Startup Process

### Step 1: Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure `.env`

Add the required JWT configuration.

### Step 4: Start the server

```bash
uvicorn app.main:app --reload
```

### Step 5: Open Swagger

```text
http://127.0.0.1:8000/docs
```

### Step 6: Run tests

```bash
pytest -q
```

---


# Author
Mayank Joshi
FastAPI Secure Task Manager Training Project
