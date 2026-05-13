
    # Quantified achievements (numbers/percentages)
    quantified = re.findall(r'\d+[\%\+xX]|\d+\s*(million|billion|thousand|k\b)', text_lower)
    if len(quantified) >= 5:
        score += 30
        feedback.append("✅ Good use of quantified achievements")
    elif len(quantified) >= 2:
        score += 15
        feedback.append("⚠️ Add more quantified results (%, numbers, impact)")
    else:
        feedback.append("❌ Missing quantified achievements - add metrics to your experience")

    if len(found_verbs) >= 8:
        feedback.append("✅ Strong action verbs used effectively")
    else:
        feedback.append("⚠️ Use more action verbs (built, developed, optimized, etc.)")

    return min(100, score), feedback


def score_skills_relevance(extracted_skills: List[str]) -> Tuple[float, List[str]]:
    """
    Score the relevance and quantity of technical skills.

    Args:
        extracted_skills: List of detected skills

    Returns:
        Tuple of (score 0-100, feedback messages)
    """
    feedback = []
    score = 0

    skill_count = len(extracted_skills)

    # Score based on skill count
    if skill_count >= 20:
        score = 90
        feedback.append("✅ Comprehensive skill set detected")
    elif skill_count >= 15:
        score = 75
        feedback.append("✅ Good number of technical skills")
    elif skill_count >= 10:
        score = 60
        feedback.append("⚠️ Consider adding more technical skills")
    elif skill_count >= 5:
        score = 40
        feedback.append("❌ Limited skills detected - expand your skills section")
    else:
        score = 20
        feedback.append("❌ Very few skills found - ensure skills are clearly listed")

    # Bonus for variety across categories
    from datasets.job_descriptions import SKILLS_TAXONOMY
    categories_covered = 0
    for category, category_skills in SKILLS_TAXONOMY.items():
        if any(skill in extracted_skills for skill in category_skills):
            categories_covered += 1

    if categories_covered >= 4:
        score = min(100, score + 10)
        feedback.append("✅ Good diversity across skill categories")
    elif categories_covered <= 1:
        feedback.append("⚠️ Diversify your skill set across more categories")

    return score, feedback


def score_structure_quality(text: str, sections: Dict) -> Tuple[float, List[str]]:
    """
    Score the structural quality of the resume.

    Args:
        text: Resume text
        sections: Detected sections dict

    Returns:
        Tuple of (score 0-100, feedback messages)
    """
    feedback = []
    score = 0

    # Check for essential sections
    essential_sections = {
        "summary": ("Professional summary", 15),
        "experience": ("Work experience", 25),
        "education": ("Education section", 20),
        "skills": ("Skills section", 20),
    }

    for section_key, (section_name, points) in essential_sections.items():
        if section_key in sections and len(sections[section_key]) > 30:
            score += points
            feedback.append(f"✅ {section_name} present")
        else:
            feedback.append(f"❌ {section_name} missing or too short")

    # Check for projects section
    if "projects" in sections and len(sections.get("projects", "")) > 30:
        score += 10
        feedback.append("✅ Projects section adds value")
    else:
        feedback.append("⚠️ Consider adding a Projects section")

    # Check text length (500-1000 words for single page)
    word_count = len(text.split())
    if 400 <= word_count <= 1200:
        score += 10
        feedback.append(f"✅ Good resume length ({word_count} words)")
    elif word_count < 200:
        feedback.append("❌ Resume is too short - expand your content")
    else:
        feedback.append("⚠️ Resume might be too long - aim for 1-2 pages")

    return min(100, score), feedback


