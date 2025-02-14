from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from typing import Dict, Any

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'CustomStyle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            spaceAfter=20
        )

    def generate_report(self, analysis_results: Dict[str, Any]) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Title
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        elements.append(Paragraph("Resume Analysis Report", title_style))
        elements.append(Spacer(1, 20))

        # Overall Score
        score_style = ParagraphStyle(
            'ScoreStyle',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#0066CC')
        )
        elements.append(Paragraph(f"Overall Score: {analysis_results['ats_score']}%", score_style))
        elements.append(Spacer(1, 20))

        # ATS Suggestions
        elements.append(Paragraph("ATS Improvement Suggestions:", self.styles['Heading2']))
        for suggestion in analysis_results['ats_suggestions']:
            elements.append(Paragraph(f"• {suggestion}", self.custom_style))
        elements.append(Spacer(1, 20))

        # Grammar Issues
        if analysis_results.get('grammar_issues'):
            elements.append(Paragraph("Grammar Issues:", self.styles['Heading2']))
            for issue in analysis_results['grammar_issues']:
                elements.append(Paragraph(f"• {issue['message']}", self.custom_style))
            elements.append(Spacer(1, 20))

        # Job Match Analysis
        if 'job_match' in analysis_results:
            elements.append(Paragraph("Job Match Analysis:", self.styles['Heading2']))
            elements.append(Paragraph(f"Match Score: {analysis_results['job_match']}%", self.custom_style))
            elements.append(Paragraph("Matching Keywords:", self.custom_style))
            for keyword in analysis_results['matching_keywords']:
                elements.append(Paragraph(f"• {keyword}", self.custom_style))

        doc.build(elements)
        buffer.seek(0)
        return buffer
