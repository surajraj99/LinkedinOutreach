# OpenOutreach Project Context

OpenOutreach is a self-hosted, open-source LinkedIn automation tool for B2B lead generation. It uses AI (Bayesian Active Learning + LLMs) to autonomously discover, qualify, and contact leads based on product descriptions and target market objectives.

## Project Overview

- **Core Tech Stack:** Python 3.12+, Django (with DjangoCRM), Playwright (with stealth), Scikit-learn (GPR), Pydantic AI (LLM integration).
- **Architecture:** 
    - **CRM-backed:** Built on a Django CRM, using SQLite (`data/db.sqlite3`) for persistence.
    - **Task-Driven:** A persistent task queue (`Task` model) managed by a daemon (`rundaemon`).
    - **ML Pipeline:** Gaussian Process Regressor (GPR) on profile embeddings for candidate selection, gated by LLM qualification.
    - **Stealth Browser Automation:** Mimics real user behavior via Playwright and interacts with LinkedIn's internal Voyager API.

## Building and Running

### Prerequisites
- Python 3.12+
- Docker (optional, but recommended for production-like environments)

### Local Setup
```bash
# Install dependencies, Playwright browsers, run migrations, and bootstrap CRM
make setup
```

### Running the Project
```bash
# Start the automation daemon
make run

# Start the Django Admin (CRM UI) at http://localhost:8000/admin/
make admin
```

### Docker Commands
```bash
make build   # Build Docker images
make up      # Run in background
make stop    # Stop services
make logs    # Follow logs
```

## Development Conventions

- **Environment:** Always use the local virtual environment (`.venv/bin/python`).
- **Coding Style:**
    - Follow existing patterns in `linkedin/`, `crm/`, and `chat/`.
    - Custom exceptions are located in `linkedin/exceptions.py`.
    - All persistent context should be in `CLAUDE.md` or `ARCHITECTURE.md`.
- **Testing:**
    - Uses `pytest` with `pytest-django`.
    - Run all tests: `make test` or `pytest`.
    - Run specific tests: `pytest tests/api/test_voyager.py` or `pytest -k test_name`.
- **State Machine:** Profile lifecycle follows: `QUALIFIED` → `READY_TO_CONNECT` → `PENDING` → `CONNECTED` → `COMPLETED` / `FAILED`.
- **Task Queue:** `linkedin/tasks/scheduler.py` is the single owner of Task creation.
- **LLM Configuration:** Managed via a `SiteConfig` singleton in the Django Admin. Supports OpenAI, Anthropic, Google, Groq, Mistral, Cohere, and OpenAI-compatible endpoints.

## Key Directories

- `linkedin/`: Core automation logic, tasks, browser interactions, and ML pipeline.
- `crm/`: Lead and Deal models, integrated with the CRM.
- `chat/`: Messaging models and history tracking.
- `docs/`: Extensive documentation on architecture, configuration, and features.
- `data/`: Persistent storage (SQLite DB).

## Documentation Reference
- [Architecture](./docs/architecture.md)
- [Configuration](./docs/configuration.md)
- [Testing](./docs/testing.md)
- [CLAUDE.md](./CLAUDE.md) - Rules and quick reference.
