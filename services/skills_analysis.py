from services.llm_utils import call_llm
import json

def analyze_skills(resume, jd):
    prompt = f"""
    Perform a comprehensive skills analysis of the following resume against the job description.

    Resume:
    {resume}

    Job Description:
    {jd}

    Please provide a detailed JSON response with the following structure:
    {{
        "matched_skills": {{
            "must_have": ["list of matched must-have skills"],
            "nice_to_have": ["list of matched nice-to-have skills"],
            "additional": ["list of other relevant skills found"]
        }},
        "missing_skills": {{
            "critical": ["list of missing critical skills"],
            "important": ["list of missing important skills"],
            "optional": ["list of missing optional skills"]
        }},
        "skill_gaps": {{
            "high_priority": ["skills that should be prioritized"],
            "medium_priority": ["skills that would be beneficial"],
            "low_priority": ["skills that are nice to have"]
        }},
        "skill_analysis": {{
            "technical_skills_match": <0-100>,
            "soft_skills_match": <0-100>,
            "domain_knowledge_match": <0-100>
        }},
        "recommendations": ["list of skill development recommendations"]
    }}

    Focus on:
    1. Technical skills (programming languages, frameworks, tools)
    2. Soft skills (communication, leadership, problem-solving)
    3. Domain knowledge (industry-specific expertise)
    4. Experience level alignment
    5. Project relevance
    """
    
    response = call_llm(prompt)
    try:
        return json.loads(response)
    except Exception:
        return {
            "error": "Could not parse response", 
            "raw_response": response,
            "matched_skills": {"must_have": [], "nice_to_have": [], "additional": []},
            "missing_skills": {"critical": [], "important": [], "optional": []}
        }
