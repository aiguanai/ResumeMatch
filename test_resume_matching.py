#!/usr/bin/env python3
"""
Test script for Resume Matching API
This script demonstrates how to use the API endpoints for resume matching and skills analysis.
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_default_job_description():
    """Test getting the default job description"""
    print("=== Testing Default Job Description ===")
    response = requests.get(f"{BASE_URL}/default-job-description")
    print(f"Status Code: {response.status_code}")
    jd = response.json()["job_description"]
    print(f"Job Description Length: {len(jd)} characters")
    print(f"First 200 characters: {jd[:200]}...")
    print()

def test_list_resumes():
    """Test listing available resumes"""
    print("=== Testing List Resumes ===")
    response = requests.get(f"{BASE_URL}/list-resumes")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total files: {data['total_files']}")
    print(f"Files: {data['files']}")
    print()

def test_match_percentage():
    """Test match percentage analysis"""
    print("=== Testing Match Percentage ===")
    
    # Sample resume text
    sample_resume = """
    SENIOR SOFTWARE ENGINEER
    
    EXPERIENCE:
    - 5 years of experience in Java development
    - Worked on high-volume transactional systems
    - Experience with Spring Framework, MySQL, and Linux
    - Led development of systems processing 20M+ requests daily
    
    SKILLS:
    - Java, Spring Framework, MySQL, Linux, Tomcat
    - JavaScript, Object-Relational Mapping
    - Microservices architecture
    - Performance optimization
    
    EDUCATION:
    - Bachelor's Degree in Computer Science
    """
    
    payload = {
        "resume": sample_resume,
        "job_description": "Senior Software Engineer with Java experience"
    }
    
    response = requests.post(f"{BASE_URL}/match-percentage", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Overall Match: {result.get('overall_match_percentage', 'N/A')}%")
    print(f"Skills Match: {result.get('skills_match_percentage', 'N/A')}%")
    print(f"Experience Match: {result.get('experience_match_percentage', 'N/A')}%")
    print()

def test_skills_analysis():
    """Test skills analysis"""
    print("=== Testing Skills Analysis ===")
    
    # Sample resume text
    sample_resume = """
    SENIOR SOFTWARE ENGINEER
    
    EXPERIENCE:
    - 5 years of experience in Java development
    - Worked on high-volume transactional systems
    - Experience with Spring Framework, MySQL, and Linux
    - Led development of systems processing 20M+ requests daily
    
    SKILLS:
    - Java, Spring Framework, MySQL, Linux, Tomcat
    - JavaScript, Object-Relational Mapping
    - Microservices architecture
    - Performance optimization
    
    EDUCATION:
    - Bachelor's Degree in Computer Science
    """
    
    payload = {
        "resume": sample_resume,
        "job_description": "Senior Software Engineer with Java experience"
    }
    
    response = requests.post(f"{BASE_URL}/skills-analysis", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    
    print("Matched Skills:")
    print(f"  Must-have: {result.get('matched_skills', {}).get('must_have', [])}")
    print(f"  Nice-to-have: {result.get('matched_skills', {}).get('nice_to_have', [])}")
    
    print("Missing Skills:")
    print(f"  Critical: {result.get('missing_skills', {}).get('critical', [])}")
    print(f"  Important: {result.get('missing_skills', {}).get('important', [])}")
    print()

def test_comprehensive_analysis():
    """Test comprehensive analysis"""
    print("=== Testing Comprehensive Analysis ===")
    
    # Sample resume text
    sample_resume = """
    SENIOR SOFTWARE ENGINEER
    
    EXPERIENCE:
    - 5 years of experience in Java development
    - Worked on high-volume transactional systems
    - Experience with Spring Framework, MySQL, and Linux
    - Led development of systems processing 20M+ requests daily
    
    SKILLS:
    - Java, Spring Framework, MySQL, Linux, Tomcat
    - JavaScript, Object-Relational Mapping
    - Microservices architecture
    - Performance optimization
    
    EDUCATION:
    - Bachelor's Degree in Computer Science
    """
    
    payload = {
        "resume": sample_resume
    }
    
    response = requests.post(f"{BASE_URL}/comprehensive-analysis", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    
    summary = result.get('summary', {})
    print(f"Overall Match: {summary.get('overall_match', 'N/A')}%")
    print(f"Technical Skills Match: {summary.get('technical_skills_match', 'N/A')}%")
    print(f"Matched Must-Have Skills: {summary.get('matched_must_have_skills', 0)}")
    print(f"Missing Critical Skills: {summary.get('missing_critical_skills', 0)}")
    print()

def test_analyze_all_resumes():
    """Test analyzing all resumes"""
    print("=== Testing Analyze All Resumes ===")
    response = requests.get(f"{BASE_URL}/analyze-all-resumes")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total resumes analyzed: {result['total_resumes']}")
        for filename, analysis in result['results'].items():
            match_percentage = analysis['match_analysis'].get('overall_match_percentage', 'N/A')
            print(f"  {filename}: {match_percentage}% match")
    else:
        print(f"Error: {response.json()}")
    print()

if __name__ == "__main__":
    print("Resume Matching API Test Script")
    print("=" * 50)
    
    try:
        # Run all tests
        test_health_check()
        test_default_job_description()
        test_list_resumes()
        test_match_percentage()
        test_skills_analysis()
        test_comprehensive_analysis()
        test_analyze_all_resumes()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Flask app is running on http://localhost:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"Error during testing: {str(e)}")
