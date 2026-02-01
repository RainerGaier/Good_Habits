# Prd_Twin - Personal Habit Tracker

## 1. Executive Summary

Prd_Twin is a personal habit tracking web application designed for building and maintaining daily habits through intuitive streak tracking, completion rate analytics, and calendar visualization. The application prioritizes simplicity and privacy by running entirely on the user's local machine with no account registration required.

Unlike cloud-based habit trackers that require subscriptions and store personal data on remote servers, Prd_Twin offers a distraction-free experience focused purely on the core functionality of habit formation. Users can track unlimited habits, visualize their progress over time, and maintain motivation through streak counts—all without internet connectivity after initial setup.

**MVP Goal**: Deliver a fully functional local habit tracking application with core CRUD operations, streak calculation, completion statistics, and a calendar view for habit history visualization.

## 2. Mission

**Mission Statement**: Empower individuals to build lasting positive habits through simple, private, and distraction-free tracking tools that respect user privacy and work offline.

**Core Principles**:
1. **Privacy First** - All data stays on the user's machine; no telemetry, no accounts, no cloud sync
2. **Simplicity Over Features** - Focus on essential habit tracking without feature bloat
3. **Offline Capable** - Full functionality without internet after initial setup
4. **Fast and Responsive** - Instant feedback for habit check-ins and navigation
5. **Data Ownership** - Users can easily export, backup, and manage their own data

## 3. Target Users

**Primary Persona: The Intentional Self-Improver**
- Age: 25-45
- Wants to build positive daily routines (exercise, reading, meditation, etc.)
- Values privacy and dislikes creating accounts for simple tools
- Comfortable running local applications
- Prefers clean, minimal interfaces over gamified experiences
- May have tried other habit apps but found them too complex or intrusive

**Technical Comfort Level**: Intermediate
- Can install and run local development tools
- Comfortable with web browsers
- May or may not be technical professionals

**Key Needs and Pain Points**:
- Tired of habit apps requiring accounts and subscriptions
- Wants to see progress at a glance without navigating complex dashboards
- Needs motivation through visible streaks and completion rates
- Prefers data stored locally rather than in the cloud
- Values quick daily check-ins (< 30 seconds)

## 4. MVP Scope

### In Scope (MVP)

**Core Functionality**:
- [x] Create, read, update, delete habits
- [x] Daily habit completion tracking (check/uncheck)
- [x] Streak calculation and display (current streak, best streak)
- [x] Completion rate statistics (weekly, monthly, all-time)
- [x] Calendar view showing habit completion history with color-coded days
- [x] Today view with all habits and quick check-in
- [x] Planned absences - skip days without breaking streaks (vacation, sick days)

**Technical**:
- [x] FastAPI REST API backend
- [x] SQLite database for local storage
- [x] React frontend with TypeScript
- [x] Responsive design (desktop and tablet)
- [x] API documentation via OpenAPI/Swagger

**Data Management**:
- [x] Automatic data persistence to local SQLite
- [x] Data stored in user-accessible location

### Out of Scope (Future Phases)

**Deferred Features**:
- [ ] Mobile-specific PWA optimizations
- [ ] Data export/import (JSON, CSV)
- [ ] Habit categories and tagging
- [ ] Habit archiving
- [ ] Multiple completion types (numeric, time-based)
- [ ] Reminders and notifications
- [ ] Dark mode theme
- [ ] Weekly/custom frequency habits (non-daily)
- [ ] Habit notes and journaling
- [ ] Goal setting and milestones
- [ ] Charts and trend graphs
- [ ] Multi-device sync
- [ ] Habit templates

## 5. User Stories

### Primary User Stories

**US-1: Create a New Habit**
> As a user, I want to create a new habit with a name and optional description, so that I can start tracking it daily.

*Example*: User clicks "Add Habit", enters "Morning Meditation" with description "10 minutes of mindfulness", and saves.

