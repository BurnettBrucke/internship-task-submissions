# Day 8 - Final Microservices & Production Backend

A production-style backend training project built with FastAPI. The project demonstrates service-to-service communication, JWT authentication with database-backed users, internal bearer authentication, separate PostgreSQL databases, Redis/ARQ background processing, idempotency, correlation/request IDs, structured logging, OpenTelemetry tracing, Docker Compose, Alembic migrations, integration testing, and CI validation.

> Training scope: this is a standalone backend exercise. It does not implement real payment or Stripe business logic.

## Architecture

```text
                              Client
                                |
                                | HTTP + JWT
                                v
                     +-----------------------+
                     |    Gateway Service    |
                     |      FastAPI :8000    |
                     +-----------+-----------+
                                 |
             +-------------------+-------------------+
             |                                   |
             v                                   v
     +----------------+                 +----------------------+
     |   Gateway DB   |                 |  Processing Service  |
     |    user_db     |                 |     FastAPI :8001    |
     +-------+--------+                 +----------+-----------+
             |                                     |
             v                          +------------+-------------+
          users table                   |                          |
                                        v                          v
                                +---------------+            +-----------+
                                |    jobs_db    |            |   Redis   |
                                |  PostgreSQL   |            |  / ARQ    |
                                +-------+-------+            +-----+-----+
                                        |                          |
                                        |                          v
                                        |                   +-------------+
                                        |                   | ARQ Worker  |
                                        |                   | background  |
                                        +-------------------+-------------+
```

### Service responsibilities

**Gateway Service**
- Public API surface.
- User registration and login.
- Stores Gateway users in its own PostgreSQL database (`user_db`).
- Hashes passwords with Argon2 before storage.
- Creates JWT access tokens after database-backed authentication.
- Pydantic request validation.
- Generates or propagates request/correlation IDs.
- Calls Processing asynchronously with `httpx`.
- Applies downstream timeouts and safe GET retries.
- Maps downstream failures to public Gateway errors.
- Implements idempotency for job creation.
- Does not access the Processing `jobs_db` directly.

**Processing Service**
- Internal API surface.
- Validates the Gateway's bearer service token.
- Creates and persists jobs in `jobs_db`.
- Enqueues background work through Redis/ARQ.
- Exposes job status.
- Exposes health/readiness checks.
- Produces structured JSON logs.

**ARQ Worker**
- Runs outside the request/response path.
- Loads jobs from `jobs_db`.
- Moves jobs through `PROCESSING`, `COMPLETED`, and `FAILED` states.
- Continues OpenTelemetry trace context from the enqueue operation.

## Database Ownership

The project uses two logical PostgreSQL databases on the same PostgreSQL server:

```text
PostgreSQL
├── user_db
│   └── users
│
└── jobs_db
    └── jobs
```

There is no foreign-key relationship between `users` and `jobs`.

- Gateway owns `user_db`.
- Processing owns `jobs_db`.
- Gateway authentication queries only `user_db`.
- Processing job operations query only `jobs_db`.

This keeps service data ownership separated and prevents the Gateway from reading the Processing database directly.

## Request and Job Flow

### User authentication flow

```text
POST /api/v1/auth/register
        |
        v
Validate username/password
        |
        v
Check username in user_db
        |
        v
Hash password with Argon2
        |
        v
Save user
        |
        v
201 Created
```

```text
POST /api/v1/auth/login
        |
        v
Find username in user_db
        |
        v
Verify password against Argon2 hash
        |
        v
Create JWT
        |
        v
Return access token
```

### Job flow

```text
POST /api/v1/jobs
        |
        v
Gateway JWT authentication + validation
        |
        v
Idempotency-Key check/reservation (Redis)
        |
        v
Gateway -> Processing
        |
        v
Create job in jobs_db
        |
        v
CREATED -> QUEUED
        |
        v
ARQ enqueue in Redis
        |
        v
Worker picks job
        |
        v
PROCESSING
      /   \
     v     v
COMPLETED FAILED
```

## API Endpoints

### Gateway - public API

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Register a new user | Public |
| `POST` | `/api/v1/auth/login` | Obtain JWT access token using a database user | Public |
| `POST` | `/api/v1/jobs` | Create a job | Bearer JWT |
| `GET` | `/api/v1/jobs/{job_id}` | Get job status/details | Bearer JWT |
| `GET` | `/health` | Liveness check | Public |
| `GET` | `/ready` | Gateway dependency readiness | Public |

