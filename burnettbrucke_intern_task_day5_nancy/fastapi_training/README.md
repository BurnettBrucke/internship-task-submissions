# Student Training Portal API (FastAPI)

A small, standalone FastAPI project that rebuilds a slice of the Django
Student Training Portal's student CRUD as an API — built to practice
FastAPI's core mechanics alongside the full Django project. Data is stored
**in-memory** (a plain Python dict, see `app/services.py`) — nothing here
persists across a server restart, and there's no relationship to the Django
project's actual database. See `training_project/api_design.md` for how a
*complete* API over the real Django models would be planned (auth,
permissions, all resources) — this project is deliberately just the
`/students` slice, to focus on learning FastAPI itself.

## Project structure

```
fastapi_training/
    app/
        __init__.py
        main.py       # routes only
        schemas.py    # Pydantic request/response models
        services.py   # in-memory data operations
    tests/
        test_main.py  # 23 pytest tests
    requirements.txt
    README.md
```

## Setup and run

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Then open:
- **Swagger UI** (interactive, try-it-yourself docs): http://127.0.0.1:8000/docs
- **ReDoc** (read-only, cleaner reference docs): http://127.0.0.1:8000/redoc

Both are generated automatically from the route type hints and Pydantic
models in `app/main.py`/`app/schemas.py` — nothing here manually maintains
a docs page.

## Run the tests

```bash
pytest tests/ -v
```

23 tests, covering health, full CRUD, validation (age/marks/email bounds),
filtering, pagination, and 404 handling.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Application status |
| GET | `/students` | List students (query params: `skip`, `limit`, `is_active`, `min_marks`) |
| GET | `/students/{student_id}` | Retrieve one student (404 if missing) |
| POST | `/students` | Create a student |
| PATCH | `/students/{student_id}` | Partially update a student (404 if missing) |
| DELETE | `/students/{student_id}` | Delete a student (404 if missing) |

### Example requests

```bash
curl http://127.0.0.1:8000/health

curl http://127.0.0.1:8000/students

curl "http://127.0.0.1:8000/students?is_active=true&min_marks=50&skip=0&limit=10"

curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "New Student", "email": "new@example.com", "age": 22, "marks": 65}'

curl -X PATCH http://127.0.0.1:8000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"marks": 80}'

curl -X DELETE http://127.0.0.1:8000/students/1
```

### Validation rules

- `age`: 16–60
- `marks`: 0–100
- `email`: must be a syntactically valid email address (`pydantic[email]`)
- `name`: 2–100 characters

Invalid input returns `422 Unprocessable Entity` with a field-by-field
error body — FastAPI generates this automatically from the `Field(...)`
constraints in `app/schemas.py`; no manual validation code was written for
these rules.

## FastAPI concepts demonstrated

- **Application instance and route decorators** — `app = FastAPI()`, `@app.get`/`@app.post`/`@app.patch`/`@app.delete`
- **Path parameters** — `{student_id}` in the URL, typed as `int`
- **Query parameters** — `skip`, `limit`, `is_active`, `min_marks` in `list_students`, using `Query(...)` for extra constraints (`ge=0`, `le=100`)
- **Request bodies** — `StudentCreate`/`StudentUpdate` as typed function parameters
- **Pydantic models** — all schemas in `app/schemas.py`
- **Response models** — `response_model=StudentResponse` etc. on every route, so the response shape is validated and documented, not just whatever the function happens to return
- **HTTP status codes** — `201` on create, `204` on delete, `404` via `HTTPException`, `422` automatic on validation failure
- **Automatic docs** — Swagger UI (`/docs`) and ReDoc (`/redoc`), generated with zero extra code

## Django vs FastAPI — comparison

| Area | Django | FastAPI |
|---|---|---|
| Primary strength | Full web framework (templates, auth, admin, ORM, sessions) | API-focused framework |
| Data validation | Forms/ModelForms, or DRF serializers if using Django REST Framework | Pydantic models — built in, type-hint-driven |
| Admin panel | Built in (`/admin/`) | Not built in |
| Templates | Built in (Django Template Language) | Optional / not the focus — typically paired with a separate frontend |
| API documentation | Usually added via DRF + drf-spectacular or similar | Automatic OpenAPI/Swagger + ReDoc, no extra packages |
| Typical use | Full web applications with a UI | APIs and backend services |
| Testing | `django.test.TestCase` + test client | `TestClient` (Starlette/httpx-based) + pytest |
| Async support | Improving each release, but the ORM and much of the ecosystem is still primarily sync | Async-first from the ground up |
| This project's usage | The full Student Training Portal — auth, roles, dashboards, templates | Just the `/students` CRUD slice, in-memory, to practice the framework |

**In short:** the Django project in `training_project/` is the actual
application — it owns the real data, the UI, and the permission system.
This FastAPI project is a focused exercise in a different framework's way
of building an API, not a replacement for or a live connection to the
Django app.

## Known limitations of this exercise project

- **In-memory storage only** — data resets every time the server restarts.
  A real version would use a database (and could reuse the Django project's
  `Student` model via a shared database, or its own).
- **No authentication or permissions** — every endpoint is open. The
  Django project's role/ownership system (`students/decorators.py`,
  `students/services.py`) is *not* replicated here; see `api_design.md`
  for how it would be if this became a real API over the Django data.
- **No pagination `next`/`previous` links** — `skip`/`limit` are returned
  as-is rather than computed follow-up URLs, to keep the exercise focused
  on the required FastAPI concepts.
