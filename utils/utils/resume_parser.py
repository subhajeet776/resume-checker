import PyPDF2
import docx
import nltk
from typing import Dict, Any
import io

class ResumeParser:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        docx_file = io.BytesIO(file_bytes)
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def parse_resume(self, file_bytes: bytes, file_type: str) -> Dict[str, Any]:
        if file_type == "application/pdf":
            text = self.extract_text_from_pdf(file_bytes)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = self.extract_text_from_docx(file_bytes)
        else:
            text = file_bytes.decode('utf-8')

        # Basic section identification
        sections = {
            'contact_info': self._extract_contact_info(text),
            'skills': self._extract_skills(text),
            'education': self._extract_education(text),
            'experience': self._extract_experience(text)
        }
        return sections

    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        # Simple contact info extraction using regex
        import re
        email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        phone = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        return {
            'email': email[0] if email else '',
            'phone': phone[0] if phone else ''
        }

    def _extract_skills(self, text: str) -> list:
        # Basic skill extraction
        common_skills = ['python', 'java', 'javascript', 'sql', 'react', 'aws']
        skills = []
        for skill in common_skills:
            if skill.lower() in text.lower():
                skills.append(skill)
        return skills

    def _extract_education(self, text: str) -> list:
        # Basic education extraction
        edu_keywords = ['bachelor', 'master', 'phd', 'degree']
        education = []
        for line in text.split('\n'):
            if any(keyword in line.lower() for keyword in edu_keywords):
                education.append(line.strip())
        return education

    def _extract_experience(self, text: str) -> list:
        # Basic experience extraction
        exp_markers = ['experience', 'work history', 'employment']
        experience = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(marker in line.lower() for marker in exp_markers):
                if i + 1 < len(lines):
                    experience.append(lines[i + 1].strip())
        return experience