**US-2: Complete a Habit for Today**
> As a user, I want to mark a habit as complete for today with a single click, so that I can quickly record my progress.

*Example*: User sees "Morning Meditation" in today's list, clicks the checkbox, and sees it marked as complete with updated streak.

**US-3: View Current Streaks**
> As a user, I want to see my current streak for each habit, so that I stay motivated to maintain my progress.

*Example*: User sees "Morning Meditation: 🔥 7 days" indicating 7 consecutive days of completion.

**US-4: View Completion Statistics**
> As a user, I want to see my completion rate for each habit, so that I understand my consistency over time.

*Example*: User sees "Morning Meditation: 85% this month, 72% all-time" with visual indicators.

**US-5: View Calendar History**
> As a user, I want to see a calendar view of my habit completions, so that I can visualize patterns and gaps.

*Example*: User opens calendar view for "Morning Meditation" and sees green dots on completed days, empty on missed days.

**US-6: Edit an Existing Habit**
> As a user, I want to edit a habit's name or description, so that I can refine my tracking over time.

*Example*: User changes "Morning Meditation" to "Morning Meditation (15 min)" after increasing duration.

**US-7: Delete a Habit**
> As a user, I want to delete a habit I no longer want to track, so that my list stays relevant.

*Example*: User deletes "Learn Spanish" habit after completing their goal, with confirmation prompt.

**US-8: View Today's Overview**
> As a user, I want to see all my habits for today on one screen, so that I can quickly check in and track progress.

*Example*: User opens app and immediately sees today's date, all habits with completion status, and overall daily progress.

**US-9: Mark Planned Absence**
> As a user, I want to mark specific days as planned absences, so that my streak doesn't break when I'm on vacation or sick.

*Example*: User is going on vacation for a week. They mark Jan 15-22 as "planned absence" for all habits. When they return, their streak continues from where it left off.

**US-10: View Absence in Calendar**
> As a user, I want to see planned absences displayed differently in the calendar, so that I can distinguish them from missed days.

*Example*: Calendar shows completed days in green, planned absences in gray/neutral, and missed days as empty/red.

### Technical User Stories

**US-T1: Persist Data Locally**
> As a user, I want my habit data saved automatically, so that I don't lose progress if I close the browser.

**US-T2: Fast Load Times**
> As a user, I want the application to load in under 2 seconds, so that daily check-ins feel instant.

## 6. Core Architecture & Patterns

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Today   │  │  Habits  │  │ Calendar │              │
│  │   View   │  │   List   │  │   View   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │             │             │                     │
│       └─────────────┼─────────────┘                     │
│                     │                                   │
│              ┌──────┴──────┐                           │
│              │  API Client │                           │
│              └──────┬──────┘                           │
└─────────────────────┼───────────────────────────────────┘
                      │ HTTP/JSON
┌─────────────────────┼───────────────────────────────────┐
│                     │         FastAPI Backend           │
│              ┌──────┴──────┐                           │
│              │   Routers   │                           │
│              │ /habits     │                           │
│              │ /completions│                           │
│              └──────┬──────┘                           │
│                     │                                   │
│              ┌──────┴──────┐                           │
│              │  Services   │                           │
│              │ HabitService│                           │
│              │ StatsService│                           │
│              └──────┬──────┘                           │
│                     │                                   │
│              ┌──────┴──────┐                           │
│              │   Models    │                           │
│              │  SQLAlchemy │                           │
│              └──────┬──────┘                           │
│                     │                                   │
└─────────────────────┼───────────────────────────────────┘
                      │
               ┌──────┴──────┐
               │   SQLite    │
               │  Database   │
               └─────────────┘
