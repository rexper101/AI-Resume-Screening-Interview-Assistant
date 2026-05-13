"""
skill_extractor.py - NLP-based skill extraction from resume text.
Uses keyword matching, NLP preprocessing, and pattern recognition.
"""

import re
from typing import List, Dict, Tuple
from collections import Counter

# Import dataset
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from datasets.job_descriptions import SKILLS_TAXONOMY


# ── Master skills list (flattened from taxonomy) ──────────────────────────────
ALL_SKILLS = []
for category, skills in SKILLS_TAXONOMY.items():
    ALL_SKILLS.extend(skills)
ALL_SKILLS = list(set(ALL_SKILLS))

# Skills that need exact phrase matching (multi-word)
MULTI_WORD_SKILLS = [s for s in ALL_SKILLS if ' ' in s]
SINGLE_WORD_SKILLS = [s for s in ALL_SKILLS if ' ' not in s]

# Additional skill aliases / synonyms
SKILL_ALIASES = {
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "tf": "tensorflow",
    "sk-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "gcp": "google cloud",
    "k8s": "kubernetes",
    "pg": "postgresql",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "hf": "hugging face",
    "lc": "langchain",
    "llms": "llm",
    "bert": "transformers",
    "gpt": "llm",
    "openai": "openai",
    "aws sagemaker": "aws",
    "amazon web services": "aws",
    "microsoft azure": "azure",
    "google cloud platform": "google cloud",
    "node": "node.js",
    "nodejs": "node.js",
    "vue": "vue.js",
    "next": "next.js",
    "angular js": "angular",
    "spring": "spring boot",
    "power bi": "power bi",
    "powerbi": "power bi",
    "tableau desktop": "tableau",
    "ms excel": "excel",
    "github actions": "ci/cd",
    "gitlab ci": "ci/cd",
    "jenkins": "ci/cd",
}


def preprocess_text(text: str) -> str:
    """
    Lowercase and normalize text for skill matching.
    """
    text = text.lower()
    # Normalize punctuation
    text = re.sub(r'[/\\|]', ' ', text)
    text = re.sub(r'[\(\)\[\]\{\}]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def apply_aliases(text: str) -> str:
    """
    Replace skill aliases with canonical names.
    """
    for alias, canonical in SKILL_ALIASES.items():
        text = re.sub(r'\b' + re.escape(alias) + r'\b', canonical, text)
    return text


def extract_skills_by_keyword(text: str) -> List[str]:
    """
    Extract skills using keyword matching against the skills taxonomy.

    Args:
        text: Resume text

    Returns:
        List of detected skill names
    """
    processed = preprocess_text(text)
    processed = apply_aliases(processed)

    found_skills = set()

    # Match multi-word skills first (higher priority)
    for skill in MULTI_WORD_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, processed):
            found_skills.add(skill)

    # Match single-word skills
    for skill in SINGLE_WORD_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, processed):
            found_skills.add(skill)

    return sorted(list(found_skills))


def extract_skills_by_section(sections: dict) -> Dict[str, List[str]]:
    """
    Extract skills from specific resume sections with weighted importance.

    Args:
        sections: Dict of resume sections from resume_parser

    Returns:
        Dict mapping section → skills found
    """
    section_skills = {}

    priority_sections = ["skills", "experience", "projects", "certifications", "summary"]

    for section_name in priority_sections:
        if section_name in sections:
            skills = extract_skills_by_keyword(sections[section_name])
            if skills:
                section_skills[section_name] = skills

    return section_skills


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """
    Categorize detected skills into taxonomy groups.

    Args:
        skills: List of skill strings

    Returns:
        Dict mapping category → list of skills in that category
    """
    categorized = {cat: [] for cat in SKILLS_TAXONOMY.keys()}
    categorized["other"] = []

    for skill in skills:
        found_category = False
        for category, category_skills in SKILLS_TAXONOMY.items():
            if skill in category_skills:
                categorized[category].append(skill)
                found_category = True
                break
        if not found_category:
            categorized["other"].append(skill)

    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}


def get_skill_frequency(skills: List[str], text: str) -> Dict[str, int]:
    """
    Count how many times each skill is mentioned in the resume.

    Args:
        skills: List of skills to count
        text: Full resume text

    Returns:
        Dict mapping skill → frequency count
    """
    processed = preprocess_text(text)
    frequency = {}

    for skill in skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        matches = re.findall(pattern, processed)
        frequency[skill] = len(matches)

    return dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))


