# Secure Task Manager API

A FastAPI-based Task Management API developed in two stages:

- **Day 6:** Built the secure API using in-memory Python dictionaries, JWT authentication, Argon2 password hashing, role-based authorization, task ownership, validation, filtering, sorting, pagination, and automated testing.
- **Day 7:** Extended the same application by replacing production in-memory storage with PostgreSQL, adding async SQLAlchemy and Alembic migrations, task history and transaction handling, database indexes, Redis caching, and DB-backed automated tests.

The Day 7 implementation keeps the security and API concepts introduced in Day 6 while moving the data layer to persistent storage.

---

## 1. Day 6 → Day 7 Evolution

### Day 6: In-Memory Version

The first version used Python dictionaries for application storage:

```python
users = {}
tasks = {}
```

The application logic operated directly on those dictionaries.

This was useful for learning:

- FastAPI routing
- JWT authentication
- Password hashing
- Role-based authorization
- Task ownership
- Pydantic validation
- Search and filtering
- Sorting
- Pagination
- HTTP error handling
- Automated API testing

However, in-memory data is temporary and is lost when the process restarts.

### Day 7: Persistent + Cached Version

Day 7 extends the same API instead of creating a completely separate application.

The data layer was changed to:

```text
FastAPI
   |
   v
Service Layer
   |
   v
Repository Layer
   |
   +------> PostgreSQL
   |
   +------> Redis Cache
```

PostgreSQL is now the primary source of truth.

Redis is used as a performance cache for the default task-list response.

---

# 2. Features

## Authentication

- User registration
- User login
- JWT Bearer authentication
- Current-user endpoint
- Token expiry
- Argon2 password hashing
- Failed-login protection
- Active-user validation
- Duplicate username protection
- Duplicate email protection
- Public admin-registration protection

## Authorization

- User and admin roles
- Task ownership
- Normal users can access their own tasks
- Admins can access tasks belonging to other users
- Cross-user update/delete protection

## Task Management

- Create task
- Retrieve task
- List tasks
- Update task
- Delete task
- Task priorities
- Task statuses
- Search
- Priority filtering
- Status filtering
- Database-backed pagination

Supported task statuses:

```text
pending
in_progress
completed
```

Supported priorities:

```text
low
medium
high
```

## Database

- PostgreSQL
- Async SQLAlchemy
- AsyncSession
- Foreign keys
- ORM relationships
- Repository pattern
- Service layer
- Alembic migrations
- Transaction rollback
- Task status history
- Database indexes

## Redis

- Async Redis client
- Per-user task cache
- Cache key:

```text
tasks:user:{user_id}
```

- Cache TTL:

```text
300 seconds
```

- Cache HIT/MISS behavior
- Cache invalidation after task creation
- Cache invalidation after task update
- Cache invalidation after task deletion

## Testing

- pytest
- pytest-asyncio
- HTTPX async client
- Separate PostgreSQL test database
- Redis test cleanup
- 22 automated tests

---

# 3. Technology Stack

| Technology | Purpose |
|---|---|
| FastAPI | API framework |
| PostgreSQL | Persistent primary database |
| SQLAlchemy 2.x | Async ORM/database access |
| asyncpg | Async PostgreSQL driver |
| Alembic | Database schema migrations |
| Redis / Memurai | Caching |
| Pydantic | Request/response validation |
| Argon2 | Password hashing |
| JWT | Authentication |
| pytest | Automated testing |
| pytest-asyncio | Async test support |
| HTTPX | Async API testing |
| Uvicorn | ASGI server |

---

# 4. Project Structure

```text
fastapi_secure_task_manager/
│
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   │
│   ├── cache/
│   │   ├── __init__.py
│   │   └── redis.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   └── security.py
│   │
│   ├── data/
│   │   └── ...
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── database.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── roles.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── task_history.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   ├── task_repository.py
│   │   └── task_history_repository.py
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
│   │   ├── task_service.py
│   │   └── task_cache.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   │   ├── 931a8be4790e_create_task_tables.py
│   │   └── 61ab968bd13c_add_last_login_timestamp.py
│   └── env.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
│
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── pytest.ini
├── readme.md
└── requirements.txt
```

