from io import BytesIO

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader

from app.core.config import settings


class PdfTextExtractor:
    async def extract_resume_text(self, file: UploadFile) -> str:
        self._validate_pdf_upload(file)
        content = await file.read()
        if len(content) > settings.max_upload_mb * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"Resume PDF must be {settings.max_upload_mb} MB or smaller.")
        try:
            reader = PdfReader(BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Could not read the uploaded PDF.") from exc
        cleaned = " ".join(text.split())
        if len(cleaned) < 80:
            raise HTTPException(status_code=422, detail="The resume PDF does not contain enough extractable text.")
        return cleaned

    async def extract_job_description(self, text: str | None, file: UploadFile | None) -> str:
        if text and text.strip():
            return self._validate_job_description(text)
        if file is None or not file.filename:
            raise HTTPException(status_code=422, detail="Provide a job description as text or upload a file.")
        content = await file.read()
        if len(content) > settings.max_upload_mb * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"Job description file must be {settings.max_upload_mb} MB or smaller.")
        content_type = (file.content_type or "").lower()
        if file.filename.lower().endswith(".pdf") or content_type == "application/pdf":
            try:
                reader = PdfReader(BytesIO(content))
                extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception as exc:
                raise HTTPException(status_code=400, detail="Could not read the job description PDF.") from exc
            return self._validate_job_description(extracted)
        try:
            return self._validate_job_description(content.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise HTTPException(status_code=400, detail="Job description file must be PDF or UTF-8 text.") from exc

    def _validate_pdf_upload(self, file: UploadFile) -> None:
        content_type = (file.content_type or "").lower()
        if not file.filename or not file.filename.lower().endswith(".pdf") or content_type not in {"application/pdf", "application/octet-stream"}:
            raise HTTPException(status_code=415, detail="Resume upload must be a PDF file.")

    @staticmethod
    def _validate_job_description(text: str) -> str:
        cleaned = " ".join(text.split())
        if len(cleaned) < 80:
            raise HTTPException(status_code=422, detail="Job description must contain at least 80 characters.")
        return cleaned
