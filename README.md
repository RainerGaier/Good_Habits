# Prd_Twin - Personal Habit Tracker

A local-first personal habit tracking web application for building and maintaining daily habits through streak tracking, completion rates, and calendar visualization.

**Key Features**:
- Daily habit completion tracking
- Streak counts (current and best)
- Completion rate statistics
- Calendar visualization
- No account required - runs locally
- Privacy-focused - all data stays on your machine

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- uv (Python package manager)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd Prd_Twin

# Install backend dependencies
cd backend && uv sync

# Install frontend dependencies
cd frontend && npm install
```

### Development

```bash
# Start backend (terminal 1)
cd backend && uv run uvicorn app.main:app --reload --port 8000

# Start frontend (terminal 2)
cd frontend && npm run dev
```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Project Structure

```
Prd_Twin/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── .claude/          # Claude Code commands
└── docs/             # Documentation
```

## Development Workflow (PIV Loop)

This project uses a structured development workflow:

### 1. Prime - Understand Context
```bash
/prime
```
Load and understand the codebase before making changes.

### 2. Plan - Design Implementation
```bash
/plan-feature "add user authentication"
```
Create a comprehensive plan before writing code.

### 3. Execute - Implement Plan
```bash
/execute .agents/plans/add-user-authentication.md
```
Follow the plan to implement the feature.

### 4. Validate - Quality Check
```bash
/validate
/code-review
```
Run tests, linting, and review code quality.

### 5. Commit - Save Changes
```bash
/commit
```
Create atomic commits with appropriate tags.

## Bug Fix Workflow

```bash
# 1. Analyze the issue
/rca 123

# 2. Implement the fix
/implement-fix 123

# 3. Commit the fix
/commit
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/prime` | Load project context |
| `/plan-feature` | Create implementation plan |
| `/execute` | Execute a plan |
| `/validate` | Run all validations |
| `/code-review` | Review code changes |
| `/commit` | Create commit |
| `/rca` | Root cause analysis |
| `/implement-fix` | Implement bug fix |
| `/create-prd` | Generate PRD document |

## Testing

```bash
# Backend tests
cd backend && uv run pytest -v

# Frontend tests
cd frontend && npm test

# Full validation
/validate
```

## License

[Add your license here]
