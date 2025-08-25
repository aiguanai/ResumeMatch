from services.llm_utils import call_llm
import json

def get_match_score(resume, jd):
    prompt = f"""
    Analyze the following resume against the job description and provide a comprehensive match assessment.

    Resume:
    {resume}

    Job Description:
    {jd}

    Please provide a JSON response with the following structure:
    {{
        "overall_match_percentage": <0-100>,
        "skills_match_percentage": <0-100>,
        "experience_match_percentage": <0-100>,
        "education_match_percentage": <0-100>,
        "detailed_analysis": {{
            "strengths": ["list of strengths"],
            "weaknesses": ["list of weaknesses"],
            "recommendations": ["list of recommendations"]
        }},
        "key_matches": ["list of key matching points"],
        "missing_requirements": ["list of missing requirements"]
    }}

    Focus on:
    1. Technical skills alignment
    2. Experience level match
    3. Educational background
    4. Project relevance
    5. Industry experience
    """
    
    response = call_llm(prompt)
    try:
        return json.loads(response)
    except Exception:
        return {
            "error": "Could not parse response", 
            "raw_response": response,
            "overall_match_percentage": "N/A"
        }
