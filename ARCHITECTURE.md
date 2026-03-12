# Backend Architecture: SOLID Principles and Design Patterns

This document describes how the HRMS Lite backend is structured to achieve clear separation of concerns, testability, and maintainability. The design follows SOLID principles and uses well-known patterns so that the codebase reads like production-quality, enterprise-style API code.

---

## High-Level Layered Structure

The backend is organized in distinct layers. Each layer has a single, well-defined responsibility and depends only on the layer below it. HTTP requests flow downward; data and results flow back up.

```
  HTTP Request
       │
       ▼
  api/routes/        ←  Thin controllers: parse request, call service, return response.
       │                     No business logic, no direct database access.
       ▼
  services/          ←  Business logic: validation, orchestration, domain rules.
       │                     Reusable from API, CLI, or other entry points.
       ▼
  repositories/      ←  Data access only: queries and persistence for one entity type.
       │                     No business rules; only CRUD and queries.
       ▼
  models/            ←  SQLAlchemy entity definitions (database schema).
       │
       ▼
  database           ←  SQLite or PostgreSQL (via engine and session).
```

This separation ensures that:

- **Routes** stay thin and easy to read; they only translate HTTP to service calls and responses.
- **Services** hold all business rules in one place and can be reused or tested without HTTP.
- **Repositories** encapsulate all SQL/ORM usage, so changing the database or query strategy does not affect services or routes.

---

## SOLID Principles in Practice

| Principle | How It Is Applied in This Backend |
|-----------|-----------------------------------|
| **S — Single Responsibility** | Each layer has one reason to change: routes handle HTTP, services handle business rules, repositories handle persistence. No class mixes HTTP, business logic, and database access. |
| **O — Open/Closed** | New behaviour is added by extending the system (new repository methods, new service methods, or new route handlers) rather than by modifying existing route, service, or repository code. Existing code remains stable. |
| **L — Liskov Substitution** | Repository implementations follow a common contract (e.g. `BaseRepository`). Any implementation that satisfies the contract can be substituted—for example, an in-memory repository for unit tests without touching the database. |
| **I — Interface Segregation** | Repositories expose only the methods that clients need (e.g. `get_by_pk`, `list_all`, `add`). There are no large, multi-purpose interfaces that force dependents to depend on methods they do not use. |
| **D — Dependency Inversion** | High-level modules (routes, services) depend on abstractions (repositories, services), not on low-level details. Dependencies are injected via FastAPI’s `Depends()`; wiring is centralized in `app/dependencies.py`. |

---

## Design Patterns Used

### Repository Pattern

All database access for a given entity goes through a dedicated repository class (e.g. `EmployeeRepository`, `AttendanceRepository`). Services and routes never write raw `select()` or `session.add()` for domain entities; they call repository methods such as `get_by_pk`, `list_all`, `add`, `list_filtered`. Benefits:

- One place to change how data is stored or queried.
- Easier to unit-test services by replacing repositories with in-memory or mock implementations.
- Clear, readable method names that describe intent (e.g. `exists_by_employee_id_or_email`).

### Service Layer

Business logic lives in service classes (e.g. `EmployeeService`, `AttendanceService`). Services use repositories to read and write data and enforce rules such as:

- “Employee ID and email must be unique” (duplicate check before create).
- “Attendance can only be marked for an existing employee.”
- “Only one attendance record per employee per date.”

Services are independent of HTTP; the same logic could be reused from a CLI, a background job, or another API. Routes remain thin by delegating every use case to a service method.

### Dependency Injection

FastAPI’s `Depends()` is used to inject the database session and then repositories and services that depend on it. All wiring is defined in `app/dependencies.py`:

- `get_db` provides the async database session (with commit/rollback handling).
- `get_employee_repository` and `get_attendance_repository` build repositories with that session.
- `get_employee_service` and `get_attendance_service` build services with the required repositories.

Routes declare their need for a service (e.g. `EmployeeService = Depends(get_employee_service)`); they do not instantiate repositories or services directly. This keeps the code testable and makes it easy to change how dependencies are constructed (e.g. for tests or different environments).

---

## File and Folder Responsibilities

| Path | Responsibility |
|------|----------------|
| `app/main.py` | Application creation, lifespan (e.g. create DB tables on startup), CORS configuration, and registration of API routers. No business logic. |
| `app/dependencies.py` | Definition of all injectable dependencies: `get_db`, repository getters, and service getters. Single place to change how the application is wired. |
| `app/api/routes/*.py` | HTTP request handlers only. Parse path/query/body, call the appropriate service method, and return the response (including status codes and schemas). No business rules, no direct database access. |
| `app/services/*.py` | Use cases and business logic. Call repositories to read/write data; raise domain-oriented exceptions (e.g. `EmployeeNotFoundError`, `DuplicateEmployeeError`) that are translated to HTTP errors by FastAPI. |
| `app/repositories/*.py` | Data access for one entity type. Methods perform queries and persistence using the injected session and SQLAlchemy models. No business rules. |
| `app/models/*.py` | SQLAlchemy model definitions (tables, columns, relationships). Purely structural; no application logic. |
| `app/schemas/*.py` | Pydantic models for request bodies and response bodies. Define validation rules and serialization; used by routes and FastAPI. |
| `app/core/exceptions.py` | Domain/HTTP exceptions (e.g. 404 Not Found, 409 Conflict) with consistent, user-friendly messages. Used by services and surfaced by FastAPI. |
| `app/config.py` | Configuration (e.g. database URL) loaded from environment. |
| `app/database.py` | Database engine, session factory, and base model. Provides `get_db` for dependency injection. |

---

## Summary

The backend is structured so that each part has a clear role: routes handle HTTP, services implement business rules, and repositories handle data access. SOLID principles and the Repository, Service Layer, and Dependency Injection patterns are applied consistently. This makes the codebase readable, testable, and ready for future extension without compromising existing behaviour.
