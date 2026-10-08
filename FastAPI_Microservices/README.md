# FastAPI Microservices – Production Backend

A production-style microservice system built using FastAPI.

The project contains two independent FastAPI services:

* Gateway Service
* Processing Service

The system also uses PostgreSQL for persistent data storage and Redis with ARQ for background job processing.

---

## Features

* Microservice architecture
* Gateway and Processing services
* Async service-to-service communication
* Internal service authentication
* JWT-based authentication
* Pydantic request validation
* PostgreSQL database
* Async SQLAlchemy
* Redis
* ARQ background worker
* Job queue processing
* Correlation ID propagation
* Request ID generation
* Timeout handling
* Safe retry handling
* Idempotency support
* Health checks
* Readiness checks
* Structured logging
* OpenTelemetry basics
* API versioning
* Docker and Docker Compose
* Integration testing
* Failure scenario testing
* Environment-based configuration
* Swagger/OpenAPI documentation

---

## Architecture

```text
                    Client
                      |
                      v
              Gateway Service
                 Port 8000
                      |
             Async HTTP Request
                      |
                      v
             Processing Service
                 Port 8001
                 /         \
                /           \
               v             v
        PostgreSQL          Redis
                              |
                              v
                         ARQ Worker
                              |
                              v
                       Background Job
```

The Gateway Service handles public API requests.

The Processing Service handles internal job processing and owns the database and background processing.

---

## Project Structure

```text
FastAPI_Microservices/
│
├── gateway_service/
│   └── app/
│       ├── api/
│       ├── clients/
│       ├── core/
│       ├── middleware/
│       ├── schemas/
│       ├── services/
│       ├── tests/
│       └── main.py
│
├── processing_service/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── models/
│       ├── repositories/
│       ├── schemas/
│       ├── services/
│       ├── tests/
│       └── workers/
│
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## Services

### Gateway Service

The Gateway Service is responsible for:

* Public APIs
* Request validation
* Authentication
* Correlation ID generation
* Request ID generation
* Communication with Processing Service
* Timeout handling
* Downstream error handling
* API versioning

### Processing Service

The Processing Service is responsible for:

* Internal APIs
* Internal service authentication
* Job creation
* PostgreSQL persistence
* Job status management
* Redis/ARQ job queue
* Background processing
* Structured logging

---

## Technologies

* Python
* FastAPI
* Pydantic
* Pydantic Settings
* PostgreSQL
* SQLAlchemy
* Async SQLAlchemy
* asyncpg
* Redis
* ARQ
* HTTPX
* JWT
* Uvicorn
* Pytest
* Docker
* Docker Compose
* OpenTelemetry

---

# Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
cd FastAPI_Microservices
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

---

## 3. Activate Virtual Environment

For PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

## 4. Install Dependencies

Install the required dependencies for the services.

```bash
pip install fastapi uvicorn[standard] httpx pydantic-settings
```

Additional project dependencies are defined according to the service requirements.

---

# Environment Configuration

Create a `.env` file using `.env.example` as a template.

Example configuration:

```env
GATEWAY_SERVICE_CLIENT_ID=gateway
GATEWAY_SERVICE_CLIENT_SECRET=change_me

PROCESSING_BASE_URL=http://processing-service:8001

PROCESSING_TIMEOUT_SECONDS=5

JWT_SECRET_KEY=change_me

REDIS_URL=redis://redis:6379/0

