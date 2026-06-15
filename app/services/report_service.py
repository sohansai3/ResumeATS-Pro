import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.config import settings
from app.db.models import AnalysisRecord


class ReportService:
    def build_pdf(self, record: AnalysisRecord) -> Path:
        path = Path(settings.report_dir) / f"ats-report-{record.id}.pdf"
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(str(path), pagesize=letter, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
        story = [
            Paragraph("Resume ATS Score Report", styles["Title"]),
            Paragraph(f"Resume: {record.resume_filename}", styles["Normal"]),
            Paragraph(f"Generated: {record.created_at:%Y-%m-%d %H:%M}", styles["Normal"]),
            Spacer(1, 16),
        ]
        score_table = Table(
            [
                ["ATS Score", "Similarity", "Keyword Match", "Skill Match"],
                [f"{record.ats_score:.1f}%", f"{record.similarity_score:.1f}%", f"{record.keyword_score:.1f}%", f"{record.skill_score:.1f}%"],
            ]
        )
        score_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2156a5")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d7dee8")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.extend([score_table, Spacer(1, 18)])
        for title, values in [
            ("Matched Skills", self._loads(record.matched_skills_json)),
            ("Missing Skills", self._loads(record.missing_skills_json)),
            ("Missing Keywords", self._loads(record.missing_keywords_json)[:20]),
            ("Improvement Suggestions", self._loads(record.suggestions_json)),
        ]:
            story.append(Paragraph(title, styles["Heading2"]))
            if values:
                for value in values:
                    story.append(Paragraph(f"- {value}", styles["BodyText"]))
            else:
                story.append(Paragraph("None detected.", styles["BodyText"]))
            story.append(Spacer(1, 10))
        doc.build(story)
        return path

    @staticmethod
    def _loads(value: str) -> list[str]:
        data = json.loads(value)
        return data if isinstance(data, list) else []
