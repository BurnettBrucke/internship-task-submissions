# FastAPI Secure Task Manager

A secure Task Management REST API built using FastAPI.

This project demonstrates:

- User registration and login
- Password hashing using Argon2
- JWT-based authentication
- Role-based authorization
- Task CRUD operations
- Task ownership
- PostgreSQL database integration
- Async SQLAlchemy
- Alembic database migrations
- Repository and service layer architecture
- Task status history
- Database transactions and rollback
- Pagination
- Database indexing
- Redis caching
- Cache invalidation
- Pydantic validation
- Environment-based configuration
- Login attempt protection
- Automated testing
- Swagger/OpenAPI documentation

---

## Project Structure

fastapi_secure_task_manager/
│
├── alembic/
│   ├── versions/
│   │   ├── 6bf9dbd6db39_create_task_tables.py
│   │   └── b03166270966_add_last_login_timestamp.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
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
│   │   ├── redis.py
│   │   └── security.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   └── store.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── task.py
│   │   ├── task_history.py
│   │   └── user.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── task_repository.py
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
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── README.md
└── requirements.txt

---

## Architecture

The application follows a layered architecture:

API Router
    ↓
Service Layer
    ↓
Repository Layer
    ↓
PostgreSQL

Redis is used as a caching layer for task list responses.

---

## Technologies Used

- Python
- FastAPI
- Pydantic
- Pydantic Settings
- PostgreSQL
- SQLAlchemy
- Async SQLAlchemy
- asyncpg
- Alembic
- Redis
- redis-py
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

## PostgreSQL Configuration

The application uses PostgreSQL as the primary database.

**Create a PostgreSQL database named:** task_db

Database tables are created and managed through SQLAlchemy models and Alembic migrations.

Production/application data is not stored in in-memory task lists or dictionaries.

---

## Redis Configuration

The application uses Redis for caching task list responses.

**Redis should be running locally on:** localhost:6379

The application uses the Redis URL configured in .env.

Example:

REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300

---

## Environment Configuration

Create a .env file in the project root.

Use .env.example as a template.

**Example:**

APP_NAME=task-management-api
APP_ENV=local
DEBUG=true

DATABASE_URL=postgresql+asyncpg://postgres:change_me@localhost:5432/task_db
TEST_DATABASE_URL=postgresql+asyncpg://postgres:change_me@localhost:5432/task_test_db

REDIS_URL=redis://localhost:6379/0

DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
CACHE_TTL_SECONDS=300

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
- Database/User Passwords
- Access tokens
- Other sensitive configuration

---

## Database Migrations

Alembic is used to manage database schema changes.

### Create a Migration

alembic revision --autogenerate -m "create task tables"

### Apply Migrations

alembic upgrade head

### Roll Back One Migration

alembic downgrade -1

### Reapply the Migration

alembic upgrade head

Database schema changes should be managed through Alembic migrations rather than manually creating or modifying tables.

---

## Database Models

The application uses three main database tables.

### Users

The users table contains:

- id
- username
- email
- password_hash
- role
- is_active
- created_at
- last_login_at

### Tasks

The tasks table contains:

- id
- user_id
- title
- description
- priority
- status
- created_at
- updated_at

### Task History

The task_history table contains:

- id
- task_id
- changed_by
- old_status
- new_status
- changed_at

### Relationships

User
  │
  └── 1 ──────── Many ──── Task
                              │
                              └── 1 ──────── Many ──── TaskHistory

A user can have multiple tasks.

A task can have multiple status history records.

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

#### Pagination

The task list supports pagination:

/api/v1/tasks?page=1&page_size=10

**Example response:**

{
  "items": [],
  "page": 1,
  "page_size": 10,
  "total": 0
}

Pagination is performed at the database query level using LIMIT/OFFSET rather than loading all tasks into memory.

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

When the task status changes, a corresponding record is created in task_history.

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
- Pagination parameter validation

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

The JWT tokens contains user identity, role and expiration information.

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

## Repository and Service Layer

Database queries are separated from API route handlers.

The application follows:

API Router
     ↓
Service Layer
     ↓
Repository Layer
     ↓
PostgreSQL

### Repository Layer

The repository layer handles database operations such as:

