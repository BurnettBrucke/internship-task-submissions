# FastAPI Microservices – Day 8

A production-oriented microservices backend built with **FastAPI**, **PostgreSQL**, **Redis/ARQ**, **JWT Authentication**, **OpenTelemetry**, **Docker**, and **GitHub Actions CI/CD**.

## 1. Architecture

                    Client
                       |
                       | JWT
                       v
              +------------------+
              | Gateway Service  |
              |     :8000        |
              +------------------+
                       |
                       | Internal Bearer Token
                       v
              +------------------+
              | Processing       |
              | Service :8001    |
              +------------------+
                 |           |
                 v           v
            PostgreSQL    Redis
                             |
                             v
                        ARQ Worker


## 2. Services

### Gateway Service – Port 8000

Responsibilities:

* User registration and JWT login
* JWT-protected public APIs
* Job request validation
* Request ID and Correlation ID handling
* Communication with Processing Service
* Downstream timeout and error handling
* Safe GET retry handling
* Idempotency protection for job creation

Endpoints:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/jobs
GET  /api/v1/jobs/{job_id}
GET  /health
GET  /ready
```

### Processing Service – Port 8001

Responsibilities:

* Internal service authentication
* Job persistence
* Idempotency handling
* Redis/ARQ background processing
* Job status management
* Database-backed job retrieval

Endpoints:

```text
POST /internal/v1/jobs
GET  /internal/v1/jobs/{job_id}
GET  /health
GET  /ready
```

### ARQ Worker

The ARQ worker processes queued jobs asynchronously and updates their status in PostgreSQL.

Run:

```powershell
python -m arq processing_service.app.worker.WorkerSettings
```

## 3. Job Flow

```text
CREATED
   |
   v
QUEUED
   |
   v
PROCESSING
   |
   +------> COMPLETED
   |
   +------> FAILED
```

Job creation requires an `Idempotency-Key`.

The same idempotency key with the same payload returns the existing job instead of creating a duplicate.

Using the same idempotency key with a different payload returns a conflict response.

## 4. Authentication

There are two authentication layers.

### Client → Gateway

The client authenticates using JWT.

```text
Client
  |
  | JWT Bearer Token
  v
Gateway
```

### Gateway → Processing

The Gateway authenticates with the Processing Service using an internal bearer token.

```text
Gateway
  |
  | Internal Bearer Token
  v
Processing Service
```

The internal service token is loaded from configuration/environment variables and is not hardcoded as a production secret.

## 5. Database, Cache and Queue

### PostgreSQL

Used for persistent storage of:

* Users
* Jobs
* Job status
* Idempotency information

### SQLAlchemy + asyncpg

Used for asynchronous database access.

### Alembic

Used for database schema migrations.

### Redis

Used for queue/cache functionality.

### ARQ

Used for asynchronous background job processing.

## 6. Reliability and Error Handling

The Gateway implements:

* Processing Service timeout handling
* Downstream `503 Service Unavailable` handling
* `504 Gateway Timeout` for processing timeouts
* Safe retries for GET requests
* No blind retries for POST requests
* Idempotency protection for POST job creation

This prevents accidental duplicate job creation while allowing safe retry behaviour for read operations.

## 7. Request and Correlation IDs

The system uses:

```text
X-Request-ID
X-Correlation-ID
```

### X-Request-ID

Identifies an individual request.

### X-Correlation-ID

Tracks the same operation across Gateway and Processing services.

Correlation IDs are propagated between services and returned in response headers.

## 8. Observability

The project includes basic production observability features:

* Structured JSON-style request logs
* Request ID logging
* Correlation ID logging
* Request duration logging
* HTTP status logging
* OpenTelemetry FastAPI instrumentation

OpenTelemetry dependencies are also included in the CI environment.

## 9. Health and Readiness

### Gateway

```text
GET /health
GET /ready
```

### Processing

```text
GET /health
GET /ready
```

`/health` confirms that the service is running.

`/ready` checks required dependencies before reporting the service as ready.

## 10. Configuration

Configuration is loaded through environment variables and the `.env` file.

Use:

```text
.env.example
```

as the configuration template.

Important configuration includes:

```text
DATABASE_URL
REDIS_URL
PROCESSING_BASE_URL
INTERNAL_SERVICE_TOKEN
JWT_SECRET_KEY
```

**Never commit real passwords, tokens, API keys, or other secrets to Git.**

## 11. Running Locally

### Processing Service

```powershell
cd E:\Burnett_internship\microservices

