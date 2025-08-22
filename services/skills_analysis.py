from services.llm_utils import call_llm
import json

def analyze_skills(resume, jd):
    prompt = f"""
    Analyze the skills in the following resume against the job description.

    Resume:
    {resume}

    Job Description:
    {jd}

    TASK:
    Return JSON with:
    - "matched_skills": [...]
    - "missing_skills": [...]

    Example:
    {{
      "matched_skills": ["Java", "Spring"],
      "missing_skills": ["JavaScript", "Tomcat"]
    }}
    """
    response = call_llm(prompt)
    try:
        return json.loads(response)
    except Exception:
        return {"error": "Could not parse response", "raw_response": response}