### Processing - internal API

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| `POST` | `/internal/v1/jobs` | Create/persist and enqueue a job | Internal bearer token |
| `GET` | `/internal/v1/jobs/{job_id}` | Read job status/details | Internal bearer token |
| `GET` | `/health` | Liveness check | Public |
| `GET` | `/ready` | PostgreSQL + Redis readiness | Public |

FastAPI also exposes interactive Swagger/OpenAPI documentation at `/docs` for both services when they are running.

- Gateway: `http://localhost:8000/docs`
- Processing: `http://localhost:8001/docs`

## Example Registration

```json
{
  "username": "mayankjsohi",
  "password": "mayank@234"
}
```

Successful registration returns:

```json
{
  "id": 1,
  "username": "mayankjsohi",
  "created_at": "2026-10-08T..."
}
```

The database stores the Argon2 password hash, never the plaintext password.

## Example Job Request

```json
{
  "name": "Generate monthly report",
  "job_type": "report",
  "priority": "high"
}
```

For create requests, the client can send:

```http
Idempotency-Key: client-job-1001
```

## Job States

```text
CREATED -> QUEUED -> PROCESSING -> COMPLETED
                               \
                                -> FAILED
```

## Authentication

### Gateway authentication

The Gateway uses database-backed authentication.

#### Registration

`POST /api/v1/auth/register`

1. Validate the request with Pydantic.
2. Check whether the username already exists.
3. Hash the password with Argon2.
4. Store the user in `user_db.users`.
5. Return the created user's ID, username, and timestamp.

Duplicate usernames return `409 Conflict`.

#### Login

`POST /api/v1/auth/login`

The Gateway:

1. Looks up the user by username in `user_db`.
2. Verifies the submitted password against the stored Argon2 hash.
3. Creates a JWT after successful verification.

The JWT contains:

- `sub` - database user ID
- `role` - user role
- `exp` - token expiration

The JWT secret, algorithm, and lifetime are configurable through environment variables.

### Gateway -> Processing authentication

The Gateway sends:

```http
Authorization: Bearer <PROCESSING_SERVICE_TOKEN>
```

Processing validates the shared internal service token before allowing internal job operations.

The real `.env` file must never be committed. Only `.env.example` belongs in source control.

## Timeout, Retry, and Error Handling

Gateway -> Processing communication uses an asynchronous `httpx` client with:

- Connect timeout: `2s`
- Configurable total timeout: `PROCESSING_TIMEOUT_SECONDS` (default `5s`)
- Limited retry for safe `GET` operations only.
- No blind retry of create `POST` operations.

### Downstream error mapping

| Condition | Gateway behavior |
|---|---|
| Processing unavailable / connection failure | `503 PROCESSING_UNAVAILABLE` |
| Downstream timeout | `504 PROCESSING_TIMEOUT` |
| Invalid internal credential | `401 PROCESSING_AUTH_FAILED` |
| Permission denied | `403 PROCESSING_FORBIDDEN` |
| Job not found | `404 JOB_NOT_FOUND` |
| Conflict | `409 CONFLICT` |
| Other unexpected downstream 4xx | `502 PROCESSING_BAD_RESPONSE` |

Gateway-generated downstream errors use the standard structure:

```json
{
  "error": {
    "code": "PROCESSING_TIMEOUT",
    "message": "Processing service timed out",
    "request_id": "..."
  }
}
```

## Correlation ID and Request ID

The request middleware implements both identifiers.

### `X-Request-ID`

A unique request ID is generated when one is not supplied. It identifies an individual incoming request.

### `X-Correlation-ID`

A correlation ID is accepted from the caller or generated when missing. The Gateway forwards it to Processing so related operations can be searched across service boundaries.

Both IDs are also returned in response headers and included in structured application logs.

## Idempotency

Job creation supports the `Idempotency-Key` header.

Behavior:

- Same key + same payload -> returns the previously created job.
- Same key + different payload -> `409 Conflict`.
- Same key while the original request is in progress -> `409 Conflict`.
- Idempotency state is stored in Redis.
- Payload fingerprints are generated with SHA-256 over a normalized JSON representation.
- Key reservation uses Redis `SET ... NX` to prevent duplicate ownership.

The implementation uses an in-progress TTL and a completed-result TTL so idempotency state does not live forever.

## PostgreSQL and Alembic

### Gateway database

The Gateway uses its own PostgreSQL database:

```text
user_db
└── users
```

Gateway Alembic files are stored under:

```text
gateway_service/
├── alembic.ini
└── alembic/
    ├── env.py
    └── versions/
```

Run Gateway migrations from the Docker container:

```powershell
docker compose exec gateway-service python -m alembic upgrade head
```

### Processing database

Processing owns the jobs database:

