#!/usr/bin/env python3
"""
Test script to verify batch scoring fix
"""

import requests
import json

def test_batch_scoring():
    """Test that batch analysis provides different scores"""
    
    # Test data - different resumes with different qualifications
    resume1 = """
    SENIOR SOFTWARE ENGINEER
    
    EXPERIENCE:
    - 7 years of experience in Java development
    - Expert in Spring Framework, MySQL, Linux
    - Led development of systems processing 30M+ requests daily
    - Strong leadership and project management experience
    
    SKILLS:
    - Java, Spring Framework, MySQL, Linux, Tomcat
    - JavaScript, React, Node.js
    - Object-Relational Mapping, Direct SQL
    - Microservices architecture, Docker, Kubernetes
    
    EDUCATION:
    - Master's Degree in Computer Science
    """
    
    resume2 = """
    JUNIOR DEVELOPER
    
    EXPERIENCE:
    - 2 years of experience in Python development
    - Basic web development experience
    - Some database experience
    
    SKILLS:
    - Python, Django, SQLite
    - HTML, CSS, JavaScript
    - Git version control
    
    EDUCATION:
    - Bachelor's Degree in Computer Science
    """
    
    resume3 = """
    MID-LEVEL DEVELOPER
    
    EXPERIENCE:
    - 4 years of experience in Java development
    - Good experience with Spring Boot
    - Some database and cloud experience
    
    SKILLS:
    - Java, Spring Boot, MySQL
    - Basic JavaScript, HTML, CSS
    - AWS, Docker basics
    
    EDUCATION:
    - Bachelor's Degree in Computer Science
    """
    
    job_description = """
    Senior Software Engineer
    Location: Remote
    Experience Required: 4-7 years
    
    Key Skills:
    Must-Have: Java
    Nice-to-Have: JavaScript
    
    Job Description:
    We are seeking a Senior Software Engineer with strong Java experience.
    """
    
    print("🧪 Testing Batch Scoring Fix")
    print("=" * 50)
    
    # Test single resume analysis
    print("\n📄 Testing Single Resume Analysis:")
    response = requests.post('http://localhost:5000/analyze', data={
        'apiKey': 'test_key',  # You'll need to replace this with a real key
        'jobTitle': 'Senior Software Engineer',
        'experience': '4-7 years',
        'location': 'Remote',
        'industry': 'Information Technology',
        'mustHaveSkills': 'Java',
        'niceToHaveSkills': 'JavaScript',
        'jobDescription': job_description,
        'uploadType': 'single'
    }, files={
        'singleResume': ('resume1.txt', resume1, 'text/plain')
    })
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            score = result['results'][0]['match_analysis'].get('overall_match_percentage', 'N/A')
            print(f"  Resume 1 (Single): {score}%")
        else:
            print(f"  Error: {result.get('error', 'Unknown error')}")
    else:
        print(f"  HTTP Error: {response.status_code}")
    
    # Test batch analysis
    print("\n📁 Testing Batch Resume Analysis:")
    
    # Create a simple test with multiple resumes
    resumes = {
        'resume1.txt': resume1,
        'resume2.txt': resume2,
        'resume3.txt': resume3
    }
    
    # Simulate batch analysis by calling the function directly
    from services.match_percentage import get_match_score
    
    print("  Analyzing resumes individually with batch flag:")
    
    for filename, resume_text in resumes.items():
        # Test with batch analysis flag
        result = get_match_score(resume_text, job_description, is_batch_analysis=True)
        score = result.get('overall_match_percentage', 'N/A')
        print(f"    {filename}: {score}%")
    
    print("\n  Analyzing resumes individually without batch flag:")
    
    for filename, resume_text in resumes.items():
        # Test without batch analysis flag
        result = get_match_score(resume_text, job_description, is_batch_analysis=False)
        score = result.get('overall_match_percentage', 'N/A')
        print(f"    {filename}: {score}%")
    
    print("\n✅ Test completed!")
    print("\nExpected Results:")
    print("- Resume 1 (Senior): Should score 85-95%")
    print("- Resume 2 (Junior): Should score 40-60%")
    print("- Resume 3 (Mid-level): Should score 70-85%")
    print("- Scores should be different between batch and single modes")

if __name__ == "__main__":
    test_batch_scoring()
