import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domain.schemas import AnalysisDetail, AnalysisSummary
from app.services.analysis_service import ResumeAnalysisService
from app.services.pdf_service import PdfTextExtractor
from app.services.report_service import ReportService

router = APIRouter(tags=["resume-analysis"])


@router.post("/analyses", response_model=AnalysisDetail, status_code=201)
async def create_analysis(
    resume_pdf: UploadFile = File(...),
    job_description_text: str | None = Form(default=None),
    job_description_file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    extractor = PdfTextExtractor()
    resume_text = await extractor.extract_resume_text(resume_pdf)
    job_description = await extractor.extract_job_description(job_description_text, job_description_file)
    record = ResumeAnalysisService(db).analyze(resume_pdf.filename or "resume.pdf", resume_text, job_description)
    return _to_detail(record)


@router.get("/analyses", response_model=list[AnalysisSummary])
def list_analyses(limit: int = Query(default=25, ge=1, le=100), db: Session = Depends(get_db)):
    return ResumeAnalysisService(db).list_recent(limit)


@router.get("/analyses/{analysis_id}", response_model=AnalysisDetail)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    record = ResumeAnalysisService(db).get(analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return _to_detail(record)


@router.get("/analyses/{analysis_id}/report")
def download_report(analysis_id: int, db: Session = Depends(get_db)):
    record = ResumeAnalysisService(db).get(analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    path = ReportService().build_pdf(record)
    return FileResponse(path, media_type="application/pdf", filename=path.name)


def _to_detail(record) -> AnalysisDetail:
    return AnalysisDetail(
        id=record.id,
        resume_filename=record.resume_filename,
        ats_score=record.ats_score,
        similarity_score=record.similarity_score,
        keyword_score=record.keyword_score,
        skill_score=record.skill_score,
        created_at=record.created_at,
        matched_keywords=json.loads(record.matched_keywords_json),
        missing_keywords=json.loads(record.missing_keywords_json),
        matched_skills=json.loads(record.matched_skills_json),
        missing_skills=json.loads(record.missing_skills_json),
        suggestions=json.loads(record.suggestions_json),
    )