def extract_experience_years(text: str) -> Dict[str, any]:
    """
    Extract years of experience from resume text.

    Args:
        text: Resume text

    Returns:
        Dict with experience information
    """
    experience_info = {
        "total_years": 0,
        "year_ranges": [],
        "estimated_level": "Entry Level"
    }

    # Find year ranges like "2019 - 2023" or "2019-Present"
    year_range_pattern = r'(20\d{2})\s*[-–]\s*(20\d{2}|present|current)'
    ranges = re.findall(year_range_pattern, text, re.IGNORECASE)

    if ranges:
        experience_info["year_ranges"] = ranges
        total = 0
        from datetime import datetime
        current_year = datetime.now().year
        for start, end in ranges:
            start_year = int(start)
            end_year = current_year if end.lower() in ['present', 'current'] else int(end)
            total += max(0, end_year - start_year)
        experience_info["total_years"] = min(total, 40)  # cap at 40

    # Determine seniority level
    years = experience_info["total_years"]
    if years == 0:
        level = "Fresher/Student"
    elif years <= 1:
        level = "Entry Level"
    elif years <= 3:
        level = "Junior"
    elif years <= 5:
        level = "Mid-Level"
    elif years <= 8:
        level = "Senior"
    else:
        level = "Lead/Principal"

    experience_info["estimated_level"] = level
    return experience_info


def extract_education_info(text: str) -> Dict[str, any]:
    """
    Extract education details from resume text.

    Args:
        text: Resume text

    Returns:
        Dict with education information
    """
    edu_info = {
        "degree": None,
        "field": None,
        "institution": None,
        "gpa": None,
        "graduation_year": None
    }

    text_lower = text.lower()

    # Detect degree level
    degree_patterns = [
        (r'\b(ph\.?d\.?|doctorate|doctor of)\b', "PhD"),
        (r'\b(m\.?s\.?|master\'?s?|msc|m\.?tech|mba)\b', "Master's"),
        (r'\b(b\.?s\.?|bachelor\'?s?|bsc|b\.?tech|b\.?e\.?|undergraduate)\b', "Bachelor's"),
        (r'\b(associate\'?s?|a\.?s\.?|a\.?a\.?)\b', "Associate's"),
        (r'\b(diploma|certificate)\b', "Diploma/Certificate"),
    ]

    for pattern, degree_name in degree_patterns:
        if re.search(pattern, text_lower):
            edu_info["degree"] = degree_name
            break

    # Common CS/Data Science fields
    field_keywords = [
        "computer science", "data science", "information technology",
        "software engineering", "electrical engineering", "mathematics",
        "statistics", "machine learning", "artificial intelligence",
        "information systems", "computer engineering"
    ]
    for field in field_keywords:
        if field in text_lower:
            edu_info["field"] = field.title()
            break

    # GPA
    gpa_pattern = r'gpa:?\s*(\d\.\d+)'
    gpa_match = re.search(gpa_pattern, text_lower)
    if gpa_match:
        edu_info["gpa"] = float(gpa_match.group(1))

    # Graduation year
    year_pattern = r'\b(20\d{2})\b'
    years = re.findall(year_pattern, text)
    if years:
        edu_info["graduation_year"] = max(years)

    return edu_info


def extract_all(text: str, sections: dict) -> dict:
    """
    Main extraction function combining all extractors.

    Args:
        text: Full resume text
        sections: Detected sections from resume_parser

    Returns:
        Complete skills and metadata extraction result
    """
    # Extract skills
    all_skills = extract_skills_by_keyword(text)
    section_skills = extract_skills_by_section(sections)
    categorized = categorize_skills(all_skills)
    frequency = get_skill_frequency(all_skills, text)

    # Extract metadata
    experience_info = extract_experience_years(text)
    education_info = extract_education_info(text)

    # Skills from skills section get a "primary skill" flag
    primary_skills = section_skills.get("skills", [])
    secondary_skills = [s for s in all_skills if s not in primary_skills]

    return {
        "all_skills": all_skills,
        "primary_skills": primary_skills,
        "secondary_skills": secondary_skills,
        "categorized_skills": categorized,
        "skill_frequency": frequency,
        "section_skills": section_skills,
        "experience_info": experience_info,
        "education_info": education_info,
        "total_skills_count": len(all_skills)
    }
