from services.llm_utils import call_llm
import json

def analyze_skills(resume, jd):
    prompt = f"""
    You are an expert skills analyst. Analyze the following resume against the job description and provide ONLY a valid JSON response.

    RESUME:
    {resume}

    JOB DESCRIPTION:
    {jd}

    IMPORTANT: Respond with ONLY valid JSON. No additional text before or after the JSON.

    JSON STRUCTURE:
    {{
        "matched_skills": {{
            "must_have": ["exact must-have skills found"],
            "nice_to_have": ["exact nice-to-have skills found"],
            "additional": ["other relevant skills found"]
        }},
        "missing_skills": {{
            "critical": ["critical missing skills"],
            "important": ["important missing skills"],
            "optional": ["optional missing skills"]
        }},
        "skill_gaps": {{
            "high_priority": ["high priority skills to learn"],
            "medium_priority": ["medium priority skills to learn"],
            "low_priority": ["low priority skills to learn"]
        }},
        "skill_analysis": {{
            "technical_skills_match": <number 0-100>,
            "soft_skills_match": <number 0-100>,
            "domain_knowledge_match": <number 0-100>
        }},
        "recommendations": ["specific skill development recommendations"]
    }}

    ANALYSIS FOCUS:
    1. Must-have skills: Java (required)
    2. Nice-to-have skills: JavaScript (preferred)
    3. Technical skills: Programming languages, frameworks, tools
    4. Soft skills: Communication, leadership, problem-solving
    5. Domain knowledge: Industry-specific expertise
    6. Experience alignment: Years of experience vs requirements
    """
    
    response = call_llm(prompt, temperature=0.5)
    
    # Try to extract JSON from the response
    try:
        # First, try direct JSON parsing
        return json.loads(response)
    except json.JSONDecodeError:
        # If that fails, try to extract JSON from the response
        try:
            # Look for JSON content between curly braces
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # If all else fails, return error with raw response
        return {
            "error": "Could not parse response", 
            "raw_response": response,
            "matched_skills": {"must_have": [], "nice_to_have": [], "additional": []},
            "missing_skills": {"critical": [], "important": [], "optional": []},
            "skill_gaps": {"high_priority": [], "medium_priority": [], "low_priority": []},
            "skill_analysis": {"technical_skills_match": 0, "soft_skills_match": 0, "domain_knowledge_match": 0},
            "recommendations": []
        }
