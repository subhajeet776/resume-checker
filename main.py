import streamlit as st
import io
from utils import resume_parser




from utils.text_analyzer import TextAnalyzer
from utils.utils.ats_checker import ATSChecker
from utils.report_generator import ReportGenerator

def load_css():
    with open("styles/custom.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    load_css()
    
    st.title("Resume Analysis & ATS Optimization Tool")
    st.markdown("""
    <div class="upload-section">
        Upload your resume and job description to get personalized feedback and optimization suggestions.
    </div>
    """, unsafe_allow_html=True)

    # Initialize components
    parser = ResumeParser()
    analyzer = TextAnalyzer()
    ats_checker = ATSChecker()
    report_generator = ReportGenerator()

    # File upload
    resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", 
                                  type=['pdf', 'docx', 'txt'])
    
    job_description = st.text_area("Paste the job description here (optional)")

    if resume_file is not None:
        with st.spinner('Analyzing your resume...'):
            # Read and parse resume
            file_bytes = resume_file.read()
            resume_sections = parser.parse_resume(file_bytes, resume_file.type)

            # Analyze text
            resume_text = " ".join([str(v) for v in resume_sections.values()])
            text_analysis = analyzer.analyze_text(resume_text)

            # Check ATS compliance
            ats_results = ats_checker.check_ats_compliance(resume_sections)

            # Calculate job match if job description provided
            job_match_score = 0
            matching_keywords = []
            if job_description:
                job_match_score, matching_keywords = analyzer.calculate_job_match_score(
                    resume_text, job_description
                )

            # Display Results
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="score-card">
                    <h3>ATS Score</h3>
                    <h2 style="color: #0066CC">{}/100</h2>
                </div>
                """.format(ats_results['score']), unsafe_allow_html=True)

            with col2:
                if job_description:
                    st.markdown("""
                    <div class="score-card">
                        <h3>Job Match Score</h3>
                        <h2 style="color: #0066CC">{}/100</h2>
                    </div>
                    """.format(job_match_score), unsafe_allow_html=True)

            # Display improvement suggestions
            st.subheader("Improvement Suggestions")
            for suggestion in ats_results['suggestions']:
                st.markdown(f"• {suggestion}")

            # Display grammar issues
            if text_analysis['grammar_issues']:
                st.subheader("Grammar Issues")
                for issue in text_analysis['grammar_issues']:
                    st.markdown(f"• {issue['message']}")

            # Display matching keywords if job description provided
            if job_description:
                st.subheader("Matching Keywords")
                st.write(", ".join(matching_keywords))

            # Generate and offer report download
            report_data = {
                'ats_score': ats_results['score'],
                'ats_suggestions': ats_results['suggestions'],
                'grammar_issues': text_analysis['grammar_issues'],
                'job_match': job_match_score,
                'matching_keywords': matching_keywords
            }
            
            report_buffer = report_generator.generate_report(report_data)
            st.download_button(
                label="Download Detailed Report",
                data=report_buffer,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()