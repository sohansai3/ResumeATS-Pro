from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisSummary(BaseModel):
    id: int
    resume_filename: str
    ats_score: float = Field(..., ge=0, le=100)
    similarity_score: float = Field(..., ge=0, le=100)
    keyword_score: float = Field(..., ge=0, le=100)
    skill_score: float = Field(..., ge=0, le=100)
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisDetail(AnalysisSummary):
    matched_keywords: list[str]
    missing_keywords: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
