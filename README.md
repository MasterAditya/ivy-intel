# ivy-intel

A FastAPI + Jinja2 web app (with SQLite + SQLAlchemy) for exploring **Ivy League–style opportunities**, tracking **students**, and supporting a lightweight **applications + posts/comments** workflow. It includes simple “intel” helpers for:

- **Opportunity domain classification** (AI / Law / Biomedical / Engineering / General)
- **InCoScore** (Intelligence & Competency Score) calculation for students

## Tech stack

- **Backend:** FastAPI
- **Templates:** Jinja2
- **Database:** SQLite (`ivy_league.db`)
- **ORM:** SQLAlchemy
- **Server:** Uvicorn

Dependencies are listed in `requirements.txt`.

## Repository layout (key components)

- `main.py` — FastAPI app entry, routing/UI, and database seeding logic
- `models.py` — SQLAlchemy models:
  - `Opportunity`, `Student`, `Application`, `Post`, `Comment`
- `database.py` — SQLAlchemy engine/session setup (SQLite) + `get_db()` dependency
- `helpers.py` — domain classifier + InCoScore calculator
- `templates/` — Jinja2 HTML templates (server-rendered UI)
- `static/` — static assets (CSS/JS/images)
- `ivy_league.db` — local SQLite database file (seeded / used by the app)
- `requirements.txt` — Python dependencies

> Note: there is also a `venv/` directory committed in this repo. In most projects you would not commit virtual environments; prefer `.gitignore` for `venv/`.

## Setup & run

### 1) Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start the server

If the FastAPI app object is named `app` inside `main.py`, run:

```bash
uvicorn main:app --reload
```

Then open:

- http://127.0.0.1:8000

## Data model overview

- **Opportunity**
  - title, description, university, domain, posted_date
- **Student**
  - profile fields + metrics used by InCoScore (hackathons, internships, research_papers, coding_score)
- **Application**
  - joins Student ↔ Opportunity with a status and timestamp
- **Post / Comment**
  - simple community content tied back to Student authors

## Helper logic

### Opportunity classification

`helpers.classify_opportunity(description)` uses keyword matching to assign a domain:
- AI, Law, Biomedical, Engineering, or General

### InCoScore

`helpers.calculate_incoscore(student)` formula:

```
hackathons*2 + internships*3 + research_papers*4 + coding_score*0.1
```

## Notes / caveats

- The database is configured in `database.py` as:

  `sqlite:///./ivy_league.db`

- Since `ivy_league.db` is committed, your local runs will modify that file unless you change the DB URL.
- Search results I pulled from GitHub code search can be incomplete (GitHub limits results returned via API).

## License

Add a license if you plan to distribute this project.
