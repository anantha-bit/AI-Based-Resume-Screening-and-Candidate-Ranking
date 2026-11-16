"""
PDF Candidate Dossier and Report Generator.
Uses ReportLab to export clean, academic, recruiter-ready evaluation dossiers.
Academic context: Unit 2 & Unit 4 (Application Reporting & Output Parsers).
"""

import os
import io
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class CandidatePDFExporter:
    """Exports structured candidate screening dossiers into PDF format."""

    @classmethod
    def generate_pdf_bytes(cls, candidate_data: Dict[str, Any], jd_title: str = "Target Position") -> bytes:
        """Generate PDF in memory and return raw bytes for Streamlit download."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )

        styles = getSampleStyleSheet()
        
        # Custom Typography
        header_title = ParagraphStyle(
            'HeaderTitle', parent=styles['Heading1'],
            fontSize=18, leading=22, textColor=colors.HexColor("#1E293B"), spaceAfter=4
        )
        sub_title = ParagraphStyle(
            'SubTitle', parent=styles['Normal'],
            fontSize=10, leading=14, textColor=colors.HexColor("#64748B"), spaceAfter=12
        )
        sec_heading = ParagraphStyle(
            'SecHeading', parent=styles['Heading2'],
            fontSize=12, leading=16, textColor=colors.HexColor("#0F172A"), spaceBefore=10, spaceAfter=6
        )
        body = ParagraphStyle(
            'Body', parent=styles['Normal'],
            fontSize=9, leading=13, textColor=colors.HexColor("#334155"), spaceAfter=4
        )
        body_bold = ParagraphStyle(
            'BodyBold', parent=styles['Normal'],
            fontSize=9, leading=13, fontName="Helvetica-Bold", textColor=colors.HexColor("#0F172A")
        )

        story = []

        # Document Header
        story.append(Paragraph("AI-Based Candidate Screening Dossier", header_title))
        story.append(Paragraph(f"PES University • Department of CSE (AI & ML) • Position: <b>{jd_title}</b>", sub_title))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#3B82F6"), spaceAfter=12))

        # Candidate Summary Table
        cand_name = candidate_data.get("candidate_name", "Unknown Candidate")
        cand_id = candidate_data.get("candidate_id", "CAND-N/A")
        overall_score = candidate_data.get("overall_score", 0.0)
        badge = candidate_data.get("recommendation_badge", "Evaluated")
        tot_exp = candidate_data.get("total_experience_years", 0.0)

        meta_table_data = [
            [
                Paragraph("<b>Candidate Name:</b>", body), Paragraph(cand_name, body),
                Paragraph("<b>Composite Score:</b>", body), Paragraph(f"<b>{overall_score:.1f} / 100</b>", body_bold)
            ],
            [
                Paragraph("<b>Candidate ID:</b>", body), Paragraph(cand_id, body),
                Paragraph("<b>Evaluation Tier:</b>", body), Paragraph(badge, body_bold)
            ],
            [
                Paragraph("<b>Documented Experience:</b>", body), Paragraph(f"{tot_exp:g} Years", body),
                Paragraph("<b>Audit Status:</b>", body), Paragraph("Grounded / Fair", body)
            ]
        ]
        meta_table = Table(meta_table_data, colWidths=[110, 150, 110, 150])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # Component Scores Breakdown
        story.append(Paragraph("Multi-Criteria Evaluation Scores", sec_heading))
        comp = candidate_data.get("component_scores", {})
        comp_table_data = [
            [Paragraph("<b>Criteria</b>", body_bold), Paragraph("<b>Score (0-100)</b>", body_bold), Paragraph("<b>Target Weight</b>", body_bold)],
            [Paragraph("Required Skills Match", body), Paragraph(f"{comp.get('required_skills_match', 0)}%", body), Paragraph("35%", body)],
            [Paragraph("Preferred Skills Match", body), Paragraph(f"{comp.get('preferred_skills_match', 0)}%", body), Paragraph("15%", body)],
            [Paragraph("Educational Qualifications", body), Paragraph(f"{comp.get('education_score', 0)}%", body), Paragraph("10%", body)],
            [Paragraph("Work Experience Depth", body), Paragraph(f"{comp.get('experience_score', 0)}%", body), Paragraph("15%", body)],
            [Paragraph("Project Relevance", body), Paragraph(f"{comp.get('project_relevance', 0)}%", body), Paragraph("10%", body)],
            [Paragraph("Transformer Semantic Match", body), Paragraph(f"{comp.get('semantic_similarity', 0)}%", body), Paragraph("15%", body)],
        ]
        comp_table = Table(comp_table_data, colWidths=[200, 160, 160])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 10))

        # Recruiter Explanation
        story.append(Paragraph("Recruiter Assessment & Transparent Explanation", sec_heading))
        explanation_text = candidate_data.get("explanation", "Assessment completed.")
        story.append(Paragraph(explanation_text, body))
        story.append(Spacer(1, 8))

        # Key Strengths & Gaps
        story.append(Paragraph("Key Strengths & Identified Qualification Gaps", sec_heading))
        for s in candidate_data.get("strengths", []):
            story.append(Paragraph(f"• <b>Strength:</b> {s}", body))
        for g in candidate_data.get("gaps", []):
            story.append(Paragraph(f"• <b>Gap / Area for Review:</b> {g}", body))
        story.append(Spacer(1, 10))

        # Grounding & Ethical Notice
        story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#E2E8F0"), spaceAfter=6))
        ethical_notice = (
            "<b>Human-in-the-Loop & Fairness Guarantee:</b> This evaluation was generated by an AI recruiter-assistance "
            "system. It serves as preliminary decision support. Final interview and hiring decisions remain strictly with "
            "human recruiters. Protected demographic characteristics are excluded from all ranking algorithms."
        )
        story.append(Paragraph(ethical_notice, sub_title))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