```

### Directory Structure

```
Prd_Twin/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── habits.py        # Habit CRUD endpoints
│   │   │   ├── completions.py   # Completion tracking endpoints
│   │   │   ├── absences.py      # Planned absence endpoints
│   │   │   └── stats.py         # Statistics endpoints
│   │   ├── core/
│   │   │   ├── config.py        # App configuration
│   │   │   ├── database.py      # Database connection
│   │   │   └── logging.py       # Structured logging
│   │   ├── models/
│   │   │   ├── habit.py         # Habit SQLAlchemy model
│   │   │   ├── completion.py    # Completion SQLAlchemy model
│   │   │   └── absence.py       # Absence SQLAlchemy model
│   │   ├── schemas/
│   │   │   ├── habit.py         # Habit Pydantic schemas
│   │   │   ├── completion.py    # Completion Pydantic schemas
│   │   │   └── absence.py       # Absence Pydantic schemas
│   │   ├── services/
│   │   │   ├── habit_service.py # Habit business logic
│   │   │   └── stats_service.py # Statistics & streak calculations
│   │   └── main.py
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HabitCard.tsx
│   │   │   ├── HabitForm.tsx
│   │   │   ├── Calendar.tsx
│   │   │   ├── StreakBadge.tsx
│   │   │   └── CompletionCheckbox.tsx
│   │   ├── pages/
│   │   │   ├── TodayPage.tsx
│   │   │   ├── HabitsPage.tsx
│   │   │   └── CalendarPage.tsx
│   │   ├── hooks/
│   │   │   ├── useHabits.ts
│   │   │   └── useCompletions.ts
│   │   └── services/
│   │       └── api.ts
│   └── tests/
└── docs/
```

### Key Design Patterns

**Backend**:
- Repository pattern for data access
- Service layer for business logic
- Pydantic schemas for validation and serialization
- Dependency injection for database sessions

**Frontend**:
- Custom hooks for data fetching and state
- Component composition for reusability
- Optimistic UI updates for responsiveness

## 7. Features Specification

### Feature: Habit Management

**Purpose**: Allow users to create and manage their habits

**Operations**:
| Operation | Endpoint | Description |
|-----------|----------|-------------|
| List | GET /api/habits | Get all habits with current stats |
| Create | POST /api/habits | Create a new habit |
| Read | GET /api/habits/{id} | Get habit details |
| Update | PUT /api/habits/{id} | Update habit name/description |
| Delete | DELETE /api/habits/{id} | Delete habit and completions |

**Habit Fields**:
- `id`: UUID, auto-generated
- `name`: string, required, max 100 chars
- `description`: string, optional, max 500 chars
- `created_at`: datetime, auto-generated
- `updated_at`: datetime, auto-updated

### Feature: Completion Tracking

**Purpose**: Record daily habit completions

**Operations**:
| Operation | Endpoint | Description |
|-----------|----------|-------------|
| Complete | POST /api/habits/{id}/complete | Mark habit complete for date |
| Undo | DELETE /api/habits/{id}/completions/{date} | Remove completion for date |
| History | GET /api/habits/{id}/completions | Get completions for date range |

**Completion Fields**:
- `id`: UUID, auto-generated
- `habit_id`: UUID, foreign key
- `completed_date`: date, required
- `created_at`: datetime, auto-generated

**Business Rules**:
- One completion per habit per day (unique constraint)
- POST creates completion, DELETE removes it (explicit actions)
- Default to today's date if not specified in POST
- Attempting to complete an already-completed day returns existing completion

### Feature: Planned Absences

**Purpose**: Allow users to skip days without breaking streaks

**Operations**:
| Operation | Endpoint | Description |
|-----------|----------|-------------|
| Create | POST /api/habits/{id}/absences | Mark date as planned absence |
| Remove | DELETE /api/habits/{id}/absences/{date} | Remove planned absence |
| History | GET /api/habits/{id}/absences | Get absences for date range |

**Absence Fields**:
- `id`: UUID, auto-generated
- `habit_id`: UUID, foreign key
- `absence_date`: date, required
- `reason`: string, optional (e.g., "vacation", "sick")
- `created_at`: datetime, auto-generated

**Business Rules**:
- Absences can be set for past, present, or future dates
- A day with an absence is treated as "neutral" - doesn't break streak, doesn't count toward completion rate
- If both completion and absence exist for same day, completion takes precedence
- Absences apply per-habit (user might skip gym but not meditation)

### Feature: Streak Calculation

**Purpose**: Calculate and display consecutive completion streaks

**Streak Types**:
- **Current Streak**: Consecutive days ending today (or yesterday if today incomplete)
- **Best Streak**: Longest consecutive streak ever achieved

**Calculation Rules**:
- A day counts as "valid" if: completion exists OR planned absence exists
- Streak breaks only on days with NO completion AND NO absence
- Current streak includes today only if completed (absences don't extend streak, just preserve it)
- Absences are "skipped" in streak calculation - they don't add to the count but don't break it

### Feature: Completion Statistics

**Purpose**: Provide completion rate analytics

**Statistics Provided**:
- **Today**: Completed, absent, or pending
- **This Week**: X/Y days (percentage) - Y excludes absence days
- **This Month**: X/Y days (percentage) - Y excludes absence days
- **All Time**: Total completions / (total days - absence days)

**Calculation Note**: Absence days are excluded from the denominator. If a user has a habit for 30 days but was absent for 5, the completion rate is calculated against 25 days.

### Feature: Calendar View

**Purpose**: Visualize habit completion history

**Functionality**:
- Monthly calendar grid
- Color-coded visual indicators:
  - **Green**: Completed days
  - **Gray/Neutral**: Planned absences
  - **Empty/Light**: Missed days (no completion, no absence)
- Navigate between months
- Click on day to toggle completion (past dates allowed)
- Long-press or secondary action to mark as planned absence

## 8. Technology Stack

### Backend
- **Runtime**: Python 3.11+
- **Framework**: FastAPI 0.109+
- **ORM**: SQLAlchemy 2.0+ (async)
- **Database**: SQLite with aiosqlite
- **Validation**: Pydantic 2.5+
- **Logging**: structlog

### Frontend
- **Runtime**: Node.js 18+
- **Framework**: React 18
- **Language**: TypeScript 5.2+
- **Build Tool**: Vite 5
- **Styling**: TailwindCSS 3
- **HTTP Client**: Fetch API (native)

### Development Tools
- **Python Package Manager**: uv
- **Node Package Manager**: npm
- **Linting (Python)**: ruff
- **Linting (TypeScript)**: ESLint
- **Testing (Python)**: pytest
- **Testing (TypeScript)**: vitest

## 9. Security & Configuration

### Security Scope

**In Scope**:
- Input validation on all endpoints
- SQL injection prevention via ORM
- CORS configuration for local development

**Out of Scope (Local-Only App)**:
- Authentication/authorization
- HTTPS (local HTTP acceptable)
- Rate limiting
- CSRF protection

### Configuration

**Environment Variables** (`.env`):
```
DATABASE_URL=sqlite+aiosqlite:///./habits.db
CORS_ORIGINS=["http://localhost:5173"]
DEBUG=true
```

### Data Storage
- SQLite database file stored in project directory
- User can backup by copying the `.db` file
- No encryption (local trusted environment)

## 10. API Specification

### Base URL
```
http://localhost:8000/api
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/habits | List all habits with stats |
| POST | /api/habits | Create a new habit |
| PUT | /api/habits/{id} | Update a habit |
| DELETE | /api/habits/{id} | Delete a habit |
| POST | /api/habits/{id}/complete | Mark habit complete for a date |
| DELETE | /api/habits/{id}/completions/{date} | Undo a completion |
| GET | /api/habits/{id}/completions | Get completion history |
| POST | /api/habits/{id}/absences | Mark planned absence(s) |
| DELETE | /api/habits/{id}/absences/{date} | Remove a planned absence |
| GET | /api/habits/{id}/absences | Get absence history |