> The old Day 6 in-memory data layer is retained only as part of the project's development history. Day 7 application behavior uses PostgreSQL for persistent data.

---

# 5. Project Setup

Move into the project directory:

```bash
cd fastapi_secure_task_manager
```

---

# 6. Virtual Environment

Create the virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

The terminal should show:

```text
(venv)
```

---

# 7. Install Dependencies

Install the project dependencies:

```bash
pip install -r requirements.txt
```

The project uses the async PostgreSQL and Redis packages required for Day 7.

---

# 8. Environment Configuration

Create a `.env` file in the project root.

Do not commit the real `.env` file.

Example development configuration:

```env
APP_NAME=task-management-api
APP_ENV=local
DEBUG=true

DATABASE_URL=postgresql+asyncpg://postgres:<password>@localhost:5432/task_db

REDIS_URL=redis://localhost:6379/0
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
CACHE_TTL_SECONDS=300

LOG_LEVEL=INFO

JWT_SECRET_KEY=<your-long-random-secret>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

PASSWORD_HASH_SCHEME=argon2
MAX_LOGIN_ATTEMPTS=5
```

Use `.env.example` as the safe template.

The example file must contain placeholders, not real credentials.

---

# 9. PostgreSQL Setup

PostgreSQL is the primary persistent datastore for Day 7.

The default local configuration used by the project is:

```text
Host: localhost
Port: 5432
Database: task_db
```

A separate database is used for automated tests:

```text
task_test_db
```

The application uses async SQLAlchemy with:

```text
postgresql+asyncpg://...
```

---

# 10. Alembic Migrations

The project uses Alembic for database schema management.

Initial migration:

```text
931a8be4790e_create_task_tables.py
```

Second migration:

```text
61ab968bd13c_add_last_login_timestamp.py
```

The second migration adds:

```text
users.last_login_at
```

## Apply migrations

```powershell
alembic upgrade head
```

## Check current migration

```powershell
alembic current
```

## View migration history

```powershell
alembic history
```

## Demonstrate downgrade

```powershell
alembic downgrade -1
```

## Upgrade again

```powershell
alembic upgrade head
```

## Verify migration consistency

```powershell
alembic check
```

The final migration state should be the current head.

---

# 11. Database Models

## Users

The `users` table stores:

```text
id
username
email
password_hash
role
is_active
created_at
last_login_at
```

The email is unique.

The password hash is never returned by the API.

## Tasks

The `tasks` table stores:

```text
id
user_id
title
description
priority
status
created_at
updated_at
```

Each task belongs to one user.

## Task History

The `task_history` table stores:

```text
id
task_id
changed_by
old_status
new_status
changed_at
```

The history records status changes made to tasks.

---

# 12. Database Relationships

```text
User
 |
 | 1
 |
 |------< many
 |
Task
 |
 | 1
 |
 |------< many
 |
TaskHistory
```

A user can have multiple tasks.

A task can have multiple history records.

---

# 13. Repository / Service Architecture

Day 6 contained business logic directly around the in-memory dictionaries.

Day 7 introduces a repository/service structure.

```text
API Router
    |
    v
Service Layer
    |
    v
Repository Layer
    |
    v
PostgreSQL
```

## Repository Layer

Repositories handle database operations such as:

- Select
- Insert
- Update
- Delete
- Count
- Pagination queries

Examples:

```text
UserRepository
TaskRepository
TaskHistoryRepository
```

## Service Layer

Services handle business rules such as:

- Authentication
- Authorization
- Ownership checks
- Task operations
- Status history
- Transaction management
- Cache invalidation

The service layer controls transaction boundaries.

---

# 14. API Endpoints

## Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Register a normal user | No |
| POST | `/api/v1/auth/login` | Login and receive JWT | No |
| GET | `/api/v1/auth/me` | Get current user | Yes |

## Tasks

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/v1/tasks` | Create a task | Yes |
| GET | `/api/v1/tasks` | List tasks | Yes |
| GET | `/api/v1/tasks/{task_id}` | Get a task | Yes |
| PUT | `/api/v1/tasks/{task_id}` | Update a task | Yes |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task | Yes |

---

# 15. Authentication

The API uses JWT Bearer authentication.

After successful login, the API returns:

```json
{
  "access_token": "your-jwt-token",
  "token_type": "bearer",
  "expires_in": 1800
}
```

Protected requests use:

```text
Authorization: Bearer <access_token>
```

Swagger UI can be used to provide the bearer token with the **Authorize** button.

---

# 16. Password Security

Passwords are hashed using Argon2 before being stored.

Conceptually:

```text
Plain Password
      |
      v
 Argon2 Hash
      |
      v
PostgreSQL
```

The API response does not expose:

```text
password_hash
```

---

# 17. Authorization Rules

The API supports:

```text
user
admin
```

| Action | Normal User | Admin |
|---|---|---|
| Create task | Yes | Yes |
| View own tasks | Yes | Yes |
| View another user's tasks | No | Yes |
| Update own task | Yes | Yes |
| Update another user's task | No | Yes |
| Delete own task | Yes | Yes |
| Delete another user's task | No | Yes |

Each task contains a `user_id` that identifies its owner.

---

# 18. Public Admin Registration Protection

Day 6 allowed the role to be supplied during registration.

Day 7 removes that public privilege-escalation path.

Public registration creates a normal user.

An attempted registration containing:

```json
{
  "username": "attacker",
  "email": "attacker@example.com",
  "password": "password123",
  "role": "admin"
}
```

is rejected by request validation.

Admin accounts should be created through a controlled administrative process rather than by an unrestricted public registration field.

---

# 19. Task Creation

Example request:

```http
POST /api/v1/tasks
```

```json
{
  "title": "Learn FastAPI",
  "description": "Complete Task CRUD",
  "priority": "high",
  "status": "pending"
}
```

Example response:

```json
{
  "id": 1,
  "user_id": 1,
  "title": "Learn FastAPI",
  "description": "Complete Task CRUD",
  "priority": "high",
  "status": "pending",
  "created_at": "2026-10-01T05:34:58.604955Z",
  "updated_at": "2026-10-01T05:34:58.604955Z"
}
```

---

# 20. Task Search and Filtering

The task-list endpoint supports database-backed filtering/searching.

## Search

```text
GET /api/v1/tasks?search=python
```

Search can check task title and description.

## Priority

```text
GET /api/v1/tasks?priority=high
```

Supported values:

```text
low
medium
high
```

## Status

```text
GET /api/v1/tasks?status=completed
```

Supported values:

```text
pending
in_progress
completed
```

---

# 21. Pagination

Day 6 used application-side slicing of the in-memory task list.

Day 7 performs pagination at the database query level.

Example:

```text
GET /api/v1/tasks?page=2&page_size=10
```

Response:

```json
{
  "items": [],
  "page": 2,
  "page_size": 10,
  "total": 15
}
```

Calculation:

```text
offset = (page - 1) * page_size
```

The repository uses database `LIMIT` and `OFFSET` instead of loading the entire task dataset into Python first.

---

# 22. Task Status History

When a task's status changes, a record is added to `task_history`.

Example:

```text
Old status:
pending

New status:
completed
```

Stored as:

```text
old_status = pending
new_status = completed
```

This provides an audit trail of task status changes.

---

# 23. Transactions and Rollback

The task status change and task-history insertion occur in the same database transaction.

```text
Task Update
     +
History Insert
     |
     v
   COMMIT
```

If the history operation fails:

```text
Task Update
     +
History Insert
     |
     v
  Database Error
     |
     v
  ROLLBACK
