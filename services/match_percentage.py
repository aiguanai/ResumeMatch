from services.llm_utils import call_llm
import json

def get_match_score(resume, jd):
    prompt = f"""
    You are an expert HR recruiter analyzing a resume against a job description. Provide a detailed, nuanced assessment with specific scoring.

    RESUME:
    {resume}

    JOB DESCRIPTION:
    {jd}

    SCORING GUIDELINES:
    - Overall Match (0-100): Consider all factors holistically
    - Skills Match (0-100): Technical skills alignment with must-have and nice-to-have skills
    - Experience Match (0-100): Years of experience and relevance to role
    - Education Match (0-100): Educational background alignment

    SCORING CRITERIA:
    90-100: Perfect match, exceeds requirements
    80-89: Strong match, meets most requirements
    70-79: Good match, meets core requirements
    60-69: Fair match, some gaps
    50-59: Below average, significant gaps
    0-49: Poor match, major gaps

    Please provide a detailed JSON response with the following structure:
    {{
        "overall_match_percentage": <specific number 0-100>,
        "skills_match_percentage": <specific number 0-100>,
        "experience_match_percentage": <specific number 0-100>,
        "education_match_percentage": <specific number 0-100>,
        "detailed_analysis": {{
            "strengths": ["specific strengths with details"],
            "weaknesses": ["specific weaknesses with details"],
            "recommendations": ["specific actionable recommendations"]
        }},
        "key_matches": ["specific matching points"],
        "missing_requirements": ["specific missing requirements"]
    }}

    IMPORTANT: Provide specific, nuanced scores based on the actual content. Do not use generic scores. Consider:
    1. Exact technical skills match (Java, JavaScript, Spring, etc.)
    2. Years of experience vs. requirements (4-7 years)
    3. Project relevance and complexity
    4. Educational background quality
    5. Leadership and management experience
    6. Industry-specific experience
    """
    
    response = call_llm(prompt, temperature=0.8)
    try:
        return json.loads(response)
    except Exception:
        return {
            "error": "Could not parse response", 
            "raw_response": response,
            "overall_match_percentage": "N/A"
        }