#### Habits

**GET /api/habits**
```json
// Response 200
[
  {
    "id": "uuid",
    "name": "Morning Meditation",
    "description": "10 minutes of mindfulness",
    "created_at": "2024-01-01T00:00:00Z",
    "current_streak": 7,
    "best_streak": 14,
    "completion_rate": {
      "week": 85.7,
      "month": 80.0,
      "all_time": 75.5
    },
    "completed_today": true
  }
]
```

**POST /api/habits**
```json
// Request
{
  "name": "Morning Meditation",
  "description": "10 minutes of mindfulness"
}

// Response 201
{
  "id": "uuid",
  "name": "Morning Meditation",
  "description": "10 minutes of mindfulness",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**PUT /api/habits/{id}**
```json
// Request
{
  "name": "Morning Meditation (15 min)",
  "description": "15 minutes of mindfulness"
}

// Response 200
{
  "id": "uuid",
  "name": "Morning Meditation (15 min)",
  "description": "15 minutes of mindfulness",
  "updated_at": "2024-01-15T00:00:00Z"
}
```

**DELETE /api/habits/{id}**
```json
// Response 204 No Content
```

#### Completions

**POST /api/habits/{id}/complete**
```json
// Request (optional date, defaults to today)
{
  "date": "2024-01-15"
}

