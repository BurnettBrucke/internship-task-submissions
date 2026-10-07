# Internship Training Progress

This repository contains my work completed during the internship training from Day 1 to Day 8.

The projects were developed progressively, so some training days continue and upgrade the project created on an earlier day.

## Training Flow

```text
Day 1
│
├── Day-1/
│   └── Python Fundamentals
│
▼
Day 2
│
├── Day-2/
│   └── Advanced Python, File Handling & Data Processing
│
▼
Day 3
│
├── training_project/
│   └── Django Student Training Portal
│
├── Day-3/
│   └── Django ORM Query Practice
│
▼
Day 4
│
└── training_project/
    └── Role-Based Authentication, Dashboards & Bootstrap
│
▼
Day 5
│
├── training_project/
│   └── Django Project Completion, Testing & Optimization
│
└── fastapi_training/
    └── First FastAPI Student API
│
▼
Day 6
│
└── fastapi_secure_task_manager/
    └── Secure FastAPI Task Manager
│
▼
Day 7
│
└── fastapi_secure_task_manager/
    └── PostgreSQL + SQLAlchemy + Alembic + Redis Upgrade
│
▼
Day 8
│
└── final_backend_training_task/
    └── Microservices & Production Backend
```

## Day-wise Folder Mapping

| Day | Folder / Project | Work Completed |
|-----|------------------|-----------------|
| **Day 1** | `Day-1/` | Python basics, conditions, loops, strings, collections, Student Marks Manager, iterator/generator and OOP practice |
| **Day 2** | `Day-2/` | Advanced functions, `*args`, `**kwargs`, closures, decorators, JSON/file handling, CRUD, comprehensions, `map()`, `filter()`, lambda and sorting |
| **Day 3** | `training_project/` + `Day-3/` | Django Student CRUD, models and relationships, ORM queries, authentication and testing |
| **Day 4** | `training_project/` | Role-based authentication, Admin/Trainer/Student dashboards, Bootstrap templates, account security and authorization |
| **Day 5** | `training_project/` + `fastapi_training/` | Django project completion, testing, query/performance improvements, API planning and first FastAPI API |
| **Day 6** | `fastapi_secure_task_manager/` | FastAPI authentication, JWT, password hashing, RBAC, task CRUD, validation, error handling and testing |
| **Day 7** | `fastapi_secure_task_manager/` | Upgraded Day 6 project with PostgreSQL, async SQLAlchemy, Alembic, repository/service pattern, transactions, task history, indexes, pagination and Redis caching |
| **Day 8** | `final_backend_training_task/` | Gateway + Processing microservices, service communication/authentication, Redis/ARQ, Docker, observability, testing and CI/CD |

## Project Evolution

### Django Project

```text
Day 3
Student CRUD
   ↓
Models & Relationships
   ↓
ORM
   ↓
Authentication

Day 4
   ↓
Role-Based Authorization
   ↓
Dashboards
   ↓
Bootstrap / Reusable Templates

Day 5
   ↓
Testing
   ↓
Query Optimization
   ↓
Project Completion
```

**Project:** `training_project/`

---

### FastAPI Task Manager

```text
Day 6
FastAPI
   ↓
JWT Authentication
   ↓
Password Hashing
   ↓
RBAC
   ↓
Task CRUD
   ↓
Validation & Testing

Day 7
   ↓
PostgreSQL
   ↓
Async SQLAlchemy
   ↓
Alembic
   ↓
Repository + Service Layers
   ↓
Transactions + Task History
   ↓
Indexes + Pagination
   ↓
Redis Cache
```

**Project:** `fastapi_secure_task_manager/`

Day 7 is therefore an **upgrade of the Day 6 project**, not a separate project.

---

### Day 8 Final Project

```text
Client
  ↓
Gateway Service
  ↓
Processing Service
  ├── PostgreSQL
  └── Redis / ARQ Worker
```

**Project:** `final_backend_training_task/`

## Quick Links

- [Day 1](./Day-1/)
- [Day 2](./Day-2/)
- [Day 3 ORM Queries](./Day-3/orm_quries.md)
- [Django Student Training Portal](./training_project/)
- [FastAPI Training API](./fastapi_training/)
- [Secure Task Manager — Day 6 & Day 7](./fastapi_secure_task_manager/)
- [Final Backend Training Task — Day 8](./final_backend_training_task/)

## Important Note

Some folders represent multiple training days because the later day was an extension of the previous day's work.

- `training_project/` → **Days 3, 4 and 5**
- `fastapi_secure_task_manager/` → **Days 6 and 7**
- `fastapi_training/` → **Day 5**
- `final_backend_training_task/` → **Day 8**
