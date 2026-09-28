# 1.FastAPI Secure Task Manager

A secure Task Manager API built with FastAPI, JWT authentication, role-based authorization, password hashing, validation, and automated tests.

## 2.Features

- User registration and login
- JWT-based authentication
- Bearer token authentication
- User and Admin roles
- Password hashing using Argon2
- Task CRUD operations
- Task ownership and authorization
- Admin access to all tasks
- Request validation
- Consistent error responses
- Failed login attempt protection
- Temporary login blocking after 5 failed attempts
- Swagger API documentation
- Automated tests

### 3. Project Structure

```text
fastapi_secure_task_manager/
│
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   └── tasks.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── errors.py
│   │   └── security.py
│   │
│   ├── data/
│   │   └── store.py
│   │
│   ├── dependencies/
│   │   └── auth.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── task_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_auth.py
│   └── test_tasks.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md

### 4.Installation

Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate

### 5. Install dependencies:

pip install -r requirements.txt
Environment Configuration

Create a .env file in the project root.

Example:

APP_NAME=fastapi_secure_task_manager
APP_ENV=local
DEBUG=true
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
PASSWORD_HASH_SCHEME=argon2
MAX_LOGIN_ATTEMPTS=5
LOG_LEVEL=INFO

### 6.Run the Application

Start the FastAPI development server:

uvicorn app.main:app --reload

### 7.Application:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
Authentication APIs
Register
POST /api/v1/auth/register

Creates a new user.

Login
POST /api/v1/auth/login

Returns a JWT access token.

Current User
GET /api/v1/auth/me

### 8.Requires:

Authorization: Bearer <access_token>
Task APIs
Create Task
POST /api/v1/tasks
Get Tasks
GET /api/v1/tasks

Normal users can view their own tasks. Admins can view all tasks.

Get Task
GET /api/v1/tasks/{task_id}
Update Task
PUT /api/v1/tasks/{task_id}
Delete Task
DELETE /api/v1/tasks/{task_id}
Authorization

The API supports two roles:

User
Create own tasks
View own tasks
Update own tasks
Delete own tasks
Cannot access other users' tasks
Admin
Access all tasks
Create, view, update, and delete tasks

Authorization is enforced on the backend.

### 9.Security
Passwords are never stored as plain text.
Passwords are hashed using Argon2.
JWT tokens contain user identity, role, and expiry.
JWT secret is loaded from environment variables.
Passwords and tokens are not logged.
Missing or invalid authentication returns 401.
Authenticated users without permission receive 403.
Failed login attempts are tracked in memory.
After 5 failed attempts, login is temporarily blocked for 5 minutes.
Successful login resets failed login attempts.
Error Handling

The API uses a consistent error format:

{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task does not exist."
  }
}

Common responses:

401 - Authentication required or invalid credentials
403 - Permission denied
404 - Resource not found
409 - Duplicate username
422 - Validation error
429 - Too many failed login attempts
Testing

### 10.Run all automated tests:

pytest -v

Current test result:

15 passed

The test suite covers:

User registration
Duplicate username
Invalid email
Weak password
Login and JWT token
Wrong password
Current user endpoint
Protected endpoints
Task creation
Task listing
Task update
Task deletion
Task ownership
Admin task access
Invalid task priority