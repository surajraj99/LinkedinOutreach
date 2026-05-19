# OpenOutreach Project Context (Targeted Networking Refactor)

OpenOutreach has been refactored from a B2B sales tool into an intelligent, stealthy professional networking tool. It identifies coffee chat prospects by matching profiles against a specific professional fingerprint using local LLMs, similarity scoring, and platform activity data.

## Project Overview

- **Core Tech Stack:** Python 3.12+, Django, Playwright (with stealth), FastEmbed (BAAI/bge-small-en-v1.5), Pydantic AI (Ollama integration).
- **Architecture:** 
    - **Local LLM:** All LLM operations run via a local Ollama instance (`gemma4:e4b`).
    - **Activity-Based Routing:** Voyager API extracts recent profile activity (last 3 posts).
    - **Likelihood Scoring:** Combines semantic similarity with platform activity. Profiles active within 7 days get a 1.5x boost; inactive (>90 days) or no-activity profiles are capped at 0.1 score.
    - **Dynamic Qualification:** LLM matches profiles directly against dynamic `campaign_objective` strings and uses recent activity to generate personalized outreach talking points.
    - **Anti-Ban System:** Strict daily limits and mandatory randomized stealth intervals. Includes a "safe stealth" mode with broader delays (45s - 120s).
    - **CSV Export:** Matched profiles are automatically exported to timestamped CSVs in the `exports/` directory every 12 hours.

## Building and Running

### Prerequisites
- Python 3.12+
- **Ollama:** Running locally with the `gemma4:e4b` model.
- Docker: Optional, configured with `extra_hosts` to reach the local Ollama instance.

### Local Setup
```bash
# Install dependencies, Playwright browsers, run migrations, and bootstrap CRM
make setup
```

### Running the Project
```bash
# Start the automation daemon
make run

# Export matches manually
python manage.py export_matches
```

## Development Conventions

- **LLM Logic:** All LLM calls must use `get_llm_model()` which routes to `http://host.docker.internal:11434/v1`.
- **Match Threshold:** Profiles with a `similarity_score > 0.65` are passed to the LLM for deep qualification.
- **Stealth:** All browser navigation must use `goto_page(session, action, ...)` which enforces randomized human-rhythm pacing.
- **Safety Mode:** `SiteConfig.randomize_delays` enables broader (45-120s) safety intervals between actions.
- **State Machine:** Automated connection requests and messaging are **disabled** for safety; the system currently focuses on discovery and export.

## Key Directories

- `linkedin/`: Core networking logic, similarity scoring, activity extraction, and Ollama integration.
- `crm/`: Lead and Deal models, including `activity_data`, `last_active_date`, and matching persistence.
- `exports/`: Destination for automated and manual CSV exports (ignored by git).
- `docs/`: System documentation (Note: some legacy docs may refer to sales features).

## Documentation Reference
- [Architecture](./docs/architecture.md)
- [CLAUDE.md](./CLAUDE.md) - Rules and quick reference.
