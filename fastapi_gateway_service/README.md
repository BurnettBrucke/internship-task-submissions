# FastAPI Gateway Microservices

A production-style FastAPI microservice system with a public Gateway Service, internal Processing Service, PostgreSQL, Redis, and an ARQ background worker.

## Architecture

```text
Client
  |
  v
Gateway Service :8000
  |
  | Async HTTP
  | X-Correlation-ID
  | Internal Bearer Token
  v
Processing Service :8001
  |
  +---------> PostgreSQL
  |
  +---------> Redis
                  |
                  v
             ARQ Worker
```

## Services

| Service            | Port | Responsibility                                                                    |
| ------------------ | ---: | --------------------------------------------------------------------------------- |
| Gateway Service    | 8000 | Public API, JWT authentication, request/correlation IDs, downstream communication |
| Processing Service | 8001 | Internal job API, PostgreSQL persistence, Redis queueing                          |
| Worker             |    - | ARQ background job processing                                                     |
| PostgreSQL         | 5432 | Job persistence                                                                   |
| Redis              | 6379 | Queue and background-job broker                                                   |

## Project Structure

```text
Fastapi-gateway/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── gateway_service/
│   ├── app/
│   │   ├── api/
│   │   ├── clients/
│   │   ├── core/
│   │   ├── middleware/
│   │   └── schemas/
│   ├── tests/
│   │   └── test_day8_integration.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── processing_service/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── workers/
│   ├── alembic/
│   ├── tests/
│   │   └── test_day8_processing.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── ruff.toml
└── README.md
```

## Implemented Features

### Gateway Service

* JWT authentication
* Public versioned APIs
* Async HTTP communication with Processing Service
* Internal service authentication
* Request ID generation
* Correlation ID propagation
* Timeout handling
* Processing Service unavailable handling
* Downstream error mapping
* Idempotency support
* Health endpoint
* Readiness endpoint
* Structured logging
* OpenTelemetry tracing basics

### Processing Service

* Internal versioned APIs
* Internal Bearer token authentication
* PostgreSQL persistence with SQLAlchemy
* Alembic migrations
* Redis integration
* ARQ background worker
* Job status transitions
* Idempotency handling
* Health endpoint
* Database and Redis readiness checks
* Structured request/correlation logging

### Job Lifecycle

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

The API stores the job in PostgreSQL first and then places the job on the Redis/ARQ queue. The worker processes it asynchronously.

## API Endpoints

### Gateway

```text
POST /api/v1/jobs
GET  /api/v1/jobs/{job_id}
GET  /health
GET  /ready
```

### Processing Service

```text
POST /internal/v1/jobs
GET  /internal/v1/jobs/{job_id}
GET  /health
GET  /ready
```

Interactive API documentation is available through FastAPI Swagger:

```text
http://localhost:8000/docs
http://localhost:8001/docs
```

## Idempotency

Job creation requires an `Idempotency-Key`.

The same key with the same payload returns the existing job instead of creating a duplicate.

The same key with a different payload returns:

```text
409 Conflict
```

with the error code:

```text
IDEMPOTENCY_CONFLICT
```

## Correlation and Request IDs

The system supports:

```text
X-Correlation-ID
X-Request-ID
```

The Gateway generates a correlation ID when one is not supplied and forwards it to the Processing Service.

A new request ID is generated for every incoming request.

These IDs are used for tracing and log correlation across services.

## Error Handling

The Gateway maps common downstream failures:

| Situation                       | Response |
| ------------------------------- | -------: |
| Missing/invalid JWT             |      401 |
| Invalid internal credential     |      401 |
| Job not found                   |      404 |
| Idempotency conflict            |      409 |
| Processing Service unavailable  |      503 |
| Processing Service timeout      |      504 |
| Processing Service server error |      502 |

## Local Setup

Create the required environment files using the provided examples.

Do not commit real secrets.

### Start the complete system

From the project root:

```powershell
docker compose up --build
```

Check running services:

```powershell
docker compose ps
```

Check logs:

```powershell
docker compose logs gateway-service
docker compose logs processing-service
docker compose logs worker
```

### Stop the system

```powershell
docker compose down
```

To remove the PostgreSQL volume as well:

```powershell
docker compose down -v
```

## Database Migration

Database migrations are managed with Alembic.

Run:

```powershell
cd processing_service
alembic upgrade head
```

## Testing

### Gateway tests

```powershell
cd gateway_service
pytest -q tests/test_day8_integration.py
```

### Processing Service tests

```powershell
cd processing_service
pytest -q tests/test_day8_processing.py
```

### Ruff linting

From the project root:

```powershell
ruff check gateway_service processing_service
```

### Ruff formatting

```powershell
ruff format --check gateway_service processing_service
```

To automatically format files:

```powershell
ruff format gateway_service processing_service
```

## Docker Commands

### Check Docker Installation

Check Docker version:

```powershell
docker --version
```

Check Docker Compose version:

```powershell
docker compose version
```