// Response 201
{
  "habit_id": "uuid",
  "date": "2024-01-15",
  "completed": true
}
```

**DELETE /api/habits/{id}/completions/{date}**
```json
// Response 204 No Content
```

**GET /api/habits/{id}/completions**
```json
// Query params: ?start_date=2024-01-01&end_date=2024-01-31

// Response 200
{
  "habit_id": "uuid",
  "completions": ["2024-01-01", "2024-01-02", "2024-01-05", "2024-01-06"]
}
```

#### Absences

**POST /api/habits/{id}/absences**
```json
// Request
{
  "date": "2024-01-15",
  "reason": "vacation"
}

// Response 201
{
  "habit_id": "uuid",
  "date": "2024-01-15",
  "reason": "vacation"
}
```

**DELETE /api/habits/{id}/absences/{date}**
```json
// Response 204 No Content
```

**GET /api/habits/{id}/absences**
```json
// Query params: ?start_date=2024-01-01&end_date=2024-01-31

// Response 200
{
  "habit_id": "uuid",
  "absences": [
    {"date": "2024-01-15", "reason": "vacation"},
    {"date": "2024-01-16", "reason": "vacation"}
  ]
}
```

### Error Responses

```json
// 404 Not Found
{
  "detail": "Habit not found"
}

// 422 Validation Error
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## 11. Success Criteria

### MVP Success Definition
The MVP is successful when a user can:
1. Create habits and track daily completions
2. See accurate streak counts that motivate continued use
3. View completion statistics and calendar history
4. Complete all actions in under 2 seconds

### Functional Requirements

- [x] User can create a habit with name and optional description
- [x] User can mark habits complete for any date
- [x] User can see current streak for each habit
- [x] User can see best streak for each habit
- [x] User can see completion rates (week, month, all-time)
- [x] User can view monthly calendar with completion history
- [x] User can edit habit details
- [x] User can delete habits
- [x] Data persists between sessions

### Quality Indicators

- API response time < 100ms for all endpoints
- Frontend initial load < 2 seconds
- Zero data loss on normal application close
- Works offline after initial load (frontend cached)

### User Experience Goals

- Daily check-in takes < 30 seconds
- Streak and stats visible without navigation
- Calendar view loads instantly
- Mobile-friendly responsive design

## 12. Implementation Phases

### Phase 1: Foundation
**Goal**: Basic backend API and database

**Deliverables**:
- [x] SQLite database setup with SQLAlchemy
- [x] Habit model and CRUD endpoints
- [x] Completion model and toggle endpoint
- [x] Basic API tests

**Validation**: All API endpoints return correct responses via Swagger UI

### Phase 2: Core Logic
**Goal**: Streak and statistics calculation

**Deliverables**:
- [x] Streak calculation service
- [x] Completion rate statistics service
- [x] Enhanced habit list endpoint with stats
- [x] Date range completion query

