from models import Student


def classify_opportunity(description: str) -> str:
    """
    Classify an opportunity based on keywords in its description.
    
    Returns domain category: AI, Law, Biomedical, Engineering, or General.
    """
    desc_lower = description.lower()
    
    if any(kw in desc_lower for kw in ["ai", "machine learning", "neural", "deep learning"]):
        return "AI"
    elif any(kw in desc_lower for kw in ["law", "policy", "legal"]):
        return "Law"
    elif any(kw in desc_lower for kw in ["biomedical", "health", "clinical"]):
        return "Biomedical"
    elif any(kw in desc_lower for kw in ["robotics", "engineering", "hardware"]):
        return "Engineering"
    else:
        return "General"


def calculate_incoscore(student: Student) -> float:
    """
    Calculate the InCoScore (Intelligence & Competency Score) for a student.
    
    Formula: hackathons*2 + internships*3 + research_papers*4 + coding_score*0.1
    """
    score = (
        student.hackathons * 2 +
        student.internships * 3 +
        student.research_papers * 4 +
        student.coding_score * 0.1
    )
    return round(score, 2)
