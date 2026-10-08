# FastAPI Microservices - Day 8

A microservices-based backend project built with FastAPI.

## 1. Architecture


Client
  |
  | JWT
  v
Gateway :8000
  |
  | Internal Bearer Token
  v
Processing :8001
  |
  +--> PostgreSQL
  |
  +--> Redis --> ARQ Worker

 ## 2. Services

Gateway Service
User JWT authentication
Job request validation
Request/Correlation ID handling
Communication with Processing Service
Timeout and downstream error handling

Endpoints:

POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/jobs
GET /api/v1/jobs/{job_id}
GET /health
GET /ready
Processing Service
Internal service authentication
Job persistence
Idempotency
Redis/ARQ background processing
Job status updates

Endpoints:

POST /internal/v1/jobs
GET /internal/v1/jobs/{job_id}
GET /health
GET /ready

### 3. Job Flow

CREATED → QUEUED → PROCESSING → COMPLETED
                              └→ FAILED

Job creation requires an Idempotency-Key to prevent duplicate jobs.

### 4. Authentication

The client authenticates with the Gateway using JWT.

The Gateway authenticates with the Processing Service using an internal bearer token.

Client → JWT → Gateway → Internal Token → Processing
### 5. Database & Queue
PostgreSQL → job persistence
Redis → queue/cache
ARQ → background job worker
SQLAlchemy + asyncpg → async database access
Alembic → database migrations

###6. Observability

X-Correlation-ID tracks a request across services.
X-Request-ID identifies an individual request.
OpenTelemetry provides basic FastAPI request instrumentation.
Structured request logs are used in both services.

### 7. Configuration

Configuration is loaded from the root .env file.

Use .env.example as the template.

Do not commit real passwords, tokens, or other secrets.

### 8. Running the Services
Gateway
cd E:\Burnett_internship\microservices\gateway_service
.\..\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --port 8000

Processing
cd E:\Burnett_internship\microservices
.\venv\Scripts\Activate.ps1
python -m uvicorn processing_service.app.main:app --port 8001

ARQ Worker
cd E:\Burnett_internship\microservices
.\venv\Scripts\Activate.ps1
arq processing_service.app.worker.WorkerSettings

Swagger:

Gateway: http://127.0.0.1:8000/docs
Processing: http://127.0.0.1:8001/docs

###9. Testing

Run:

pytest gateway_service\tests processing_service\tests -v

Current result:

15 passed

Tests cover authentication, authorization, validation, health/readiness, job creation, internal authentication and idempotency.

### 10. Status

Day 8 core implementation completed.

Gateway + Processing: Complete
JWT + Internal Authentication: Complete
PostgreSQL + Redis + ARQ: Complete
Idempotency: Complete
Request/Correlation ID: Complete
Timeout/Error Handling: Complete
OpenTelemetry Basics: Complete
Tests: 15/15 Passed