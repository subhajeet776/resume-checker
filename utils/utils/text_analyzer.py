import spacy
import language_tool_python
from typing import Dict, List, Tuple

class TextAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        try:
            self.grammar_tool = language_tool_python.LanguageTool('en-US')
            self.grammar_check_available = True
        except Exception as e:
            print(f"Grammar checking unavailable: {str(e)}")
            self.grammar_check_available = False

    def analyze_text(self, text: str) -> Dict:
        doc = self.nlp(text)

        # Analyze various aspects of the text
        analysis = {
            'word_count': len(doc),
            'sentence_count': len(list(doc.sents)),
            'grammar_issues': self._check_grammar(text) if self.grammar_check_available else [],
            'readability_score': self._calculate_readability(doc),
            'action_verbs': self._find_action_verbs(doc)
        }
        return analysis

    def _check_grammar(self, text: str) -> List[Dict]:
        if not self.grammar_check_available:
            return []
        try:
            matches = self.grammar_tool.check(text)
            return [{'message': match.message, 'context': match.context} for match in matches[:5]]
        except Exception as e:
            print(f"Grammar check failed: {str(e)}")
            return []

    def _calculate_readability(self, doc) -> float:
        # Simple Flesch-Kincaid readability score
        words = len([token for token in doc if not token.is_punct])
        sentences = len(list(doc.sents))
        if sentences == 0:
            return 0
        return round((words / sentences), 2)

    def _find_action_verbs(self, doc) -> List[str]:
        action_verbs = []
        for token in doc:
            if token.pos_ == "VERB":
                action_verbs.append(token.text)
        return list(set(action_verbs))

    def calculate_job_match_score(self, resume_text: str, job_description: str) -> Tuple[float, List[str]]:
        resume_doc = self.nlp(resume_text.lower())
        job_doc = self.nlp(job_description.lower())

        # Extract keywords from job description
        job_keywords = set([token.text for token in job_doc if token.pos_ in ['NOUN', 'PROPN']])

        # Find matching keywords in resume
        matching_keywords = []
        for token in resume_doc:
            if token.text in job_keywords:
                matching_keywords.append(token.text)

        # Calculate match score
        if len(job_keywords) == 0:
            return 0.0, matching_keywords

        match_score = (len(set(matching_keywords)) / len(job_keywords)) * 100
        return round(match_score, 2), list(set(matching_keywords))