```

The transaction rollback test deliberately creates an invalid foreign-key condition and verifies that:

- The task status remains unchanged
- The failed history record is not committed

This prevents partial updates.

---

# 24. Database Indexing

The project uses several meaningful indexes.

## `tasks.user_id`

Used frequently when retrieving tasks belonging to a user.

```sql
WHERE tasks.user_id = ?
```

## `tasks.status`

Useful for status filtering.

```sql
WHERE tasks.status = ?
```

## `task_history.task_id`

Useful when retrieving history for a particular task.

## `users.username`

The username is unique and frequently used during login.

## `users.email`

The email is unique, and PostgreSQL maintains the corresponding unique index.

## Index trade-offs

Indexes can improve read performance, but they also have costs:

- Additional storage
- Index maintenance during inserts
- Index maintenance during updates
- Index maintenance during deletes

For that reason, indexing every column is unnecessary. Indexes should target columns that are frequently searched, filtered, joined, or constrained for uniqueness.

---

# 25. Redis Caching

Day 7 adds Redis as a cache on top of PostgreSQL.

PostgreSQL remains the source of truth.

## Cache Key

```text
tasks:user:{user_id}
```

Example:

```text
tasks:user:2
```

## TTL

```text
300 seconds
```

Configured by:

```env
CACHE_TTL_SECONDS=300
```

## Cache flow

```text
GET /api/v1/tasks
          |
          v
     Redis GET
       /     \
    HIT       MISS
     |          |
     |          v
     |      PostgreSQL
     |          |
     |          v
     |       Redis SET
     |          |
     +----------+
           |
           v
        Response
```

## Cacheable request

The required single user key is used for the default task-list request:

```text
page = 1
page_size = 10
search = empty
priority = empty
status = empty
```

Different filters/pages are not stored under the same key because they represent different datasets.

## Cache invalidation

After a successful mutation:

```text
POST /api/v1/tasks
    -> invalidate tasks:user:{user_id}

PUT /api/v1/tasks/{task_id}
    -> invalidate owner cache

DELETE /api/v1/tasks/{task_id}
    -> invalidate owner cache
```

The database change is committed before invalidation.

---

# 26. Windows Redis Setup

For local Windows development, the project uses Memurai as the Redis-compatible server.

Verify the server:

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" ping
```

Expected:

```text
PONG
```

The Python Redis client is used by the FastAPI application.

---

# 27. Redis Verification

A cache key can be inspected directly:

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" GET tasks:user:2
```

Check the expiration:

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" TTL tasks:user:2
```

The TTL starts near:

```text
300
```

and decreases toward zero as time passes.

A deleted/non-existent key reports:

```text
-2
```

from `TTL`.

---

# 28. Request Validation

Pydantic schemas validate incoming data.

Examples of rejected requests include:

- Invalid email
- Short password
- Invalid priority
- Invalid status
- Missing required fields
- Invalid task title
- Invalid pagination values
- Unexpected registration fields such as a public `role`

Validation errors return:

```text
422 Unprocessable Entity
```

---

# 29. HTTP Status Codes

| Status Code | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Resource deleted successfully |
| 401 | Authentication required or invalid credentials |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict, such as duplicate username/email |
| 422 | Validation error |
| 429 | Too many failed login attempts / temporary block |

---

# 30. API Documentation

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API normally runs at:

```text
http://127.0.0.1:8000
```

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger can be used to test the API interactively.

---

# 31. Automated Testing

The project uses:

```text
pytest
pytest-asyncio
HTTPX
```

Tests use:

- a separate PostgreSQL database
- async API requests
- Redis cleanup between tests
- database cleanup between tests

Test configuration is stored in:

```text
pytest.ini
```

Run the complete test suite:

```powershell
pytest -q
```

Expected result:

```text
22 passed
```

---

# 32. Automated Test Cases

The final suite contains 22 tests.

## Authentication

