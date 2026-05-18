"""
resume_parser.py - Handles resume file upload and text extraction.
Supports PDF files with fallback error handling.
"""

import re
import io
from typing import Optional


def extract_text_from_pdf(file) -> str:
    """
    Extract raw text from a PDF file object.
    Tries pdfplumber first (better layout handling), falls back to PyPDF2.

    Args:
        file: File-like object (from Streamlit uploader)

    Returns:
        Extracted text string
    """
    text = ""

    # Try pdfplumber first (handles complex layouts better)
    try:
        import pdfplumber
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback to PyPDF2
    try:
        import PyPDF2
        if hasattr(file, 'seek'):
            file.seek(0)
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # Last fallback: try pypdf
    try:
        from pypdf import PdfReader
        if hasattr(file, 'seek'):
            file.seek(0)
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Could not extract text from PDF: {str(e)}")

    return text


def clean_resume_text(text: str) -> str:
    """
    Clean and normalize extracted resume text.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    # Fix common PDF extraction artifacts
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # camelCase splits

    return text.strip()


def detect_sections(text: str) -> dict:
    """
    Detect key sections in a resume using regex pattern matching.

    Args:
        text: Cleaned resume text

    Returns:
        Dict of detected section names and their content
    """
    sections = {}

    # Common section headers (case-insensitive)
    section_patterns = {
        "contact": r"(contact|personal\s+info|contact\s+information)",
        "summary": r"(summary|objective|profile|about\s+me|professional\s+summary)",
        "experience": r"(experience|work\s+experience|employment|work\s+history|professional\s+experience)",
        "education": r"(education|academic|qualification|degrees?)",
        "skills": r"(skills|technical\s+skills|core\s+competencies|technologies|expertise)",
        "projects": r"(projects|personal\s+projects|key\s+projects|portfolio)",
        "certifications": r"(certifications?|certificates?|credentials|licenses?|achievements?)",
        "languages": r"(languages?)",
    }

    lines = text.split('\n')
    current_section = "header"
    sections[current_section] = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Check if line is a section header
        found_section = False
        for section_name, pattern in section_patterns.items():
            if re.match(r'^' + pattern + r'[\s:]*$', line_stripped, re.IGNORECASE):
                current_section = section_name
                sections[current_section] = []
                found_section = True
                break

        if not found_section:
            sections.setdefault(current_section, []).append(line_stripped)

    # Convert lists to strings
    return {k: '\n'.join(v) for k, v in sections.items()}


def extract_contact_info(text: str) -> dict:
    """
    Extract contact information from resume text.

    Args:
        text: Resume text

    Returns:
        Dict with name, email, phone, linkedin, github
    """
    contact = {
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "location": None,
    }

    # Email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact["email"] = email_match.group()

    # Phone
    phone_pattern = r'(\+?[\d\s\-\(\)]{10,15})'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact["phone"] = phone_match.group().strip()

    # LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
    linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_match:
        contact["linkedin"] = linkedin_match.group()

    # GitHub
    github_pattern = r'github\.com/[\w\-]+'
    github_match = re.search(github_pattern, text, re.IGNORECASE)
    if github_match:
        contact["github"] = github_match.group()

    # Location (city, state/country)
    location_pattern = r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s*(?:[A-Z]{2}|[A-Z][a-z]+))\b'
    location_match = re.search(location_pattern, text)
    if location_match:
        contact["location"] = location_match.group()

    return contact


def calculate_resume_stats(text: str) -> dict:
    """
    Calculate basic statistics about the resume.

    Args:
        text: Resume text

    Returns:
        Dict with word count, page estimate, sections found
    """
    words = text.split()
    sections = detect_sections(text)

    # Estimate pages (average 400 words per page for resumes)
    estimated_pages = max(1, round(len(words) / 400, 1))

    # Count years of experience from text
    year_matches = re.findall(r'\b(19|20)(\d{2})\b', text)
    unique_years = sorted(set([int(a + b) for a, b in year_matches]))

    has_sections = {
        "has_summary": "summary" in sections and len(sections.get("summary", "")) > 20,
        "has_experience": "experience" in sections and len(sections.get("experience", "")) > 20,
        "has_education": "education" in sections and len(sections.get("education", "")) > 20,
        "has_skills": "skills" in sections and len(sections.get("skills", "")) > 10,
        "has_projects": "projects" in sections and len(sections.get("projects", "")) > 20,
        "has_certifications": "certifications" in sections and len(sections.get("certifications", "")) > 10,
    }

    return {
        "word_count": len(words),
        "char_count": len(text),
        "estimated_pages": estimated_pages,
        "sections_detected": [k for k, v in has_sections.items() if v],
        **has_sections
    }


def parse_resume(file) -> dict:
    """
    Main function to parse a resume file and return structured data.

    Args:
        file: Uploaded file object from Streamlit

    Returns:
        Dict containing all parsed resume data
    """
    # Extract raw text
    raw_text = extract_text_from_pdf(file)

    if not raw_text.strip():
        raise ValueError("No text could be extracted from the PDF. The file may be scanned or image-based.")

    # Clean the text
    cleaned_text = clean_resume_text(raw_text)

    # Extract structured data
    sections = detect_sections(cleaned_text)
    contact_info = extract_contact_info(cleaned_text)
    stats = calculate_resume_stats(cleaned_text)

    return {
        "raw_text": raw_text,
        "cleaned_text": cleaned_text,
        "sections": sections,
        "contact_info": contact_info,
        "stats": stats
    }


def get_sample_resume_text() -> str:
    """
    Returns a sample resume text for demo purposes when no file is uploaded.
    """
    return """
