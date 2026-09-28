# FastAPI Secure Task Manager

A secure Task Management REST API built using FastAPI.

This project demonstrates:

- User registration and login
- Password hashing using Argon2
- JWT-based authentication
- Role-based authorization
- Task CRUD operations
- Task ownership
- Pydantic validation
- Environment-based configuration
- Login attempt protection
- Automated testing
- Swagger/OpenAPI documentation

---

## Project Structure

fastapi_secure_task_manager/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   └── tasks.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── errors.py
│   │
│   ├── data/
│   │   └── store.py
│   │
│   ├── dependencies/
│   │   └── auth.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── task.py
│   │
│   └── services/
│       ├── auth_service.py
│       └── task_service.py
│
├── tests/
│   ├── test_auth.py
│   └── test_tasks.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

---

## Technologies Used

- Python
- FastAPI
- Pydantic
- Pydantic Settings
- JWT
- Argon2 password hashing
- Uvicorn
- Pytest
- HTTPX
- python-dotenv

---

## Setup

### 1. Clone the repository
git clone <repository-url>

**Navigate into the project:** cd fastapi_secure_task_manager

### 2. Create a virtual environment
python -m venv venv

### 3. Activate the virtual environment

**For PowerShell:** .\venv\Scripts\Activate.ps1

**If PowerShell execution policy blocks activation:** Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\venv\Scripts\Activate.ps1

### 4. Install dependencies
pip install -r requirements.txt

---

## Environment Configuration

Create a .env file in the project root.

Use .env.example as a template.

**Example:**

APP_NAME=fastapi_secure_task_manager
APP_ENV=local
DEBUG=true

JWT_SECRET_KEY=change_me
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

PASSWORD_HASH_SCHEME=argon2
MAX_LOGIN_ATTEMPTS=5
LOG_LEVEL=INFO

**Important**
Do not commit the real .env file.

**Never expose:**

- JWT secret
- Passwords
- Access tokens
- Other sensitive configuration

---

## Run the Application

**Start the FastAPI server:** uvicorn app.main:app --reload

The application will run locally.

---

## API Documentation

**Swagger UI:** /docs

**ReDoc:** /redoc

The API documentation provides interactive testing for authentication and task endpoints.
Swagger UI supports Bearer token authentication for protected endpoints.

---

## API Endpoints

### Health Check

#### GET
*/health*

**Returns:**

{
  "status": "ok"
}

---

## Authentication

### Register User

#### POST

*/api/v1/auth/register*

**Example request:**

{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "TestUser@123",
  "role": "user"
}

Successful response does not expose the password or password hash.
Protected endpoints require a valid JWT Bearer token.

---

### Login

### POST

*/api/v1/auth/login*

**Example request:**

{
  "username": "testuser",
  "password": "TestUser@123"
}

**Example response:**

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "expires_in": 1800
}

Use the access token as a Bearer token for protected endpoints.

---

### Current User

#### GET

*/api/v1/auth/me*

**Requires:**

Authorization: Bearer <access_token>

**Returns the authenticated user's:**

- username
- email
- role

---

## Task APIs

All task endpoints require authentication.

### Create Task

#### POST
*/api/v1/tasks*

**Example:**

{
  "title": "Learn FastAPI",
  "description": "Study authentication and security",
  "priority": "high",
  "completed": false
}

### List Tasks

#### GET
*/api/v1/tasks*

- Normal users receive their own tasks.
- Admins can access all tasks.

### Get Task

#### GET
*/api/v1/tasks/{task_id}*

- Users can access their own tasks.
- Admins can access all tasks.

### Update Task

#### PUT
*/api/v1/tasks/{task_id}*

**Example:**

{
  "title": "Updated Task",
  "completed": true
}

### Delete Task

#### DELETE
*/api/v1/tasks/{task_id}*

---

## Authorization

The API supports two roles:

### User

**A normal user can:**

- Create tasks
- View own tasks
- Update own tasks
- Delete own tasks

A user cannot access another user's task.

### Admin

**An admin can:**

- Access all tasks
- Access tasks belonging to other users

Authorization is enforced on the backend.

---

## Validation

Pydantic validation is used for request data.

**Examples:**

- Username length validation
- Email validation
- Password minimum length
- Task title validation
- Task priority validation
- Task completion boolean validation

**Invalid request data returns:** 422 Unprocessable Entity

---

## Authentication and Security

**The project uses:**

- Argon2 password hashing
- JWT access tokens
- Token expiration
- Role-based authorization
- Environment-based configuration
- Protected API endpoints
- Login attempt protection

Passwords are never stored as plain text.

The JWT contains user identity, role and expiration information.

---

## Error Status Codes

| Status Code | Meaning                         |
| ----------- | ------------------------------- |
| 200         | Successful request              |
| 201         | Resource created                |
| 204         | Resource deleted                |
| 401         | Authentication required/invalid |
| 403         | Permission denied               |
| 404         | Resource not found              |
| 409         | Duplicate/conflict              |
| 422         | Validation error                |

---

## Login Attempt Protection

The application supports failed login attempt tracking.

**The maximum number of failed attempts is configured through:** MAX_LOGIN_ATTEMPTS=5

After reaching the configured limit, further login attempts are blocked.

A successful login resets the failed-attempt counter.

---

## Running Tests

**Run all automated tests:** pytest -q

**Current test suite:** 24 passed

### The tests cover:

- User registration
- Duplicate username
- Email validation
- Password validation
- Successful login
- Invalid login
- Authentication protection
- Current user endpoint
- Task creation
- Task listing
- Task retrieval
- Task update
- Task deletion
- Task ownership
- Admin authorization
- Task validation
- Login attempt protection
- Security Notes
- User cannot update another user's task
- Admin can delete another user's task
- Invalid JWT token

### Security Notes

**Do not commit the following to Git**:

- .env
- Passwords
- JWT secrets
- Access tokens

The .env.example file can be committed because it contains placeholder configuration only.

---

## Project Status

Day 6 FastAPI Secure Task Manager implementation includes:

- FastAPI project structure
- Authentication
- JWT authorization
- Argon2 password hashing
- User/admin roles
- Task CRUD
- Task ownership
- Validation
- Error handling
- Login attempt protection
- Automated tests
- Swagger/OpenAPI documentation