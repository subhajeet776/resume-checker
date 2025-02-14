from typing import Dict, List, Any

class ATSChecker:
    def __init__(self):
        self.ats_rules = {
            'file_format': ['pdf', 'docx'],
            'forbidden_elements': ['images', 'tables', 'headers', 'footers'],
            'recommended_sections': ['contact', 'summary', 'experience', 'education', 'skills']
        }

    def check_ats_compliance(self, resume_sections: Dict) -> Dict[str, Any]:
        score = 100
        suggestions = []

        # Check for required sections
        missing_sections = []
        for section in self.ats_rules['recommended_sections']:
            if section not in resume_sections:
                missing_sections.append(section)
                score -= 10

        if missing_sections:
            suggestions.append(f"Add missing sections: {', '.join(missing_sections)}")

        # Check contact information
        if not resume_sections.get('contact_info', {}).get('email'):
            score -= 15
            suggestions.append("Add a professional email address")

        if not resume_sections.get('contact_info', {}).get('phone'):
            score -= 10
            suggestions.append("Add a phone number")

        # Check skills section
        if len(resume_sections.get('skills', [])) < 5:
            score -= 10
            suggestions.append("Add more relevant skills (aim for at least 5)")

        # Check experience section
        if len(resume_sections.get('experience', [])) < 2:
            score -= 15
            suggestions.append("Add more detailed work experience")

        return {
            'score': max(0, score),
            'suggestions': suggestions
        }