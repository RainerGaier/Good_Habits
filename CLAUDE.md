# Prd_Twin - Personal Habit Tracker

A local-first personal habit tracking web application for building and maintaining daily habits through streak tracking, completion rates, and calendar visualization. Built with FastAPI (backend) and React (frontend), this application runs entirely on your machine with no account required.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLite, SQLAlchemy
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS
- **Testing**: pytest (backend), vitest (frontend)
- **Linting**: ruff (Python), ESLint (TypeScript)
- **Package Management**: uv (Python), npm (Node.js)

## Project Structure

```
Prd_Twin/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Core config and utilities
│   │   ├── models/        # SQLAlchemy models
│   │   └── services/      # Business logic
│   ├── tests/             # Backend tests
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom hooks
│   │   └── services/      # API services
│   ├── tests/             # Frontend tests
│   └── package.json
├── .claude/
│   ├── commands/          # Claude slash commands
│   └── reference/         # Best practices docs
├── .agents/
│   ├── plans/             # Feature implementation plans
│   ├── code-reviews/      # Code review reports
│   ├── execution-reports/ # Implementation reports
│   └── system-reviews/    # Process review reports
└── docs/
    └── rca/               # Root cause analysis docs
```

## Commands

```bash
# Install backend dependencies
cd backend && uv sync

# Install frontend dependencies
cd frontend && npm install

# Run backend development server
cd backend && uv run uvicorn app.main:app --reload --port 8000

# Run frontend development server
cd frontend && npm run dev

# Run backend tests
cd backend && uv run pytest -v

# Run frontend tests
cd frontend && npm test

# Lint backend
cd backend && uv run ruff check .

# Lint frontend
cd frontend && npm run lint
```

## Claude Slash Commands

| Command | Purpose |
|---------|---------|
| `/prime` | Load project context and understand codebase |
| `/plan-feature <feature>` | Create comprehensive implementation plan |
| `/execute <plan-path>` | Execute an implementation plan |
| `/validate` | Run all validation (lint, type check, tests) |
| `/code-review` | Review changed files for issues |
| `/code-review-fix <file>` | Fix issues from code review |
| `/execution-report` | Generate post-implementation report |
| `/system-review <plan> <report>` | Analyze implementation vs plan |
| `/rca <issue-id>` | Root cause analysis for GitHub issue |
| `/implement-fix <issue-id>` | Implement fix from RCA document |
| `/commit` | Create atomic commit with tag |
| `/init-project` | Initialize and start project locally |
| `/create-prd <filename>` | Generate Product Requirements Document |

## Reference Documentation

| Document | When to Read |
|----------|--------------|
| `.claude/reference/fastapi-best-practices.md` | Backend API development |
| `.claude/reference/react-frontend-best-practices.md` | Frontend development |
| `.claude/reference/sqlite-best-practices.md` | Database operations |
| `.claude/reference/testing-and-logging.md` | Writing tests, logging setup |

## Code Conventions

### Backend (Python)
- Use type hints for all function parameters and return values
- Follow PEP 8 style guide (enforced by ruff)
- Use async/await for database operations
- Structured logging with structlog
- Pydantic models for request/response validation

### Frontend (TypeScript)
- Functional components with hooks
- TypeScript strict mode
- Props interfaces for all components
- Custom hooks for reusable logic
- TailwindCSS for styling

### API Design
- RESTful endpoints
- Consistent error response format
- Pydantic schemas for validation
- OpenAPI documentation auto-generated

## Logging

Backend uses structlog for structured logging:
```python
import structlog
logger = structlog.get_logger()
logger.info("event_name", key="value")
```

## Database

- SQLite for development
- SQLAlchemy ORM with async support
- Alembic for migrations

## Testing Strategy

### Testing Pyramid
- **Unit tests**: Individual functions and classes
- **Integration tests**: API endpoints with database
- **E2E tests**: Full user flows (optional with Playwright)

### Test Organization
```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # API and database tests
└── conftest.py     # Shared fixtures
```