Test that Docker can run containers:

```powershell
docker run hello-world
```

### Docker Login

Login to Docker Hub:

```powershell
docker login
```

Logout:

```powershell
docker logout
```

### Pull Docker Images

Pull PostgreSQL:

```powershell
docker pull postgres:16
```

If Docker Hub is unreachable and the PostgreSQL pull times out, use the mirror:

```powershell
docker pull mirror.gcr.io/library/postgres:16
```

Tag the mirrored image as the normal PostgreSQL image:

```powershell
docker tag mirror.gcr.io/library/postgres:16 postgres:16
```

Verify downloaded images:

```powershell
docker images
```

Pull Redis:

```powershell
docker pull redis:7-alpine
```

### Build the Project

Build all Docker Compose services:

```powershell
docker compose build
```

Build again without using the cache:

```powershell
docker compose build --no-cache
```

Build a specific service:

```powershell
docker compose build gateway-service
```

Build the Processing Service:

```powershell
docker compose build processing-service
```

### Start the Complete Application

Start all services and show logs:

```powershell
docker compose up
```

Build images and start all services:

```powershell
docker compose up --build
```

Start services in the background:

```powershell
docker compose up -d
```

Build and start in the background:

```powershell
docker compose up -d --build
```

### Start Individual Services

Start PostgreSQL and Redis:

```powershell
docker compose up -d postgres redis
```

Start the Processing Service:

```powershell
docker compose up -d processing-service
```

Start the ARQ worker:

```powershell
docker compose up -d worker
```

Start the Gateway Service:

```powershell
docker compose up -d gateway-service
```

### Check Running Containers

Show Compose service status:

```powershell
docker compose ps
```

Show all Docker containers:

```powershell
docker ps
```

Show running and stopped containers:

```powershell
docker ps -a
```

### View Logs

View all Compose logs:

```powershell
docker compose logs
```

View Gateway logs:

```powershell
docker compose logs gateway-service
```

View Processing Service logs:

```powershell
docker compose logs processing-service
```

View Worker logs:

```powershell
docker compose logs worker
```

View PostgreSQL logs:

```powershell
docker compose logs postgres
```

View Redis logs:

```powershell
docker compose logs redis
```

Show only the latest 100 log lines:

```powershell
docker compose logs --tail=100
```

Follow logs continuously:

```powershell
docker compose logs -f
```

Follow Gateway logs:

```powershell
docker compose logs -f gateway-service
```

Follow Worker logs:

```powershell
docker compose logs -f worker
```

### Execute Commands Inside Containers

Open a shell inside the Gateway container:

```powershell
docker compose exec gateway-service sh
```

Open a shell inside the Processing Service container:

```powershell
docker compose exec processing-service sh
```

Open a shell inside the Worker container:

```powershell
docker compose exec worker sh
```

Check PostgreSQL readiness:

```powershell
docker compose exec postgres pg_isready -U postgres -d jobs_db
```

Check Redis:

```powershell
docker compose exec redis redis-cli ping
```

Expected Redis response:

```text
PONG
```

### Database Migrations Through Docker

Run Alembic migrations inside the Processing Service image:

```powershell
docker compose run --rm --no-deps processing-service alembic upgrade head
```

Check the current migration revision:

```powershell
docker compose run --rm --no-deps processing-service alembic current
```

Show migration history:

```powershell
docker compose run --rm --no-deps processing-service alembic history
```

### Restart Services

Restart everything:

```powershell
docker compose restart
```

Restart Gateway:

```powershell
docker compose restart gateway-service
```

Restart Processing Service:

```powershell
docker compose restart processing-service
```

Restart Worker:

```powershell
docker compose restart worker
```

### Stop Services

Stop services without removing containers:

```powershell
docker compose stop
```

Stop and remove containers/networks:

```powershell
docker compose down
```

Stop and remove containers, networks, and PostgreSQL volume:

```powershell
docker compose down -v
```

Remove containers and rebuild from scratch:

```powershell
docker compose down
docker compose build --no-cache
docker compose up
```

### Remove Docker Resources

Remove stopped containers:

```powershell
docker container prune
```

Remove unused images:

```powershell
docker image prune
```

Remove unused Docker resources:

```powershell
docker system prune
```

Be careful with:

```powershell
docker system prune -a
```

because it can remove unused images and other Docker resources that you may want to keep.

### Inspect Docker Images

List images:

```powershell
docker images
```

Inspect a specific image:

```powershell
docker image inspect postgres:16
```

### Inspect Containers

Inspect a container:

```powershell
docker inspect jobs-postgres
```

Inspect the Compose service:

```powershell
docker compose config
```

### Check Docker Health

Check the PostgreSQL container:

```powershell
docker inspect --format='{{.State.Health.Status}}' jobs-postgres
```

Check the Redis container:

```powershell
docker inspect --format='{{.State.Health.Status}}' jobs-redis
```

Expected result:

```text
healthy
```

### Complete Project Startup

From the project root, the normal startup command is:

