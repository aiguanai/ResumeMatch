from services.llm_utils import call_llm
import json

def get_match_score(resume, jd, is_batch_analysis=False):
    """
    Analyze a single resume against a job description.
    
    Args:
        resume: Resume text content
        jd: Job description text
        is_batch_analysis: Whether this is part of a batch analysis
    """
    
    if is_batch_analysis:
        prompt = f"""
        You are an expert HR recruiter analyzing a resume against a job description. This is part of a batch analysis - score each resume independently and accurately.

        RESUME:
        {resume}

        JOB DESCRIPTION:
        {jd}

        CRITICAL: Score this resume independently as if it's the only resume you're analyzing. Do not be influenced by other resumes in the batch.

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

        IMPORTANT: 
        1. Score this resume independently - ignore any batch context
        2. Provide specific, nuanced scores based on actual content
        3. Do not use generic or conservative scores
        4. Consider exact technical skills match, experience level, education quality
        5. Be precise: if a candidate deserves 90%, give them 90%, not 85%
        """
    else:
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
    
    # Use higher temperature for batch analysis to encourage more varied responses
    temperature = 0.9 if is_batch_analysis else 0.8
    response = call_llm(prompt, temperature=temperature)
    
    try:
        return json.loads(response)
    except Exception:
        return {
            "error": "Could not parse response", 
            "raw_response": response,
            "overall_match_percentage": "N/A"
        }