def score_experience_section(text: str, sections: Dict) -> Tuple[float, List[str]]:
    """
    Score the quality of the experience section.

    Args:
        text: Resume text
        sections: Detected sections

    Returns:
        Tuple of (score 0-100, feedback messages)
    """
    feedback = []
    score = 0

    exp_text = sections.get("experience", text)

    # Check for date ranges
    date_pattern = r'(20\d{2})\s*[-–]\s*(20\d{2}|present|current)'
    dates = re.findall(date_pattern, exp_text, re.IGNORECASE)

    if len(dates) >= 2:
        score += 25
        feedback.append("✅ Clear employment timeline with dates")
    elif len(dates) == 1:
        score += 15
        feedback.append("⚠️ Add dates for all positions")
    else:
        feedback.append("❌ Add employment dates to all positions")

    # Check for company names (Title Case words)
    company_pattern = r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*(?:\s(?:Inc|LLC|Ltd|Corp|Co|Technologies|Solutions|Group)\.?)?'
    companies = re.findall(company_pattern, exp_text)
    if len(companies) >= 2:
        score += 20
        feedback.append("✅ Multiple work experiences detected")
    elif len(companies) == 1:
        score += 10
        feedback.append("ℹ️ One work experience found")

    # Check for bullet points / responsibilities
    bullet_indicators = text.count('•') + text.count('-') + text.count('·')
    if bullet_indicators >= 6:
        score += 25
        feedback.append("✅ Good use of bullet points for responsibilities")
    elif bullet_indicators >= 3:
        score += 15
        feedback.append("⚠️ Add more bullet points to detail responsibilities")
    else:
        feedback.append("❌ Format experience as bullet points")

    # Check for impact/numbers
    numbers = re.findall(r'\b\d+[\%\+]|\b\d+\s*(million|thousand|users|customers)', exp_text.lower())
    if len(numbers) >= 3:
        score += 30
        feedback.append("✅ Strong quantified impact in experience")
    elif len(numbers) >= 1:
        score += 15
        feedback.append("⚠️ Add more quantified impact metrics")
    else:
        feedback.append("❌ Include metrics (% improvements, team size, scale)")

    return min(100, score), feedback


def score_education_section(text: str, sections: Dict, education_info: Dict) -> Tuple[float, List[str]]:
    """
    Score the education section completeness.

    Args:
        text: Resume text
        sections: Detected sections
        education_info: Extracted education info

    Returns:
        Tuple of (score 0-100, feedback messages)
    """
    feedback = []
    score = 0

    if "education" not in sections or len(sections.get("education", "")) < 20:
        feedback.append("❌ Education section missing")
        return 0, feedback

    score += 30  # Base score for having education

    # Check for degree
    if education_info.get("degree"):
        score += 30
        feedback.append(f"✅ Degree detected: {education_info['degree']}")
    else:
        feedback.append("⚠️ Degree type not clearly stated")

    # Check for field of study
    if education_info.get("field"):
        score += 20
        feedback.append(f"✅ Field of study: {education_info['field']}")
    else:
        feedback.append("⚠️ Field of study not clearly stated")

    # Check for GPA
    if education_info.get("gpa") and education_info["gpa"] >= 3.0:
        score += 10
        feedback.append(f"✅ GPA listed: {education_info['gpa']}")
    elif education_info.get("gpa") and education_info["gpa"] < 3.0:
        feedback.append("⚠️ Consider omitting GPA below 3.0")

    # Check for graduation year
    if education_info.get("graduation_year"):
        score += 10
        feedback.append(f"✅ Graduation year: {education_info['graduation_year']}")

    return min(100, score), feedback


def score_contact_info(contact_info: Dict) -> Tuple[float, List[str]]:
    """
    Score the completeness of contact information.

    Args:
        contact_info: Extracted contact information

    Returns:
        Tuple of (score 0-100, feedback messages)
    """
    feedback = []
    score = 0

    if contact_info.get("email"):
        score += 40
        feedback.append("✅ Email address present")
    else:
        feedback.append("❌ Email address missing")

    if contact_info.get("phone"):
        score += 25
        feedback.append("✅ Phone number present")
    else:
        feedback.append("⚠️ Phone number missing")

    if contact_info.get("linkedin"):
        score += 20
        feedback.append("✅ LinkedIn profile linked")
    else:
        feedback.append("⚠️ Add LinkedIn profile URL")

    if contact_info.get("github"):
        score += 15
        feedback.append("✅ GitHub profile linked")
    else:
        feedback.append("ℹ️ Consider adding GitHub profile")

    return score, feedback