```powershell
docker compose up --build
```

For background startup:

```powershell
docker compose up -d --build
```

Then verify:

```powershell
docker compose ps
```

Check the services:

```powershell
docker compose logs --tail=100
```

Test Gateway:

```powershell
curl http://localhost:8000/health
```

Test Processing Service:

```powershell
curl http://localhost:8001/health
```

Check Gateway readiness:

```powershell
curl http://localhost:8000/ready
```

Check Processing Service readiness:

```powershell
curl http://localhost:8001/ready
```

### Complete Project Shutdown

```powershell
docker compose down
```

For a completely fresh environment, including the database volume:

```powershell
docker compose down -v
docker compose up --build
```

### GitHub Container Registry Images

The CI/CD workflow publishes:

```text
ghcr.io/aditya045s/gateway-service
ghcr.io/aditya045s/processing-service
```

Pull the published Gateway image:

```powershell
docker pull ghcr.io/aditya045s/gateway-service:latest
```

Pull the published Processing Service image:

```powershell
docker pull ghcr.io/aditya045s/processing-service:latest
```

List the downloaded images:

```powershell
docker images
```

### Useful Debugging Commands

Check all containers:

```powershell
docker ps -a
```

Check Compose configuration:

```powershell
docker compose config
```

Check service logs:

```powershell
docker compose logs --tail=100 gateway-service
docker compose logs --tail=100 processing-service
docker compose logs --tail=100 worker
```

Check PostgreSQL:

```powershell
docker compose exec postgres pg_isready -U postgres -d jobs_db
```

Check Redis:

```powershell
docker compose exec redis redis-cli ping
```

Check the application's health endpoints:

```powershell
curl http://localhost:8000/health
curl http://localhost:8001/health
```

## Recommended Daily Docker Workflow

When working on the project, the normal sequence is:

```powershell
docker compose up --build
```

Then in another terminal:

```powershell
docker compose ps
```

Check logs when needed:

```powershell
docker compose logs --tail=100
```

After finishing:

```powershell
docker compose down
```

For a completely clean restart:

```powershell
docker compose down -v
docker compose up --build
```


## CI/CD

GitHub Actions is configured in:

```text
.github/workflows/ci.yml
```

The pipeline runs on pushes to `main` and pull requests targeting `main`.

Pipeline flow:

```text
Checkout
   |
   v
Python Setup
   |
   v
Ruff Lint
   |
   v
Ruff Format Check
   |
   v
PostgreSQL + Redis
   |
   v
Alembic Migration
   |
   v
Integration Tests
   |
   v
Docker Build
   |
   v
Publish Docker Images
```

Docker images are published to GitHub Container Registry after successful CI on `main`.

Images:

```text
ghcr.io/aditya045s/gateway-service
ghcr.io/aditya045s/processing-service
```

Images receive:

```text
latest
<commit-sha>
```

The publish step does not run for pull requests.

## Security Practices

* Secrets are supplied through environment variables.
* Real credentials must not be committed.
* Docker images do not contain production secrets.
* Gateway-to-Processing communication uses an internal bearer token.
* JWT authentication is applied at the Gateway.
* Access tokens, passwords, database credentials, and internal secrets must not be written to logs.

## Failure Scenarios Tested

The integration tests cover:

```text
Gateway job creation
Processing Service request handling
Invalid internal credential
Correlation ID propagation
Processing Service timeout
Processing Service unavailable
Database persistence
ARQ worker completion
ARQ worker failure
Idempotency replay
Idempotency conflict
Health endpoint
Readiness endpoint
Database readiness failure
Redis readiness failure
Job not found
Missing JWT
Missing idempotency key
```

## Day 8 Completion Summary

The project demonstrates:

```text
FastAPI
Microservices
Async HTTP
JWT authentication
Service-to-service authentication
PostgreSQL
SQLAlchemy
Alembic
Redis
ARQ
Background workers
Idempotency
Correlation IDs
Request IDs
Structured logging
OpenTelemetry basics
Docker
Docker Compose
Integration testing
GitHub Actions CI/CD
GitHub Container Registry
```

## Example End-to-End Flow

```text
1. Client sends POST /api/v1/jobs
2. Gateway validates JWT and Idempotency-Key
3. Gateway generates/propagates request metadata
4. Gateway calls Processing Service
5. Processing Service validates internal token
6. Job is persisted in PostgreSQL as CREATED
7. Job is queued in Redis/ARQ
8. Job becomes QUEUED
9. ARQ worker receives the job
10. Worker changes status to PROCESSING
11. Worker completes or fails the job
12. Final status becomes COMPLETED or FAILED
13. Client retrieves the job through the Gateway
```

## Health Checks

Gateway:

```text
GET http://localhost:8000/health
GET http://localhost:8000/ready
```

Processing Service:

```text
GET http://localhost:8001/health
GET http://localhost:8001/ready
```

`/health` confirms that the process is alive.

`/ready` confirms that required dependencies are available.
