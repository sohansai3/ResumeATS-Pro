from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AnalysisRecord(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_filename: Mapped[str] = mapped_column(String(255))
    resume_text: Mapped[str] = mapped_column(Text)
    job_description: Mapped[str] = mapped_column(Text)
    ats_score: Mapped[float] = mapped_column(Float, index=True)
    similarity_score: Mapped[float] = mapped_column(Float)
    keyword_score: Mapped[float] = mapped_column(Float)
    skill_score: Mapped[float] = mapped_column(Float)
    matched_keywords_json: Mapped[str] = mapped_column(Text)
    missing_keywords_json: Mapped[str] = mapped_column(Text)
    matched_skills_json: Mapped[str] = mapped_column(Text)
    missing_skills_json: Mapped[str] = mapped_column(Text)
    suggestions_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