- Creating tasks
- Retrieving tasks
- Updating tasks
- Deleting tasks
- Counting tasks
- Creating task history
- Retrieving 

### Service Layer

The service layer handles application/business logic such as:

- Task ownership
- Status conversion
- Task history creation
- Transactions
- Redis cache handling
- Cache invalidation

---

## Transactions and Task History

Task status changes and their corresponding history records are handled in the same database transaction.

**For example:**

Task Status Update
        +
Task History Insert
        ↓
   Same Transaction

If the history insertion fails, the task status update is rolled back.

This keeps the task data and task history consistent.

---

## Redis Caching

Redis is used to cache task list responses.

The application follows a cache-aside pattern.

### Cache Key

Task list cache keys follow this format:

tasks:user:{user_id}:page:{page}:size:{page_size}

**Example:**

tasks:user:1:page:1:size:10

### Cache TTL

The default cache TTL is:

300 seconds

### Cache Miss

GET /tasks
     ↓
Redis Cache
     ↓
Cache MISS
     ↓
PostgreSQL
     ↓
Store response in Redis
     ↓
Return response

### Cache Hit

GET /tasks
     ↓
Redis Cache
     ↓
Cache HIT
     ↓
Return cached response

### Cache Invalidation

The task cache is invalidated after:

- Task creation
- Task update
- Task deletion

This prevents stale task data from being returned.

---

## Database Indexing

The application uses indexes on frequently queried fields.

**Examples include:**

- users.email
- tasks.user_id
- tasks.status

Indexes improve lookup performance for commonly filtered columns.

Indexes also have storage and write/update overhead, so they are used for meaningful query patterns.

---

## Running Tests

The project uses Pytest for automated testing.

**Run all automated tests:** pytest -q

**Current test suite:** 31 passed

The tests use a separate PostgreSQL test database configured through:

TEST_DATABASE_URL=postgresql+asyncpg://postgres:change_me@localhost:5432/task_test_db

This keeps test data separate from the development database.

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
- Database/User Passwords
- JWT secrets
- Access tokens
- Other sensitive configuration

The .env.example file can be committed because it contains placeholder configuration only.

### Task Management

- Task creation
- Task listing
- Task retrieval
- Task update
- Task deletion
- Task ownership
- Admin authorization
- Task validation
- User cannot update another user's task
- Admin can delete another user's task

### PostgreSQL and Transactions

- Creating users and tasks in PostgreSQL
- Retrieving tasks from PostgreSQL
- Task updates
- Task deletion
- Task history creation
- Transaction rollback
- Invalid foreign key handling

### Pagination

- Correct page response
- Page size handling
- Total task count

### Redis

- Cache creation after task list request
- Cache hit
- Cache invalidation after create
- Cache invalidation after update
- Cache invalidation after delete

---

## Project Status

### Day 6 — FastAPI Secure Task Manager

**Completed:**

- FastAPI project structure
- User registration
- Login
- JWT authentication
- Argon2 password hashing
- User/admin roles
- Task CRUD
- Task ownership
- Pydantic validation
- Error handling
- Login attempt protection
- Swagger/OpenAPI documentation
- Automated testing

### Day 7 — PostgreSQL + Redis Integration

**Completed:**

- PostgreSQL database integration
- Async SQLAlchemy
- AsyncSession
- SQLAlchemy models
- User-Task relationship
- Task-TaskHistory relationship
- Alembic initial migration
- Alembic schema update migration
- Migration rollback and reapply
- Repository layer
- Service layer
- PostgreSQL-backed task CRUD
- Task status history
- Database transactions
- Transaction rollback handling
- Pagination
- Database indexes
- Redis integration
- Redis task caching
- Cache-aside pattern
- Cache invalidation
- Separate PostgreSQL test database
- Automated Day 7 tests
- Full test suite passing

---

## Definition of Done

The Day 7 implementation is complete when:

- Day 6 authentication and authorization continue to work
- Task data persists in PostgreSQL
- Alembic manages database schema changes
- Task history is stored in PostgreSQL
- Transactions and rollback work correctly
- Pagination is implemented
- Meaningful database indexes are present
- Redis caching works
- Redis cache invalidation works after task changes
- Automated tests pass

**Current result:**

30 passed

---