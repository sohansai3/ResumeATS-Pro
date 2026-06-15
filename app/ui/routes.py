import json

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.analysis_service import ResumeAnalysisService
from app.services.pdf_service import PdfTextExtractor
from app.services.report_service import ReportService

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    analyses = ResumeAnalysisService(db).list_recent(10)
    return templates.TemplateResponse("index.html", {"request": request, "analyses": analyses, "result": None, "errors": []})


@router.post("/", response_class=HTMLResponse)
async def analyze_from_form(
    request: Request,
    resume_pdf: UploadFile = File(...),
    job_description_text: str | None = Form(default=None),
    job_description_file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    service = ResumeAnalysisService(db)
    errors: list[str] = []
    result = None
    try:
        extractor = PdfTextExtractor()
        resume_text = await extractor.extract_resume_text(resume_pdf)
        job_description = await extractor.extract_job_description(job_description_text, job_description_file)
        result = service.analyze(resume_pdf.filename or "resume.pdf", resume_text, job_description)
    except Exception as exc:
        detail = getattr(exc, "detail", "Unable to analyze the submitted resume.")
        errors = [str(detail)]

    analyses = service.list_recent(10)
    return templates.TemplateResponse("index.html", {"request": request, "analyses": analyses, "result": result, "errors": errors})


@router.get("/analyses/{analysis_id}", response_class=HTMLResponse)
def analysis_detail(request: Request, analysis_id: int, db: Session = Depends(get_db)):
    record = ResumeAnalysisService(db).get(analysis_id)
    if record is None:
        return templates.TemplateResponse("not_found.html", {"request": request}, status_code=404)
    detail = {
        "record": record,
        "matched_keywords": json.loads(record.matched_keywords_json),
        "missing_keywords": json.loads(record.missing_keywords_json),
        "matched_skills": json.loads(record.matched_skills_json),
        "missing_skills": json.loads(record.missing_skills_json),
        "suggestions": json.loads(record.suggestions_json),
    }
    return templates.TemplateResponse("detail.html", {"request": request, **detail})


@router.get("/analyses/{analysis_id}/report")
def ui_download_report(request: Request, analysis_id: int, db: Session = Depends(get_db)):
    record = ResumeAnalysisService(db).get(analysis_id)
    if record is None:
        return templates.TemplateResponse("not_found.html", {"request": request}, status_code=404)
    path = ReportService().build_pdf(record)
    return FileResponse(path, media_type="application/pdf", filename=path.name)