John Smith
john.smith@email.com | +1-555-0123 | linkedin.com/in/johnsmith | github.com/johnsmith
San Francisco, CA

PROFESSIONAL SUMMARY
Passionate Data Scientist with 3+ years of experience building machine learning models and
data pipelines. Expertise in Python, SQL, and cloud technologies. Proven track record of
delivering end-to-end ML solutions from data collection to production deployment.

WORK EXPERIENCE

Senior Data Scientist | TechCorp Inc. | 2022 - Present
- Built and deployed machine learning models for customer churn prediction (92% accuracy)
- Developed NLP pipeline for sentiment analysis using BERT and TensorFlow
- Reduced data processing time by 60% using Apache Spark and AWS EMR
- Mentored junior data scientists and conducted code reviews

Data Scientist | DataStartup | 2021 - 2022
- Created recommendation system using collaborative filtering and matrix factorization
- Built automated ETL pipelines using Apache Airflow and Python
- Performed A/B testing and statistical analysis for product experiments
- Developed dashboards using Tableau and Power BI for business stakeholders

Data Analyst Intern | Analytics Co. | 2020 - 2021
- Analyzed large datasets using SQL and Python (Pandas, NumPy)
- Created data visualizations using Matplotlib, Seaborn, and Plotly
- Built automated reporting pipelines using Python scripts

EDUCATION
Bachelor of Science in Computer Science | Stanford University | 2020
- GPA: 3.8/4.0
- Relevant Coursework: Machine Learning, Statistics, Algorithms, Database Systems

TECHNICAL SKILLS
Programming: Python, SQL, R, Scala, Bash
ML/AI: Machine Learning, Deep Learning, NLP, Computer Vision, TensorFlow, PyTorch, Scikit-learn
Data: Pandas, NumPy, Spark, Hadoop, Kafka, ETL
Visualization: Matplotlib, Seaborn, Plotly, Tableau, Power BI
Cloud/DevOps: AWS (EC2, S3, SageMaker, Lambda), Docker, Kubernetes, CI/CD, Git
Databases: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch

PROJECTS

Real-time Fraud Detection System
- Built ML pipeline detecting fraudulent transactions in real-time using Random Forest and XGBoost
- Achieved 99.2% precision and deployed on AWS using Docker and FastAPI
- Technologies: Python, Scikit-learn, AWS, Docker, Redis

Customer Segmentation Engine
- Developed K-Means and DBSCAN clustering models for customer behavior analysis
- Built interactive Streamlit dashboard for business stakeholders
- Technologies: Python, Pandas, Plotly, Streamlit, PostgreSQL

CERTIFICATIONS
- AWS Certified Machine Learning Specialty (2023)
- Google Professional Data Engineer (2022)
- TensorFlow Developer Certificate (2021)
"""