python -m uvicorn processing_service.app.main:app --reload --port 8001
```

### Gateway Service

```powershell
cd E:\Burnett_internship\microservices\gateway_service

python -m uvicorn app.main:app --reload --port 8000
```

### ARQ Worker

```powershell
cd E:\Burnett_internship\microservices

python -m arq processing_service.app.worker.WorkerSettings
```

### Swagger Documentation

Gateway:

```text
http://127.0.0.1:8000/docs
```

Processing:

```text
http://127.0.0.1:8001/docs
```

## 12. Database Migrations

Gateway migrations:

```powershell
cd E:\Burnett_internship\microservices\gateway_service

alembic upgrade head
```

Processing migrations:

```powershell
cd E:\Burnett_internship\microservices

alembic upgrade head
```

## 13. Testing

### Gateway Tests

```powershell
cd E:\Burnett_internship\microservices\gateway_service

pytest -q tests
```

Result:

```text
12 passed
```

### Processing Tests

```powershell
cd E:\Burnett_internship\microservices\processing_service

pytest -q tests
```

Result:

```text
10 passed
```

### Total

```text
22 tests passed
```

Tests cover:

* JWT authentication
* Authorization
* Internal service authentication
* Job creation
* Job retrieval
* Validation
* Idempotency
* Job status flow
* Health/readiness
* Request ID
* Correlation ID
* Processing Service failure handling
* Timeout handling
* GET retry behaviour

## 14. CI/CD

GitHub Actions is configured for automated testing.

The CI pipeline:

1. Checks out the repository
2. Sets up Python 3.10
3. Installs project dependencies
4. Starts PostgreSQL
5. Starts Redis
6. Runs Gateway database migrations
7. Runs Processing database migrations
8. Starts the Processing Service
9. Runs Gateway tests
10. Runs Processing tests

Current CI status:

```text
Gateway tests:     12 passed
Processing tests:  10 passed
Total:             22 passed
GitHub Actions:    PASS
```

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

## 15. Docker

The project supports Docker and Docker Compose for running the complete microservices environment.

### Docker Services

```text
Gateway       :8000
Processing    :8001
PostgreSQL    :5432
Redis         :6379
ARQ Worker
```

### Build Containers

From the `microservices` directory:

```bash
docker compose build
```

### Start Services

```bash
docker compose up -d
```

### Check Service Status

```bash
docker compose ps
```

PostgreSQL and Redis include health checks, and the Processing Service and Worker depend on these healthy services.

### Database Migrations

Gateway:

```bash
docker compose exec gateway alembic upgrade head
```

Processing:

```bash
docker compose exec processing alembic -c /app/alembic.ini upgrade head
```

### Health Checks

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
```

### View Worker Logs

```bash
docker compose logs worker --tail=30
```

### Docker Verification

The complete Docker environment was verified successfully.

```text
Gateway:              HEALTHY
Processing:           HEALTHY
PostgreSQL:           HEALTHY
Redis:                HEALTHY
ARQ Worker:           RUNNING
Database Migrations:  PASS
```

End-to-end job verification:

```text
POST /api/v1/jobs       → 201 Created
Job Status              → QUEUED
ARQ Worker              → PROCESSING
Final Job Status        → COMPLETED
```

## 16. Project Status

### Completed

* Gateway Service
* Processing Service
* JWT Authentication
* Internal Service Authentication
* PostgreSQL Persistence
* Redis
* ARQ Background Worker
* Idempotency
* Job Status Flow
* Request ID
* Correlation ID
* Timeout Handling
* Downstream Error Handling
* Safe GET Retry
* Structured Logging
* Health/Readiness Checks
* OpenTelemetry Basics
* Database Migrations
* Automated Tests
* GitHub Actions CI/CD
* Docker
* Docker Compose
* Containerized PostgreSQL
* Containerized Redis
* Containerized ARQ Worker
* End-to-End Docker Verification

### Verification

```text
Gateway:        12/12 tests passed
Processing:     10/10 tests passed
Total:          22/22 tests passed
CI/CD:          PASS
Docker:         PASS
E2E Job Flow:   PASS
```

## 17. Conclusion

The Day 8 microservices backend is implemented and verified with automated tests, GitHub Actions CI/CD, and Docker Compose.

The final architecture provides:

* Service-to-service authentication
* Persistent database storage
* Asynchronous background processing
* Idempotent job creation
* Retry and timeout handling
* Request tracing through correlation IDs
* Structured logging
* Health and readiness checks
* Automated testing and CI validation
* Containerized microservices deployment
* PostgreSQL and Redis container integration
* End-to-end background job processing