def score_additional_sections(sections: Dict) -> Tuple[float, List[str]]:
    """
    Score additional resume sections (projects, certifications, etc.)

    Args:
        sections: Detected sections

    Returns:
        Tuple of (score 0-100, feedback messages)
    """
    feedback = []
    score = 0

    if "projects" in sections and len(sections.get("projects", "")) > 50:
        score += 40
        feedback.append("✅ Projects section present")
    else:
        feedback.append("⚠️ Add relevant projects to strengthen your resume")

    if "certifications" in sections and len(sections.get("certifications", "")) > 20:
        score += 40
        feedback.append("✅ Certifications section present")
    else:
        feedback.append("ℹ️ Industry certifications can boost your profile")

    if "languages" in sections and len(sections.get("languages", "")) > 10:
        score += 20
        feedback.append("✅ Programming languages section present")

    return min(100, score), feedback


def calculate_ats_score(
    text: str,
    sections: Dict,
    extracted_skills: List[str],
    contact_info: Dict,
    education_info: Dict
) -> Dict:
    """
    Calculate comprehensive ATS compatibility score.

    Args:
        text: Full resume text
        sections: Detected sections
        extracted_skills: Extracted skills list
        contact_info: Extracted contact info
        education_info: Extracted education info

    Returns:
        Comprehensive ATS score report
    """
    scores = {}
    all_feedback = {}

    # Score each component
    scores["keyword_optimization"], all_feedback["keyword_optimization"] = \
        score_keyword_optimization(text, extracted_skills)

    scores["skills_relevance"], all_feedback["skills_relevance"] = \
        score_skills_relevance(extracted_skills)

    scores["structure_quality"], all_feedback["structure_quality"] = \
        score_structure_quality(text, sections)

    scores["experience_section"], all_feedback["experience_section"] = \
        score_experience_section(text, sections)

    scores["education_section"], all_feedback["education_section"] = \
        score_education_section(text, sections, education_info)

    scores["contact_completeness"], all_feedback["contact_completeness"] = \
        score_contact_info(contact_info)

    scores["additional_sections"], all_feedback["additional_sections"] = \
        score_additional_sections(sections)

    # Calculate weighted total
    total_score = 0
    for component, weight in SCORING_WEIGHTS.items():
        component_score = scores.get(component, 0)
        weighted = (component_score / 100) * weight
        total_score += weighted

    total_score = round(min(100, total_score))

    # Determine ATS tier
    if total_score >= 85:
        tier = "Excellent"
        tier_color = "green"
        tier_message = "Your resume is highly ATS-optimized! Strong candidate."
    elif total_score >= 70:
        tier = "Good"
        tier_color = "blue"
        tier_message = "Your resume performs well with ATS. Minor improvements needed."
    elif total_score >= 55:
        tier = "Fair"
        tier_color = "orange"
        tier_message = "Your resume needs improvements to pass ATS filters effectively."
    elif total_score >= 40:
        tier = "Poor"
        tier_color = "red"
        tier_message = "Your resume may be filtered out by ATS. Significant updates needed."
    else:
        tier = "Critical"
        tier_color = "darkred"
        tier_message = "Your resume is unlikely to pass ATS screening. Major revision needed."

    # Collect all feedback messages
    positive_feedback = []
    improvement_feedback = []

    for component, messages in all_feedback.items():
        for msg in messages:
            if msg.startswith("✅"):
                positive_feedback.append(msg)
            else:
                improvement_feedback.append(msg)

    return {
        "total_score": total_score,
        "tier": tier,
        "tier_color": tier_color,
        "tier_message": tier_message,
        "component_scores": scores,
        "scoring_weights": SCORING_WEIGHTS,
        "positive_feedback": positive_feedback,
        "improvement_feedback": improvement_feedback,
        "all_feedback": all_feedback,
    }


def get_improvement_priority(ats_result: Dict) -> List[Dict]:
    """
    Prioritize improvements based on their potential score impact.

    Args:
        ats_result: ATS score result dict

    Returns:
        Sorted list of improvement opportunities
    """
    improvements = []

    for component, score in ats_result["component_scores"].items():
        if score < 80:  # Room for improvement
            weight = SCORING_WEIGHTS[component]
            potential_gain = round((80 - score) / 100 * weight, 1)
            improvements.append({
                "component": component.replace("_", " ").title(),
                "current_score": score,
                "weight": weight,
                "potential_gain": potential_gain,
                "priority": "High" if weight >= 20 else ("Medium" if weight >= 10 else "Low")
            })

    return sorted(improvements, key=lambda x: x["potential_gain"], reverse=True)
