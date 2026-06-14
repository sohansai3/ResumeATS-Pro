# ResumeATS-Pro

### AI-Powered Resume ATS Score Analyzer

ResumeATS-Pro is a production-ready web application that analyzes how well a resume matches a job description using ATS (Applicant Tracking System) principles. The system extracts content from PDF resumes, identifies relevant keywords and skills, calculates an ATS compatibility score, highlights missing requirements, and provides actionable recommendations to improve resume effectiveness.

Built with FastAPI, Scikit-Learn, Pandas, NumPy, SQLite, Jinja Templates, and PDF processing libraries, ResumeATS-Pro delivers both a user-friendly web interface and RESTful APIs.

---

## Features

### Resume Analysis

* Upload PDF resumes
* Paste or upload job descriptions
* Automatic PDF text extraction
* Resume-job description similarity analysis
* ATS compatibility score calculation

### Keyword & Skill Matching

* Keyword extraction and matching
* Technical skill identification
* Missing skill detection
* Matched and unmatched keyword reporting

### Resume Improvement Insights

* ATS optimization recommendations
* Missing skills suggestions
* Resume enhancement guidance

### Reporting & History

* Download detailed PDF reports
* Store previous analyses
* Analysis dashboard
* Historical ATS score tracking

### Developer Features

* REST API with Swagger UI
* SQLite database integration
* Structured logging
* Input validation
* Exception handling
* Unit test coverage

---

## Tech Stack

| Category          | Technologies          |
| ----------------- | --------------------- |
| Backend           | FastAPI               |
| Machine Learning  | Scikit-Learn          |
| Data Processing   | Pandas, NumPy         |
| Database          | SQLite                |
| PDF Processing    | pypdf                 |
| Report Generation | ReportLab             |
| Frontend          | HTML, CSS, JavaScript |
| Templates         | Jinja2                |
| Testing           | Pytest                |

---

## Project Architecture

```text
ResumeATS-Pro/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── domain/
│   ├── repositories/
│   ├── services/
│   ├── static/
│   └── templates/
│
├── reports/
│
├── tests/
│
└── ats_analyzer.db
```

---

## ATS Analysis Workflow

```text
Resume PDF
     │
     ▼
Text Extraction
     │
     ▼
Keyword & Skill Extraction
     │
     ▼
Resume ↔ Job Description Comparison
     │
     ▼
ATS Score Calculation
     │
     ▼
Missing Skills Detection
     │
     ▼
Suggestions Generation
     │
     ▼
PDF Report & Dashboard Storage
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/ResumeATS-Pro.git
cd ResumeATS-Pro
```

### Create Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file:

```env
APP_NAME=Resume ATS Score Analyzer
DATABASE_URL=sqlite:///./ats_analyzer.db
LOG_LEVEL=INFO
MAX_UPLOAD_MB=8
REPORT_DIR=reports
```

---

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

| Method | Endpoint                              | Description            |
| ------ | ------------------------------------- | ---------------------- |
| GET    | /health                               | Health Check           |
| POST   | /api/v1/analyses                      | Create Resume Analysis |
| GET    | /api/v1/analyses                      | List All Analyses      |
| GET    | /api/v1/analyses/{analysis_id}        | Get Analysis Details   |
| GET    | /api/v1/analyses/{analysis_id}/report | Download PDF Report    |

---

## Database Schema

### resume_analyses

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

---

## Running Tests

```bash
pytest
```

---

## Deployment

The application can be deployed on:

* Render
* Railway
* AWS EC2
* Azure App Service
* Google Cloud Run

Production Command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Future Enhancements

* Resume parsing with NLP transformers
* Industry-specific ATS scoring
* Resume ranking against multiple job descriptions
* AI-powered resume rewriting suggestions
* User authentication and profiles
* PostgreSQL support
* Docker deployment
* CI/CD integration

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

**Sohan Sai**

Aspiring Software Engineer | Machine Learning Enthusiast | Backend Developer

If you found this project useful, consider giving it a ⭐ on GitHub.