```text
jobs_db
└── jobs
```

Run Processing migrations with:

```powershell
docker compose run --rm processing-service alembic upgrade head
```

SQLAlchemy uses asynchronous engines and `AsyncSession` for database access.

## Redis and ARQ

Redis provides:

- ARQ queue storage.
- Gateway idempotency storage.

ARQ is used for background processing so the API request does not wait for the simulated job work to finish.

### Producer

Processing creates an ARQ pool and enqueues `process_job`.

### Worker

The worker:

1. Loads the job from `jobs_db`.
2. Sets status to `PROCESSING`.
3. Performs the simulated background work.
4. Sets status to `COMPLETED`.
5. Records `FAILED` when processing raises an exception and attempts to persist the failure state.

The worker receives propagated trace context so the asynchronous operation can continue the originating OpenTelemetry trace.

## Health and Readiness

### `/health`

A lightweight liveness endpoint. It confirms that the process is alive without performing expensive dependency checks.

### `/ready`

Checks required dependencies.

Processing readiness verifies:

- PostgreSQL connectivity using `SELECT 1`.
- Redis connectivity using `PING`.

Gateway readiness checks whether the Processing Service is ready.

A dependency failure returns `503` from the readiness endpoint.

## Structured Logging

Application logs are emitted as JSON rather than arbitrary print statements.

The formatter includes the fields required for operational debugging:

```text
timestamp
level
service
event
request_id
correlation_id
job_id
duration_ms
status
```

No passwords, JWT/access tokens, client secrets, or database passwords should be logged.

## OpenTelemetry

Basic OpenTelemetry tracing is implemented for both FastAPI services and outbound `httpx` calls.

The asynchronous queue flow also propagates W3C trace context:

```text
Client request
    |
    v
Gateway server span
    |
    v
Gateway HTTP client span
    |
    v
Processing server span
    |
    v
ARQ enqueue span
    |
    v
ARQ worker span
```

Correlation IDs remain separate from trace IDs so they can be used for operational request searching.

The current training implementation exports spans to the console rather than to an external tracing backend.

## API Versioning

Business and internal APIs are versioned explicitly:

```text
/api/v1/...
/internal/v1/...
```

Versioning keeps contracts stable when future API changes need to be introduced without breaking existing clients.

## Configuration

Configuration is loaded through `pydantic-settings` and environment variables.

The repository contains:

```text
.env.example   # safe template
.env           # local secrets, ignored by Git
```

Important database URLs are separated by service:

```env
# Gateway
GATEWAY_DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/user_db

# Processing
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/jobs_db
```

Inside Docker Compose, the Gateway uses the PostgreSQL service hostname:

```text
postgres:5432
```

while local Windows tooling uses:

```text
localhost:5432
```

Mandatory settings are represented as required Pydantic fields, so application startup fails when required configuration is missing.

## Docker Compose

The complete local environment contains five services:

```text
gateway-service
processing-service
worker
postgres
redis
```

Each FastAPI service has its own Dockerfile.

The Gateway image includes:

```text
app/
alembic/
alembic.ini
```

so Gateway migrations can be applied from inside the container.

The worker reuses the Processing Service image but runs the ARQ command instead of Uvicorn.

Container health checks are configured for PostgreSQL, Redis, Processing, and Gateway.

### Start the environment

1. Create `.env` from `.env.example` and provide local values.
2. Ensure the PostgreSQL server contains both logical databases:

```text
user_db
jobs_db
```

3. Start the environment:

```powershell
docker compose up -d --build
```

4. Apply Gateway migrations:

```powershell
docker compose exec gateway-service python -m alembic upgrade head
```

5. Apply Processing migrations:

```powershell
docker compose run --rm processing-service alembic upgrade head
```

6. Check service state:

```powershell
docker compose ps
```

Gateway: `http://localhost:8000`

Processing: `http://localhost:8001`

Swagger:

- `http://localhost:8000/docs`
- `http://localhost:8001/docs`

## Local Development and Tests

The project uses separate virtual environments for Gateway and Processing development.

Integration tests are run from the project root:

```powershell
pytest tests\integration -v
```

The project previously verified a 29-test integration baseline before the database-backed registration/login change. After switching authentication from demo credentials to `user_db`, the authentication tests should be rerun and updated to exercise registration and database-backed login.

The integration suite covers authentication, authorization requirements, correlation/request IDs, health endpoints, idempotency, Gateway job creation, job retrieval, worker completion, invalid requests, Processing service authentication, and validation behavior.

### Recommended authentication test flow

