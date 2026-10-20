# People Directory — Employee Directory Search System

A full-stack employee directory application built with **React + Vite + TypeScript** (frontend) and **Python + FastAPI + SQLAlchemy** (backend), using **MySQL** as the database.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Database Choice & Design](#database-choice--design)
- [Search Performance — How It Works](#search-performance--how-it-works)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Design Decisions](#design-decisions)

---

## Overview

People Directory is an internal tool for searching and viewing company employees. Users can:

- Browse all employees with pagination
- Search by **name** or **department** (case-insensitive substring matching)
- View employee details: name, email, department, designation, and date of joining
- Experience smooth loading states, empty states, and error recovery

---

## Architecture

```
┌────────────────────┐     HTTP/JSON      ┌──────────────────────┐     SQL      ┌───────────┐
│   React Frontend   │ ──────────────────► │   FastAPI Backend    │ ──────────► │   MySQL   │
│   (Vite + TS)      │ ◄────────────────── │   (Python 3.10+)     │ ◄────────── │  Database  │
└────────────────────┘                     └──────────────────────┘             └───────────┘
     Port 5173                                  Port 8000
```

### Frontend Flow
```
User Input → SearchBar (controlled) → debounce (300ms) → TanStack Query →
  fetch() with AbortSignal → API response → cache update → EmployeeList render
```

### Backend Layers
```
Router (routes/employees.py) → Service (employee_service.py) →
  Repository (employee_repository.py) → SQLAlchemy ORM → MySQL
```

---

## Tech Stack

| Layer     | Technology                                                       |
|-----------|------------------------------------------------------------------|
| Frontend  | React 19, Vite 8, TypeScript 6, TanStack Query 5, GSAP 3       |
| Backend   | Python 3.10+, FastAPI, Pydantic 2, SQLAlchemy 2.x               |
| Database  | MySQL 8.x (with PyMySQL driver)                                  |
| Migrations| Alembic                                                          |
| Testing   | Vitest + React Testing Library (frontend), Pytest (backend)      |

---

## Prerequisites

- **Node.js** >= 18.x and npm
- **Python** >= 3.10
- **MySQL** >= 8.0 (running and accessible)

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone <repo-url>
cd resteverse
```

### 2. Database Setup (MySQL)

```sql
-- Connect to MySQL as root or an admin user
CREATE DATABASE employee_directory CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON employee_directory.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Backend Setup

```bash
cd backend

# Create and activate virtual environment (recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your actual DATABASE_URL credentials

# Run database migrations
alembic upgrade head

# Seed development data (idempotent — safe to run multiple times)
python -m app.seed
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Default values work for local development
```

---

## Running the Application

You need **two terminals** — one for the backend, one for the frontend.

### Terminal 1 — Backend (port 8000)

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend (port 5173)

```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

API documentation is available at **http://localhost:8000/docs** (Swagger UI).

---

## Running Tests

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v
```

Tests use an **in-memory SQLite database** — no MySQL required for testing.

### Frontend Tests

```bash
cd frontend
npm test
```

---

## Database Choice & Design

### Why MySQL?

MySQL was selected per the assignment requirement ("Preferably MySQL"). Additional reasons:

- **Mature and reliable** — widely used for internal tools with predictable workloads
- **Strong indexing support** — B-tree indexes on `name` and `department` columns
- **utf8mb4_0900_ai_ci collation** — provides built-in case-insensitive matching
- **Connection pooling** — SQLAlchemy's pool with `pool_pre_ping=True` handles connection lifecycle, avoiding stale connection errors after MySQL's `wait_timeout`

### Schema

```sql
CREATE TABLE employees (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(150)  NOT NULL,
    email       VARCHAR(255)  NOT NULL UNIQUE,
    department  VARCHAR(100)  NOT NULL,
    designation VARCHAR(100)  NOT NULL,
    date_of_joining DATE      NOT NULL,

    INDEX ix_employees_name (name),
    INDEX ix_employees_department (department)
);
```

### Connection Strategy

The backend uses SQLAlchemy's connection pool with:
- `pool_size=5` — appropriate for a small internal tool
- `max_overflow=10` — handles burst traffic
- `pool_recycle=1800` — prevents MySQL `wait_timeout` disconnects
- `pool_pre_ping=True` — validates connections before use

This approach is suitable because it reuses database connections across requests (avoiding the overhead of creating a new connection per request) while ensuring stale connections are detected and replaced.

---

## Search Performance — How It Works

### Frontend Optimization

1. **Debouncing (300ms):** Typing "Rahul" does NOT trigger 5 API calls. The `useDebouncedValue` hook waits until the user stops typing for 300ms before issuing a request.

2. **Request cancellation:** When a new search term is entered before the previous request completes, TanStack Query passes an `AbortSignal` to the `fetch()` call, cancelling the obsolete request. This prevents stale results from overwriting newer ones.

3. **Cache-first strategy:** TanStack Query caches results keyed by `[search, limit, offset]`. Repeat searches return instantly from cache (`staleTime: 30s`).

4. **`keepPreviousData`:** While new results load, the previous results remain visible — avoiding a flash of empty content.

### Backend Optimization

1. **Parameterized queries:** All search queries use SQLAlchemy's parameterized expressions — never string concatenation. This prevents SQL injection and allows the database to reuse query plans.

2. **Bounded results:** Every query uses `LIMIT` (max 100) and `OFFSET` with a deterministic `ORDER BY id` for stable pagination.

3. **Indexes:** B-tree indexes on `name` and `department` columns.

4. **Count optimization:** The total count query uses the same filters as the data query, ensuring the count accurately reflects the filtered dataset.

### Index Trade-offs (Important)

The search uses `LIKE '%term%'` (substring matching) for usability — users expect "rah" to match "Rahul" anywhere in the name.

**B-tree indexes cannot accelerate leading-wildcard LIKE patterns** (`%term%`). MySQL must scan the index or table for these queries. For the expected dataset size of an internal company directory (hundreds to low tens of thousands of employees), this is perfectly acceptable — the query completes in single-digit milliseconds.

For datasets exceeding ~100k rows, consider:
- **MySQL FULLTEXT indexes** with `MATCH ... AGAINST` for natural language search
- **Prefix-only search** (`LIKE 'term%'`) which CAN use B-tree indexes efficiently
- An external search engine (Elasticsearch) — overkill for this use case

The current approach was chosen because it provides the best user experience (substring matching) with acceptable performance for the intended scale.

---

## API Documentation

### `GET /api/v1/employees`

Search employees by name or department with pagination.

**Query Parameters:**

| Parameter | Type   | Default | Constraints   | Description                         |
|-----------|--------|---------|---------------|-------------------------------------|
| `search`  | string | `""`    | max 100 chars | Search term (name or department)    |
| `limit`   | int    | `20`    | 1–100         | Results per page                    |
| `offset`  | int    | `0`     | >= 0          | Number of results to skip           |

**Response (200):**

```json
{
  "items": [
    {
      "id": 1,
      "name": "Rahul Sharma",
      "email": "rahul.sharma@company.com",
      "department": "Engineering",
      "designation": "Senior Software Engineer",
      "date_of_joining": "2021-03-15"
    }
  ],
  "total": 25,
  "limit": 20,
  "offset": 0
}
```

**Error Responses:**

| Status | Meaning                              |
|--------|--------------------------------------|
| `422`  | Invalid query parameters             |
| `503`  | Database temporarily unavailable     |
| `500`  | Unexpected server error              |

### `GET /api/v1/health`

Health check endpoint. Returns database connectivity status.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable          | Required | Default                                                       | Description                    |
|-------------------|----------|---------------------------------------------------------------|--------------------------------|
| `DATABASE_URL`    | Yes      | `mysql+pymysql://app_user:change_me@localhost:3306/employee_directory` | MySQL connection string |
| `APP_ENV`         | No       | `development`                                                 | Environment name               |
| `CORS_ORIGINS`    | No       | `http://localhost:5173`                                       | Comma-separated allowed origins|
| `LOG_LEVEL`       | No       | `INFO`                                                        | Logging level                  |
| `DB_POOL_SIZE`    | No       | `5`                                                           | Connection pool size           |
| `DB_MAX_OVERFLOW` | No       | `10`                                                          | Max overflow connections       |
| `DB_POOL_RECYCLE` | No       | `1800`                                                        | Connection recycle time (sec)  |

### Frontend (`frontend/.env`)

| Variable             | Required | Default                           | Description      |
|----------------------|----------|-----------------------------------|------------------|
| `VITE_API_BASE_URL`  | Yes      | `http://localhost:8000/api/v1`    | Backend API URL  |

> **Note:** `VITE_`-prefixed variables are embedded in the client bundle and are public. Never put secrets in frontend env vars.

---

## Project Structure

```
resteverse/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app factory
│   │   ├── seed.py                    # Development data seeder
│   │   ├── core/
│   │   │   ├── config.py              # Pydantic settings
│   │   │   └── logging.py            # Structured logging
│   │   ├── api/
│   │   │   ├── router.py             # Route aggregation
│   │   │   └── routes/
│   │   │       ├── employees.py       # Employee search endpoint
│   │   │       └── health.py          # Health check
│   │   ├── schemas/
│   │   │   └── employee.py            # Request/response schemas
│   │   ├── models/
│   │   │   └── employee.py            # ORM model
│   │   ├── services/
│   │   │   └── employee_service.py    # Business logic
│   │   ├── repositories/
│   │   │   └── employee_repository.py # Database queries
│   │   └── db/
│   │       ├── base.py                # Declarative base
│   │       └── session.py             # Engine & session
│   ├── tests/
│   │   ├── conftest.py                # Test fixtures
│   │   └── test_employees.py          # API tests (19 tests)
│   ├── alembic/                       # Database migrations
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── main.tsx                   # Entry point + providers
│   │   ├── App.tsx                    # Root component
│   │   ├── index.css                  # Design system & styles
│   │   ├── components/
│   │   │   ├── SearchBar.tsx          # Search input component
│   │   │   ├── EmployeeCard.tsx       # Employee display card
│   │   │   ├── EmployeeList.tsx       # Card grid with GSAP animation
│   │   │   ├── EmptyState.tsx         # No results state
│   │   │   ├── ErrorState.tsx         # Error + retry state
│   │   │   └── Pagination.tsx         # Page navigation
│   │   ├── hooks/
│   │   │   └── useEmployeeSearch.ts   # Search hook with debounce
│   │   ├── api/
│   │   │   └── employees.ts           # API client
│   │   ├── config/
│   │   │   └── env.ts                 # Environment config
│   │   ├── types/
│   │   │   └── employee.ts            # TypeScript types
│   │   └── test/
│   │       ├── setup.ts               # Test setup
│   │       └── App.test.tsx           # Component tests (22 tests)
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── .env.example
│   └── index.html
└── README.md
```

---

## Design Decisions

| Decision                    | Rationale                                                                                    |
|-----------------------------|----------------------------------------------------------------------------------------------|
| **TanStack Query**          | Manages caching, request deduplication, AbortSignal cancellation, and retry logic out of the box |
| **300ms debounce**          | Balances responsiveness with request reduction — prevents per-keystroke API calls              |
| **Substring search (`LIKE '%term%'`)** | Best UX for a directory tool — users search partial names. Prefix-only is too restrictive |
| **GSAP for card animations** | Stagger entrance animation adds polish without blocking interactivity. Respects `prefers-reduced-motion` |
| **In-memory SQLite for tests** | Fast, isolated test runs without requiring MySQL. Dependency override injects the test session |
| **Repository pattern**      | Isolates SQL from business logic. Service layer coordinates, repository builds queries        |
| **Pydantic Settings**       | Validates env vars at startup with type safety — fast failure on misconfiguration              |
| **`pool_pre_ping=True`**    | Detects dead MySQL connections before they cause 500 errors                                   |
| **Alembic migrations**      | Schema changes are versioned and repeatable — no reliance on ORM auto-create                  |