DATABASE_URL=postgresql+asyncpg://jobs_user:jobs_password@postgres:5432/jobs_db
```

Do not commit the real `.env` file.

Never expose:

* Database passwords
* JWT secrets
* Service client secrets
* Access tokens
* Other sensitive configuration

---

# API Versioning

Public APIs use:

```text
/api/v1/
```

Internal service APIs use:

```text
/internal/v1/
```

Versioning makes it easier to introduce future API changes without breaking existing clients.

---

# Gateway APIs

## Create Job

### POST

```text
/api/v1/jobs
```

Example request:

```json
{
  "name": "Generate monthly report",
  "job_type": "report",
  "priority": "high"
}
```

The Gateway validates the request and sends it to the Processing Service.

---

## Get Job

### GET

```text
/api/v1/jobs/{job_id}
```

The Gateway requests the job information from the Processing Service.

---

## Health Check

### GET

```text
/health
```

Used to verify that the Gateway service is running.

---

## Readiness Check

### GET

```text
/ready
```

Used to verify that the Gateway service is ready to handle requests.

---

# Processing APIs

Processing Service APIs are internal APIs.

## Create Job

### POST

```text
/internal/v1/jobs
```

The Processing Service:

1. Validates the internal request.
2. Creates the job record.
3. Stores the job in PostgreSQL.
4. Adds the job to the Redis/ARQ queue.
5. Returns the job information.

---

## Get Job

### GET

```text
/internal/v1/jobs/{job_id}
```

Returns the job information from the Processing Service.

---

## Health Check

### GET

```text
/health
```

Checks whether the Processing Service is running.

---

## Readiness Check

### GET

```text
/ready
```

Checks whether required dependencies are available.

---

# Job Status

Jobs can move through the following states:

```text
CREATED
   ↓
QUEUED
   ↓
PROCESSING
   ↓
COMPLETED
```

If processing fails:

```text
PROCESSING
   ↓
FAILED
```

---

# Service-to-Service Authentication

The Gateway communicates with the Processing Service using internal authentication.

Example configuration:

```env
GATEWAY_SERVICE_CLIENT_ID=gateway
GATEWAY_SERVICE_CLIENT_SECRET=change_me
```

The Processing Service validates the internal service credentials before accepting internal requests.

---

# Correlation ID and Request ID

The system uses two identifiers.

### Correlation ID

`X-Correlation-ID` identifies the complete request flow across services.

If the client provides a correlation ID, the Gateway forwards it to the Processing Service.

If it is missing, the Gateway generates one.

### Request ID

`X-Request-ID` identifies an individual request.

The Gateway generates a unique request ID.

Example:

```text
X-Correlation-ID: corr-10001
X-Request-ID: req-a91f
```

The correlation ID is included in service logs so that the complete request flow can be traced.

---

# Timeout Handling

The Gateway uses a timeout when communicating with the Processing Service.

Example:

```env
PROCESSING_TIMEOUT_SECONDS=5
```

If the Processing Service does not respond within the configured timeout, the Gateway returns an appropriate downstream timeout error.

Example:

```json
{
  "error": {
    "code": "PROCESSING_SERVICE_TIMEOUT",
    "message": "Processing service did not respond in time.",
    "request_id": "req-a91f"
  }
}
```

---

# Retry Handling

Retries should only be used for operations where retrying is safe.

The system should avoid blindly retrying job creation requests because a retry can create duplicate jobs.

For operations that support retries:

* Use a limited number of retries.
* Use short backoff.
* Use idempotency where required.

---

# Idempotency

Job creation supports an idempotency key.

Example:

```text
Idempotency-Key: client-job-1001
```

The same key with the same request should not create a duplicate job.

If the same key is reused with a different request payload, the API returns:

```text
409 Conflict
```

Idempotency information can be stored in PostgreSQL or Redis.

---

# PostgreSQL

PostgreSQL is used by the Processing Service for persistent job data.

Current Docker Compose configuration:

```text
Database: jobs_db
User: jobs_user
Host: postgres
Port: 5432
```

From the host machine:

```text
localhost:5433
```

Example database URL:

```env
DATABASE_URL=postgresql+asyncpg://jobs_user:jobs_password@postgres:5432/jobs_db
```

The Processing Service owns the job database.

The Gateway does not directly access the Processing Service database.

---

# Redis

Redis is used for background job processing.

Configuration:

```env
REDIS_URL=redis://redis:6379/0
```

Redis is used together with ARQ.

---

# ARQ Background Worker

ARQ is used to process jobs asynchronously.

The flow is:

```text
Client
  ↓
Gateway
  ↓
Processing Service
  ↓
PostgreSQL
  ↓
