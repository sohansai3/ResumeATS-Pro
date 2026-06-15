# Resume ATS Score Analyzer

Resume ATS Score Analyzer is a production-ready FastAPI application for comparing a PDF resume against a target job description. It extracts resume text from PDF, detects skills and keywords, calculates an ATS-style score, persists analysis history, renders a dashboard, and generates downloadable PDF reports.

The application runs locally with SQLite by default and can be deployed behind any ASGI server.

## Features

- PDF resume upload and text extraction
- Job description paste/upload support
- Keyword matching and missing keyword detection
- Skill extraction using a curated technical and professional taxonomy
- ATS score calculation using scikit-learn TF-IDF similarity plus coverage metrics
- Resume improvement suggestions
- Downloadable PDF reports
- Dashboard with recent analyses
- Clean layered structure: API, UI, services, repositories, domain schemas
- Input validation with Pydantic
- Structured logging and exception handling
- Unit tests with FastAPI `TestClient`
- OpenAPI documentation at `/docs`

## Quick Start

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:

- Web app: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API Documentation

### `GET /health`

Returns application health.

### `POST /api/v1/analyses`

Creates a resume analysis. Submit as `multipart/form-data`.

Fields:

- `resume_pdf`: required PDF file
- `job_description_text`: optional pasted text
- `job_description_file`: optional PDF or UTF-8 text file

Response:

```json
{
  "id": 1,
  "resume_filename": "resume.pdf",
  "ats_score": 82.4,
  "similarity_score": 71.2,
  "keyword_score": 88.6,
  "skill_score": 90.0,
  "created_at": "2026-06-14T16:45:00",
  "matched_keywords": ["python", "api"],
  "missing_keywords": ["kubernetes"],
  "matched_skills": ["python", "fastapi"],
  "missing_skills": ["kubernetes"],
  "suggestions": ["Add evidence for these required skills: kubernetes."]
}
```

### `GET /api/v1/analyses`

Lists recent analyses.

### `GET /api/v1/analyses/{analysis_id}`

Returns a full analysis by ID.

### `GET /api/v1/analyses/{analysis_id}/report`

Downloads a PDF report.

## Database Schema

SQLite is used by default. The database file is created at `ats_analyzer.db`.

```sql
CREATE TABLE resume_analyses (
    id INTEGER PRIMARY KEY,
    resume_filename VARCHAR(255) NOT NULL,
    resume_text TEXT NOT NULL,
    job_description TEXT NOT NULL,
    ats_score FLOAT NOT NULL,
    similarity_score FLOAT NOT NULL,
    keyword_score FLOAT NOT NULL,
    skill_score FLOAT NOT NULL,
    matched_keywords_json TEXT NOT NULL,
    missing_keywords_json TEXT NOT NULL,
    matched_skills_json TEXT NOT NULL,
    missing_skills_json TEXT NOT NULL,
    suggestions_json TEXT NOT NULL,
    created_at DATETIME NOT NULL
);
```

## Project Structure

```text
.
|-- main.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- app/
|   |-- api/
|   |-- core/
|   |-- db/
|   |-- domain/
|   |-- repositories/
|   |-- services/
|   |-- static/
|   `-- templates/
`-- tests/
```

## Running Tests

```bash
pytest
```

## Configuration

Environment variables:

- `APP_NAME`: defaults to `Resume ATS Score Analyzer`
- `DATABASE_URL`: defaults to `sqlite:///./ats_analyzer.db`
- `LOG_LEVEL`: defaults to `INFO`
- `MAX_UPLOAD_MB`: defaults to `8`
- `REPORT_DIR`: defaults to `reports`

## Deployment

For a simple server deployment:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

For PostgreSQL, set `DATABASE_URL` to a SQLAlchemy PostgreSQL URL such as:

```bash
DATABASE_URL=postgresql+psycopg://ats_user:strong_secret@host:5432/ats_analyzer
```

Install the matching PostgreSQL driver if you choose PostgreSQL in production.