**Validation**: Unit tests pass for streak edge cases (gaps, today incomplete, etc.)

### Phase 3: Frontend MVP
**Goal**: Functional React frontend

**Deliverables**:
- [x] Today page with habit list and quick completion
- [x] Habit management (create, edit, delete)
- [x] Streak and stats display
- [x] Basic styling with TailwindCSS

**Validation**: User can complete full habit tracking workflow

### Phase 4: Calendar & Polish
**Goal**: Calendar view and UX refinement

**Deliverables**:
- [x] Calendar component with month navigation
- [x] Click-to-toggle past completions
- [x] Loading states and error handling
- [x] Responsive design verification

**Validation**: End-to-end testing of all user flows

## 13. Future Considerations

### Post-MVP Enhancements

**Data Portability**:
- JSON/CSV export
- Import from other habit trackers
- Backup/restore functionality

**Enhanced Tracking**:
- Weekly habits (e.g., "Exercise 3x per week")
- Numeric habits (e.g., "Drink 8 glasses of water")
- Time-based habits (e.g., "Read for 30 minutes")

**Organization**:
- Habit categories/tags
- Habit archiving
- Custom sort order

**Visualization**:
- Trend graphs over time
- Year-in-review heatmap
- Weekly/monthly summary reports

### Integration Opportunities

- Optional cloud backup (user-controlled)
- Calendar app integration (iCal export)
- Webhook support for automation

## 14. Risks & Mitigations

### Risk 1: Data Loss
**Risk**: User loses habit data due to accidental deletion or system issues
**Mitigation**:
- Store database in user-visible location with clear naming
- Document backup procedures in README
- Consider auto-backup on app start (Phase 2+)

### Risk 2: Streak Calculation Complexity
**Risk**: Edge cases in streak calculation lead to incorrect counts
**Mitigation**:
- Comprehensive unit tests for all edge cases
- Clear documentation of calculation rules
- Test with real-world scenarios (timezone edges, etc.)

### Risk 3: Performance with Large Data
**Risk**: App slows down with months/years of habit data
**Mitigation**:
- Index database on frequently queried fields
- Paginate completion queries
- Lazy load calendar months

### Risk 4: Browser Compatibility
**Risk**: Frontend doesn't work in all browsers
**Mitigation**:
- Target modern browsers only (Chrome, Firefox, Safari, Edge)
- Use well-supported CSS and JS features
- Test on multiple browsers before release

## 15. Appendix

### Database Schema

```sql
CREATE TABLE habits (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE completions (
    id TEXT PRIMARY KEY,
    habit_id TEXT NOT NULL,
    completed_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
    UNIQUE(habit_id, completed_date)
);

CREATE TABLE absences (
    id TEXT PRIMARY KEY,
    habit_id TEXT NOT NULL,
    absence_date DATE NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
    UNIQUE(habit_id, absence_date)
);

CREATE INDEX idx_completions_habit_date ON completions(habit_id, completed_date);
CREATE INDEX idx_absences_habit_date ON absences(habit_id, absence_date);
```

### Key Dependencies

| Package | Purpose | Documentation |
|---------|---------|---------------|
| FastAPI | Backend framework | https://fastapi.tiangolo.com |
| SQLAlchemy | ORM | https://docs.sqlalchemy.org |
| Pydantic | Validation | https://docs.pydantic.dev |
| React | Frontend framework | https://react.dev |
| TailwindCSS | Styling | https://tailwindcss.com |
| Vite | Build tool | https://vitejs.dev |

### Glossary

- **Habit**: A recurring activity the user wants to track daily
- **Completion**: A record that a habit was done on a specific date
- **Absence**: A planned skip day (vacation, sick) that preserves the streak without counting as a completion
- **Streak**: Consecutive days of completing a habit (absences are skipped, not counted)
- **Completion Rate**: Percentage of days a habit was completed, excluding absence days from the calculation