Redis Queue
  ↓
ARQ Worker
  ↓
Background Processing
  ↓
PostgreSQL
```

The API does not have to wait for long-running background work to complete.

---

# Docker

The project uses Docker Compose to run the complete system.

Services:

```text
gateway-service
processing-service
worker
postgres
redis
```

---

## Build Containers

```bash
docker compose build
```

---

## Start Services

```bash
docker compose up -d
```

---

## Check Running Containers

```bash
docker compose ps
```

or:

```bash
docker ps
```

---

## View Logs

Gateway:

```bash
docker compose logs gateway-service
```

Processing:

```bash
docker compose logs processing-service
```

Worker:

```bash
docker compose logs worker
```

---

## Stop Services

```bash
docker compose down
```

---

# Current Docker Configuration

The development environment uses:

```text
Gateway       → localhost:8000
Processing    → localhost:8001
PostgreSQL    → localhost:5433
Redis         → localhost:6379
```

Inside Docker Compose, services communicate using their service names.

Example:

```text
Processing Service:
http://processing-service:8001
```

---

# PostgreSQL Database Access

To connect to PostgreSQL:

```bash
docker compose exec postgres psql -U jobs_user -d jobs_db
```

List tables:

```sql
\dt
```

List public tables:

```sql
\dt public.*
```

View jobs:

```sql
SELECT * FROM jobs;
```

View users:

```sql
SELECT * FROM users;
```

Exit PostgreSQL:

```sql
\q
```

---

# Health and Readiness

## Health

Health checks confirm that the service process is alive.

```text
GET /health
```

## Readiness

Readiness checks confirm that required dependencies are available.

```text
GET /ready
```

Readiness may check dependencies such as:

* PostgreSQL
* Redis

Health checks should remain lightweight.

---

# Structured Logging

Logs should contain useful structured fields such as:

* timestamp
* level
* service
* event
* request_id
* correlation_id
* job_id
* duration_ms
* status

Example:

```json
{
  "level": "INFO",
  "service": "processing-service",
  "event": "job_completed",
  "job_id": "JOB1001",
  "correlation_id": "corr-10001",
  "duration_ms": 742
}
```

Sensitive information must not be logged.

Do not log:

* Passwords
* JWT/access tokens
* Client secrets
* Database passwords

---

# OpenTelemetry

OpenTelemetry can be used for distributed tracing.

Example request flow:

```text
Client
  ↓
Gateway Span
  ↓
HTTP Client Span
  ↓
Processing Service Span
  ↓
ARQ Worker Span
```

Important tracing concepts:

* Trace ID
* Span ID

Correlation ID should still be maintained separately for application-level request tracking.

---

# Error Handling

Common error responses include:

| Status Code | Meaning                        |
| ----------- | ------------------------------ |
| 400         | Bad request                    |
| 401         | Invalid authentication         |
| 403         | Permission denied              |
| 404         | Job not found                  |
| 409         | Idempotency conflict           |
| 422         | Validation error               |
| 502         | Processing service unavailable |
| 503         | Service unavailable            |
| 504         | Processing service timeout     |

---

# Integration Tests

The project should test the complete microservice workflow.

Important test cases:

1. Gateway creates a job successfully.
2. Processing Service receives the internal request.
3. Invalid service credentials fail.
4. Correlation ID reaches Processing Service.
5. Gateway handles Processing Service timeout.
6. Processing Service creates a database record.
7. ARQ worker changes job status to `COMPLETED`.
8. Failed worker changes job status to `FAILED`.
9. Duplicate idempotency key does not create another job.
10. Health endpoint works.
11. Readiness fails when a required dependency is unavailable.
12. Job not found returns `404`.

Run tests with:

```bash
pytest -q
```

---

# Failure Scenarios

The system should handle the following failure scenarios.

## Processing Service Down

Stop the Processing Service and send a request through the Gateway.

The Gateway should return an appropriate service-unavailable error.

---

## Redis Down

Stop Redis and check:

```text
/ready
```

Readiness should indicate that the required dependency is unavailable.

---

## Invalid Internal Credentials

Use an invalid service credential.

The Processing Service should reject the request.

---

## Duplicate Idempotency Key

Send the same job creation request twice with the same:

```text
Idempotency-Key
```

The system should not create duplicate jobs.

---

## Worker Failure

Force a background job failure.

The job should move to:

```text
FAILED
```

---

## Invalid Job ID

Request a non-existing job:

```text
/api/v1/jobs/{job_id}
```

The API should return:

```text
404 Not Found
```

---

# CI/CD

The expected CI/CD flow is:

```text
Push Code
    ↓
