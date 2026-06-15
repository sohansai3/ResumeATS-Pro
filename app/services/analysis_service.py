import re
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.db.models import AnalysisRecord
from app.repositories.analysis_repository import AnalysisRepository


class ResumeAnalysisService:
    skill_taxonomy = sorted(
        {
            "python",
            "fastapi",
            "django",
            "flask",
            "sql",
            "postgresql",
            "mysql",
            "sqlite",
            "mongodb",
            "redis",
            "pandas",
            "numpy",
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "machine learning",
            "deep learning",
            "nlp",
            "data analysis",
            "data visualization",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "terraform",
            "ci/cd",
            "git",
            "linux",
            "javascript",
            "typescript",
            "react",
            "node.js",
            "html",
            "css",
            "rest api",
            "microservices",
            "unit testing",
            "pytest",
            "agile",
            "leadership",
            "communication",
            "problem solving",
            "stakeholder management",
        },
        key=len,
        reverse=True,
    )

    def __init__(self, db: Session) -> None:
        self.repository = AnalysisRepository(db)

    def analyze(self, resume_filename: str, resume_text: str, job_description: str) -> AnalysisRecord:
        result = self._score(resume_filename, resume_text, job_description)
        return self.repository.create(result)

    def list_recent(self, limit: int = 25) -> list[AnalysisRecord]:
        return self.repository.list_recent(limit)

    def get(self, analysis_id: int) -> AnalysisRecord | None:
        return self.repository.get(analysis_id)

    def _score(self, resume_filename: str, resume_text: str, job_description: str) -> dict:
        resume_normalized = self._normalize(resume_text)
        jd_normalized = self._normalize(job_description)
        similarity_score = self._similarity_score(resume_normalized, jd_normalized)
        jd_keywords = self._extract_keywords(jd_normalized)
        resume_tokens = set(self._tokens(resume_normalized))
        matched_keywords = [keyword for keyword in jd_keywords if keyword in resume_tokens]
        missing_keywords = [keyword for keyword in jd_keywords if keyword not in resume_tokens]
        keyword_score = self._coverage_score(matched_keywords, jd_keywords)
        jd_skills = self._extract_skills(jd_normalized)
        resume_skills = self._extract_skills(resume_normalized)
        matched_skills = sorted(set(jd_skills) & set(resume_skills))
        missing_skills = sorted(set(jd_skills) - set(resume_skills))
        skill_score = self._coverage_score(matched_skills, jd_skills)
        ats_score = round((similarity_score * 0.4) + (keyword_score * 0.3) + (skill_score * 0.3), 2)
        suggestions = self._suggestions(ats_score, missing_keywords, missing_skills, similarity_score)

        return {
            "resume_filename": resume_filename,
            "resume_text": resume_text,
            "job_description": job_description,
            "ats_score": ats_score,
            "similarity_score": similarity_score,
            "keyword_score": keyword_score,
            "skill_score": skill_score,
            "matched_keywords": matched_keywords[:30],
            "missing_keywords": missing_keywords[:30],
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
        }

    def _similarity_score(self, resume_text: str, job_description: str) -> float:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", min_df=1)
        matrix = vectorizer.fit_transform([resume_text, job_description])
        score = cosine_similarity(matrix[0], matrix[1])[0][0]
        return round(float(np.clip(score * 100, 0, 100)), 2)

    def _extract_keywords(self, text: str, limit: int = 35) -> list[str]:
        tokens = [
            token
            for token in self._tokens(text)
            if token not in ENGLISH_STOP_WORDS and len(token) > 2 and not token.isnumeric()
        ]
        counts = Counter(tokens)
        terms = pd.DataFrame(counts.most_common(), columns=["term", "count"])
        if terms.empty:
            return []
        terms["score"] = terms["count"] * terms["term"].str.len().clip(upper=12)
        return terms.sort_values(["score", "count"], ascending=False)["term"].head(limit).tolist()

    def _extract_skills(self, text: str) -> list[str]:
        found: list[str] = []
        searchable = f" {text} "
        aliases = {"node.js": ["node js", "nodejs"], "ci/cd": ["ci cd", "cicd"], "scikit-learn": ["sklearn", "scikit learn"], "rest api": ["restful api", "rest"]}
        for skill in self.skill_taxonomy:
            variants = [skill, *aliases.get(skill, [])]
            if any(re.search(rf"(?<![a-z0-9]){re.escape(variant)}(?![a-z0-9])", searchable) for variant in variants):
                found.append(skill)
        return sorted(set(found))

    @staticmethod
    def _coverage_score(matched: list[str], expected: list[str]) -> float:
        if not expected:
            return 100.0
        return round((len(set(matched)) / len(set(expected))) * 100, 2)

    @staticmethod
    def _tokens(text: str) -> list[str]:
        return re.findall(r"[a-z0-9+#]+", text.lower())

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(text.lower().split())

    @staticmethod
    def _suggestions(ats_score: float, missing_keywords: list[str], missing_skills: list[str], similarity_score: float) -> list[str]:
        suggestions: list[str] = []
        if missing_skills:
            suggestions.append(f"Add evidence for these required skills: {', '.join(missing_skills[:8])}.")
        if missing_keywords:
            suggestions.append(f"Mirror relevant job description language by naturally including: {', '.join(missing_keywords[:10])}.")
        if similarity_score < 45:
            suggestions.append("Rewrite the professional summary and recent experience bullets to align more directly with the target role.")
        if ats_score < 70:
            suggestions.append("Use measurable achievements with tools, scope, and outcomes in each major experience section.")
        suggestions.append("Keep formatting ATS-friendly: simple headings, standard section names, and selectable text rather than images.")
        return suggestions
