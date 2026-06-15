from io import BytesIO

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from app.main import app

client = TestClient(app)


def _pdf_bytes(text: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    y = 800
    for line in text.splitlines():
        pdf.drawString(40, y, line[:110])
        y -= 16
    pdf.save()
    return buffer.getvalue()


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_resume_analysis_lifecycle():
    resume_text = """
    Senior Python engineer with FastAPI, SQL, PostgreSQL, Docker, AWS, pytest,
    pandas, numpy, scikit-learn, REST API design, machine learning, CI/CD, and
    leadership experience delivering production analytics platforms.
    """
    job_description = """
    We need a Python backend engineer with FastAPI, PostgreSQL, Docker, AWS,
    pytest, REST API design, machine learning, pandas, numpy, scikit-learn,
    CI/CD, communication, stakeholder management, and production experience.
    """

    response = client.post(
        "/api/v1/analyses",
        files={"resume_pdf": ("resume.pdf", _pdf_bytes(resume_text), "application/pdf")},
        data={"job_description_text": job_description},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["ats_score"] > 50
    assert "python" in payload["matched_skills"]

    detail = client.get(f"/api/v1/analyses/{payload['id']}")
    assert detail.status_code == 200
    assert detail.json()["id"] == payload["id"]

    report = client.get(f"/api/v1/analyses/{payload['id']}/report")
    assert report.status_code == 200
    assert report.headers["content-type"] == "application/pdf"


def test_rejects_non_pdf_resume():
    response = client.post(
        "/api/v1/analyses",
        files={"resume_pdf": ("resume.txt", b"not a pdf", "text/plain")},
        data={"job_description_text": "Python FastAPI PostgreSQL Docker AWS pytest " * 5},
    )

    assert response.status_code == 415
