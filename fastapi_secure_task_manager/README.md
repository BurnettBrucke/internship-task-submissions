# Secure Task Management API

A secure REST API built with **FastAPI** for managing users and tasks.

This project was developed as part of **Day 6 FastAPI Training** and focuses on authentication, JWT authorization, role-based access control, task ownership, validation, error handling, and automated testing.

---

## 📌 Features

- User registration
- User login with JWT authentication
- Password hashing
- Current user information
- Role-based access control
- `user` and `admin` roles
- Task CRUD operations
- Task ownership protection
- Admin access to other users' tasks
- Failed login protection
- Request validation
- Custom error responses
- Protected API endpoints
- Swagger/OpenAPI documentation
- Automated tests using Pytest
- In-memory data storage

---

## 🛠️ Technologies Used

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Python-JOSE
- Passlib / bcrypt
- Pytest
- HTTPX
- Swagger / OpenAPI

---

## 📂 Project Structure

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
│   │   ├── login_security.py
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
├── requirements.txt
└── README.md




🔐 Authentication

The API uses JWT (JSON Web Token) authentication.

Authentication Flow
Register
   ↓
Login
   ↓
Validate username/password
   ↓
Generate JWT
   ↓
Send JWT to client
   ↓
Client sends JWT with protected requests
   ↓
Token is decoded and user is identified

JWT contains:

User ID
Username
User role
Expiration time

Passwords are never stored as plain text. A password hash is stored instead.

👥 User Roles

The API supports two roles:

Role	Access
user	Can access and manage their own tasks
admin	Can access and manage tasks belonging to other users
Example

If User A owns Task 1:

User A → Can access Task 1
User B → Cannot access Task 1
Admin → Can access Task 1
🔑 Authentication Endpoints
Register
POST /api/v1/auth/register

Example request:

{
  "username": "john",
  "email": "john@example.com",
  "password": "StrongPass@123",
  "role": "user"
}

Successful response:

201 Created
Login
POST /api/v1/auth/login

Example request:

{
  "username": "john",
  "password": "StrongPass@123"
}

Example response:

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "expires_in": 1800
}
Get Current User
GET /api/v1/auth/me

Requires:

Authorization: Bearer <access_token>
📝 Task Endpoints

All task endpoints require authentication.

Method	Endpoint	Description
POST	/api/v1/tasks	Create a task
GET	/api/v1/tasks	Get accessible tasks
GET	/api/v1/tasks/{task_id}	Get a specific task
PUT	/api/v1/tasks/{task_id}	Update a task
DELETE	/api/v1/tasks/{task_id}	Delete a task
Create Task
POST /api/v1/tasks

Example:

{
  "title": "Complete FastAPI Task",
  "description": "Finish Day 6 assignment",
  "priority": "high",
  "completed": false
}

The owner_id is automatically assigned from the authenticated user.

Get Tasks
GET /api/v1/tasks

Normal users receive their own tasks.

Admins can access tasks belonging to all users.

Get Task
GET /api/v1/tasks/{task_id}

Example:

GET /api/v1/tasks/1

Users can access their own tasks.

Admins can access any task.

Update Task
PUT /api/v1/tasks/{task_id}

Example:

{
  "title": "Updated FastAPI Task",
  "priority": "medium",
  "completed": true
}

The API checks task ownership before allowing a normal user to update the task.

Delete Task
DELETE /api/v1/tasks/{task_id}

Successful deletion returns:

204 No Content
🛡️ Failed Login Protection

The API includes protection against repeated failed login attempts.

Configuration:

Maximum failed attempts: 5
Lockout duration: 10 minutes

After repeated failed login attempts, the account is temporarily locked.

Successful login resets the failed-attempt counter.

⚠️ Error Handling

The API uses a consistent error format.

Example:

{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task does not exist."
  }
}
Common Errors
Status	Error	Description
401	AUTHENTICATION_REQUIRED	Token is missing
401	INVALID_TOKEN	Token is invalid or expired
401	INVALID_CREDENTIALS	Login credentials are incorrect
403	FORBIDDEN	User does not have permission
404	TASK_NOT_FOUND	Task does not exist
409	USERNAME_ALREADY_EXISTS	Username already exists
422	VALIDATION_ERROR	Request validation failed
✅ Validation

Pydantic schemas are used to validate incoming requests.

Examples of validation include:

Valid email format
Password requirements
Valid task priority
Valid task fields
Correct data types

Invalid requests return:

422 Unprocessable Entity

with the standard error response.

🧪 Testing

Automated tests are implemented using Pytest and FastAPI's TestClient.

Run all tests:

pytest -v
Current Test Result
15 passed, 1 warning
Authentication Tests
Register new user
Duplicate username
Valid login
Invalid login
Access /me without token
Invalid email
Weak password
Access /me with valid token
Task Tests
User creates task
User views own tasks
User cannot update another user's task
Admin can view another user's task
Admin can delete another user's task
Invalid task priority
Unknown task ID
📖 API Documentation

FastAPI automatically generates Swagger documentation.

Start the development server:

uvicorn app.main:app --reload

Open Swagger:

http://127.0.0.1:8000/docs

Alternative ReDoc documentation:

http://127.0.0.1:8000/redoc
⚙️ Installation
1. Clone the repository
git clone <repository-url>
2. Navigate to the project
cd fastapi_secure_task_manager
3. Create virtual environment
python -m venv venv
4. Activate virtual environment
Windows
venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
▶️ Running the Application

Start the FastAPI server:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Health check:

GET /health

Response:

{
  "status": "healthy"
}
💾 Data Storage

This project currently uses an in-memory data store.

Users and tasks are stored in Python lists:

users = []
tasks = []

Because the data is stored in memory:

Data is available while the application is running.
Restarting the server clears users and tasks.
No permanent database is currently used.

This implementation keeps the project focused on FastAPI, authentication, authorization, service-layer logic, and API design.