import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AnalysisRecord


class AnalysisRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: dict) -> AnalysisRecord:
        record = AnalysisRecord(
            resume_filename=data["resume_filename"],
            resume_text=data["resume_text"],
            job_description=data["job_description"],
            ats_score=data["ats_score"],
            similarity_score=data["similarity_score"],
            keyword_score=data["keyword_score"],
            skill_score=data["skill_score"],
            matched_keywords_json=json.dumps(data["matched_keywords"]),
            missing_keywords_json=json.dumps(data["missing_keywords"]),
            matched_skills_json=json.dumps(data["matched_skills"]),
            missing_skills_json=json.dumps(data["missing_skills"]),
            suggestions_json=json.dumps(data["suggestions"]),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_recent(self, limit: int = 25) -> list[AnalysisRecord]:
        statement = select(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(limit)
        return list(self.db.scalars(statement).all())

    def get(self, analysis_id: int) -> AnalysisRecord | None:
        return self.db.get(AnalysisRecord, analysis_id)