```text
Register user
    ↓
Verify user exists in user_db
    ↓
Login using registered credentials
    ↓
Receive JWT
    ↓
Use JWT on protected Gateway endpoints
```

### Failure scenarios demonstrated

The project was also exercised manually for the required failure cases:

- Processing Service unavailable.
- Downstream timeout.
- Redis unavailable / readiness degradation.
- Invalid internal service token.
- Duplicate idempotency key.
- Worker failure resulting in `FAILED`.
- Invalid job ID returning `404`.

The manual failure demonstrations are intentionally separated from the normal automated integration suite so the production code does not contain permanent test-only failure injection.

## CI

GitHub Actions is configured in:

```text
.github/workflows/ci.yml
```

The workflow performs:

```text
Push / Pull Request
        |
        v
Install dependencies
        |
        v
Ruff lint
        |
        v
Ruff formatting check
        |
        v
Docker Compose validation
        |
        v
Docker image build
        |
        v
PostgreSQL + Redis
        |
        v
Alembic migrations
        |
        v
Gateway + Processing + Worker
        |
        v
Health / Readiness checks
        |
        v
Integration tests
        |
        v
Cleanup
```

The assignment does not require a full cloud deployment. This project therefore implements CI validation rather than cloud CD/deployment.

Ruff is used as the project's linting/formatting tool; the training task requires linting/formatting but does not mandate Ruff specifically.

## Project Structure

```text
final_backend_training_task/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── gateway_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   └── app/
│       ├── api/
│       │   └── v1/
│       │       ├── auth.py
│       │       └── jobs.py
│       ├── clients/
│       ├── core/
│       │   ├── config.py
│       │   ├── password.py
│       │   ├── security.py
│       │   └── ...
│       ├── db/
│       │   ├── base.py
│       │   └── session.py
│       ├── dependencies/
│       ├── middleware/
│       ├── models/
│       │   └── user.py
│       ├── schemas/
│       └── services/
│
├── processing_service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   └── app/
│       ├── api/
│       │   └── internal/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── repositories/
│       ├── schemas/
│       ├── services/
│       ├── workers/
│       └── middleware/
│
├── tests/
│   ├── integration/
│   └── manual/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Security Practices

- Real `.env` files are ignored by Git.
- Secrets are provided through environment variables.
- User passwords are stored only as Argon2 hashes.
- Service authentication is required for internal job APIs.
- JWT authentication protects Gateway job APIs.
- No tokens or passwords are intentionally written to structured logs.
- Gateway does not access the Processing database directly.
- POST job creation is not blindly retried.
- Idempotency is used to protect create operations from duplicates.
- User credentials and job data are stored in separate logical databases.

## Validation Checklist

The implementation was checked against the Day 8 training requirements:

- [x] Two FastAPI services.
- [x] Gateway public API.
- [x] Processing internal API.
- [x] Secure Gateway -> Processing communication.
- [x] User registration.
- [x] Database-backed user login.
- [x] Argon2 password hashing.
- [x] JWT authentication.
- [x] Separate `user_db` and `jobs_db`.
- [x] Request and correlation ID propagation.
- [x] Downstream timeout handling.
- [x] Safe GET retries.
- [x] Standard downstream error mapping.
- [x] PostgreSQL persistence.
- [x] Redis integration.
- [x] ARQ producer and worker.
- [x] Job state transitions.
- [x] Idempotency.
- [x] Health and readiness endpoints.
- [x] Structured JSON logging.
- [x] OpenTelemetry tracing.
- [x] API versioning.
- [x] Environment-based configuration.
- [x] Dockerfiles and Docker Compose.
- [x] Gateway and Processing Alembic migrations.
- [x] Integration tests.
- [x] Failure scenario demonstrations.
- [x] GitHub Actions CI workflow.

## Known Scope / Limitations

This is a training project rather than a fully deployed production platform.

- User registration/login are database-backed, but the project still uses a simple `role="user"` model rather than a full role/permissions system.
- OpenTelemetry currently exports spans to the console; no Jaeger/Tempo/OTel Collector is included.
- Failure scenarios that require stopping dependencies or forcing worker errors are documented/manual demonstrations rather than always-on automated tests.
- CI validates and tests the application but does not perform cloud deployment.
- The last verified 29-test baseline was recorded before the database-backed authentication change; the auth integration tests need a final rerun after the change.

## Final Outcome

The project demonstrates a complete request path from a public Gateway through an authenticated internal Processing Service to PostgreSQL and Redis/ARQ background processing, with database-backed user authentication, password hashing, request tracing, structured logs, resilience controls, idempotency, Docker orchestration, migrations, and integration testing.