Lint / Format
    ↓
Unit Tests
    ↓
Integration Tests
    ↓
Docker Build
    ↓
Deploy
```

A failed test or failed build should stop the deployment pipeline.

---

# Demo Flow

The complete system can be demonstrated using the following flow:

```text
Client
  ↓
POST /api/v1/jobs
  ↓
Gateway
  ↓
Correlation ID + Request ID
  ↓
Internal Authentication
  ↓
Processing Service
  ↓
PostgreSQL
  ↓
Redis / ARQ
  ↓
Worker
  ↓
PROCESSING
  ↓
COMPLETED
```

During the demo, verify:

* Job creation through Gateway
* Gateway to Processing communication
* Internal authentication
* Correlation ID propagation
* PostgreSQL record
* Redis queue
* ARQ worker
* Final job status
* Timeout handling
* Idempotency
* Structured logs
* Health and readiness
* Integration tests

---

# Important Concepts

### Microservice

An independently deployable service responsible for a specific business capability.

### Gateway

The public entry point that communicates with internal services.

### Service-to-Service Authentication

Authentication used when one internal service communicates with another service.

### Correlation ID

Identifier used to track one request flow across multiple services.

### Request ID

Identifier used to identify an individual request.

### Timeout

Maximum amount of time a service waits for another service to respond.

### Idempotency

Ensures that repeating the same request does not unintentionally create duplicate results.

### Redis

An in-memory data store used here for queue/background job processing.

### ARQ

A Python background job queue that uses Redis.

### Worker

A process that consumes queued jobs and performs background work.

### Health Check

Shows whether the service is alive.

### Readiness Check

Shows whether the service is ready to handle requests.

---

# Definition of Done

The Day 8 implementation is complete when:

* Gateway and Processing services communicate securely.
* Correlation IDs propagate between services.
* Request IDs are generated and available in logs/errors.
* Downstream failures are handled correctly.
* Timeouts are configured.
* Safe retry behavior is implemented where applicable.
* Idempotency is supported for job creation.
* PostgreSQL stores job data.
* Redis and ARQ process background jobs.
* Docker Compose runs the complete environment.
* Health and readiness endpoints work.
* Structured logging is available.
* OpenTelemetry basics are understood/implemented where applicable.
* Integration tests verify the main workflow.
* Failure scenarios can be demonstrated.
* README and `.env.example` are included.

---

# Security Notes

Do not commit:

```text
.env
Real passwords
JWT secrets
Service client secrets
Access tokens
Database credentials
```

Commit only placeholder configuration through:

```text
.env.example
```

---

# Docker Compose Services

```text
┌─────────────────────┐
│   Gateway Service   │
│      :8000          │
└──────────┬──────────┘
           │
           │ HTTP
           ▼
┌─────────────────────┐
│ Processing Service  │
│      :8001          │
└───────┬─────┬───────┘
        │     │
        ▼     ▼
  PostgreSQL  Redis
               │
               ▼
          ARQ Worker
```

---

# Project Status

## Day 8 — Production Backend Microservices

Completed / Implemented:

* Gateway Service
* Processing Service
* FastAPI service structure
* Docker Compose environment
* PostgreSQL integration
* Redis integration
* ARQ worker setup
* Service-to-service communication
* Internal API structure
* Health endpoints
* Readiness endpoints
* Job processing flow
* Structured project architecture
* Integration testing structure

The remaining Day 8 requirements should be verified through the final integration tests and demo checklist.