1. Register a user successfully
2. Duplicate username fails
3. Duplicate email fails
4. Invalid email fails
5. Login returns JWT
6. Current-user endpoint works

## Task CRUD

7. Create task
8. Retrieve task
9. Update task
10. Delete task

## Authorization

11. User cannot access another user's task
12. Admin can access another user's task

## Database behavior

13. Task history is created after status change
14. Database-backed pagination
15. Invalid foreign key is rejected
16. Transaction rollback works

## Security regression

17. Public registration cannot create an admin

## Redis

18. Task cache is created
19. Task cache HIT works
20. CREATE invalidates task cache
21. UPDATE invalidates task cache
22. DELETE invalidates task cache

Final test result:

```text
22 passed
```

---

# 33. Test Database

Automated tests use a separate PostgreSQL database:

```text
task_test_db
```

This keeps test data separate from:

```text
task_db
```

Set the test database for the current PowerShell session:

```powershell
$env:TEST_DATABASE_URL="postgresql+asyncpg://postgres:<password>@localhost:5432/task_test_db"
```

Then run:

```powershell
pytest -q
```

Do not use the production/development database for automated test cleanup.

---

# 34. Day 6 Architecture vs Day 7 Architecture

### Day 6

```text
Client
  |
  v
FastAPI Router
  |
  v
Dependencies / Auth
  |
  v
Service Layer
  |
  v
In-Memory Dictionaries
```

Example:

```python
users = {}
tasks = {}
```

### Day 7

```text
Client
  |
  v
FastAPI Router
  |
  v
Dependencies / Auth
  |
  v
Service Layer
  |
  +---------> Redis Cache
  |
  v
Repository Layer
  |
  v
PostgreSQL
```

The application therefore keeps the original API/security concepts while replacing temporary storage with a persistent database and adding caching.

---

# 35. Useful Commands

## Start application

```powershell
uvicorn app.main:app --reload
```

## Run tests

```powershell
pytest -q
```

## Check migrations

```powershell
alembic current
```

```powershell
alembic history
```

```powershell
alembic check
```

## Check Redis

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" ping
```

## Inspect cache

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" GET tasks:user:2
```

## Inspect cache TTL

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" TTL tasks:user:2
```

---

# 36. Final Day 7 Status

```text
✅ PostgreSQL
✅ Async SQLAlchemy / AsyncSession
✅ Database models and relationships
✅ Alembic initial migration
✅ Second migration
✅ Upgrade / downgrade / upgrade demonstration
✅ Repository/service architecture
✅ CRUD
✅ Authorization and ownership
✅ Task status history
✅ Transaction rollback
✅ Database pagination
✅ Meaningful indexes
✅ Redis connection
✅ Redis cache creation
✅ Redis cache HIT
✅ Redis invalidation after CREATE
✅ Redis invalidation after UPDATE
✅ Redis invalidation after DELETE
✅ Public admin-registration protection
✅ 22 automated tests
```

---

# 37. Complete Startup Process

### Step 1 — Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 2 — Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 3 — Configure `.env`

Add the local PostgreSQL, Redis, JWT, and application configuration.

### Step 4 — Start PostgreSQL

Make sure PostgreSQL is running and the `task_db` database is available.

### Step 5 — Apply migrations

```powershell
alembic upgrade head
```

### Step 6 — Start Memurai

Verify:

```powershell
& "C:\Program Files\Memurai\memurai-cli.exe" ping
```

Expected:

```text
PONG
```

### Step 7 — Start FastAPI

```powershell
uvicorn app.main:app --reload
```

### Step 8 — Open Swagger

```text
http://127.0.0.1:8000/docs
```

### Step 9 — Run tests

Configure the test database:

```powershell
$env:TEST_DATABASE_URL="postgresql+asyncpg://postgres:<password>@localhost:5432/task_test_db"
```

Run:

```powershell
pytest -q
```

Expected:

```text
22 passed
```

---

# 38. Author

**Mayank Joshi**

FastAPI Secure Task Manager Training Project
