# ResumeATS-Pro
ResumeATS-Pro is a production-ready Resume ATS Score Analyzer built with FastAPI, Scikit-Learn, Pandas, NumPy, SQLite, PDF processing, HTML/CSS, JavaScript, and Jinja Templates.

The application helps users analyze how well a PDF resume matches a job description. It extracts text from the resume, identifies important keywords and skills, calculates an ATS-style score, detects missing skills, provides resume improvement suggestions, stores previous analyses, and allows users to download a PDF report.

## Features

- Upload PDF resume
- Add job description as text or file
- Extract text from PDF
- Keyword matching
- Skill extraction
- ATS score calculation
- Missing skills detection
- Resume improvement suggestions
- Download analysis report as PDF
- Dashboard with analysis history
- REST API with Swagger documentation
- SQLite database storage
- Error handling and logging
- Input validation
- Unit tests

## Tech Stack

- Python
- FastAPI
- Scikit-Learn
- Pandas
- NumPy
- SQLite
- Jinja Templates
- HTML/CSS/JavaScript
- pypdf
- ReportLab

Run the Application
python -m uvicorn main:app --reload
Open in browser:
http://127.0.0.1:8000
API documentation:
http://127.0.0.1:8000/docs
API Endpoints
GET  /health
POST /api/v1/analyses
GET  /api/v1/analyses
GET  /api/v1/analyses/{analysis_id}
GET  /api/v1/analyses/{analysis_id}/report
Project Structure
ResumeATS-Pro/
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
Database
The application uses SQLite by default.
ats_analyzer.db
Main table:
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
Run Tests
pytest
Environment Variables
APP_NAME=Resume ATS Score Analyzer
DATABASE_URL=sqlite:///./ats_analyzer.db
LOG_LEVEL=INFO
MAX_UPLOAD_MB=8
REPORT_DIR=reports
Deployment
python -m uvicorn main:app --host 0.0.0.0 --port 8000
The project can be deployed on platforms such as Render, Railway, AWS EC2, Azure App Service, or Google Cloud Run.
