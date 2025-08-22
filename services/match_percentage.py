from services.llm_utils import call_llm

def get_match_score(resume, jd):
    prompt = f"""
    Compare the following resume and job description.
    Return ONLY the match percentage (0–100) based on relevance of skills, experience, and responsibilities.

    Resume:
    {resume}

    Job Description:
    {jd}
    """
    response = call_llm(prompt)
    return {"match_percentage": response.strip()}
