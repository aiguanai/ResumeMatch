#!/usr/bin/env python3
"""
Test script for the Resume Matching API
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_list_resumes():
    """Test listing available resumes"""
    print("Testing /list-resumes endpoint...")
    response = requests.get(f"{BASE_URL}/list-resumes")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['total_files']} resume files:")
        for file in data['files']:
            print(f"  - {file}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    print()

def test_default_jd():
    """Test getting default job description"""
    print("Testing /default-job-description endpoint...")
    response = requests.get(f"{BASE_URL}/default-job-description")
    if response.status_code == 200:
        data = response.json()
        print("Default Job Description:")
        print(data['job_description'][:200] + "...")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    print()

def test_match_percentage():
    """Test match percentage analysis"""
    print("Testing /match-percentage endpoint...")
    
    sample_resume = """
    SENIOR SOFTWARE ENGINEER
    
    EXPERIENCE:
    - 5 years of experience in Java development
    - Strong knowledge of Spring framework
    - Experience with MySQL and database design
    - Worked on high-traffic web applications
    - Bachelor's degree in Computer Science
    
    SKILLS:
    - Java, Spring Boot, MySQL, JavaScript
    - RESTful APIs, Microservices
    - Git, Maven, Jenkins
    - Agile methodologies
    """
    
    payload = {
        "resume": sample_resume,
        "job_description": "Senior Software Engineer with Java experience required"
    }
    
    response = requests.post(f"{BASE_URL}/match-percentage", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("Match Analysis Results:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code} - {response.text}")
    print()

def test_skills_analysis():
    """Test skills analysis"""
    print("Testing /skills-analysis endpoint...")
    
    sample_resume = """
    SOFTWARE DEVELOPER
    
    EXPERIENCE:
    - 3 years of experience in web development
    - Proficient in JavaScript and React
    - Basic knowledge of Java
    - Experience with Node.js and MongoDB
    
    SKILLS:
    - JavaScript, React, Node.js
    - MongoDB, Express.js
    - HTML, CSS, Git
    """
    
    payload = {
        "resume": sample_resume
    }
    
    response = requests.post(f"{BASE_URL}/skills-analysis", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("Skills Analysis Results:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code} - {response.text}")
    print()

def test_analyze_specific_resume():
    """Test analyzing a specific resume file"""
    print("Testing /analyze-resume-file endpoint...")
    
    # Get list of available resumes first
    response = requests.get(f"{BASE_URL}/list-resumes")
    if response.status_code == 200:
        data = response.json()
        if data['files']:
            filename = data['files'][0]  # Use the first available resume
            print(f"Analyzing resume: {filename}")
            
            payload = {
                "filename": filename
            }
            
            response = requests.post(f"{BASE_URL}/analyze-resume-file", json=payload)
            if response.status_code == 200:
                data = response.json()
                print("Resume Analysis Results:")
                print(f"Filename: {data['filename']}")
                if 'match_analysis' in data and 'overall_match_percentage' in data['match_analysis']:
                    print(f"Overall Match: {data['match_analysis']['overall_match_percentage']}%")
                if 'skills_analysis' in data and 'matched_skills' in data['skills_analysis']:
                    print(f"Matched Skills: {data['skills_analysis']['matched_skills']}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        else:
            print("No resume files found")
    else:
        print(f"Error getting resume list: {response.status_code}")
    print()

def test_analyze_all_resumes():
    """Test analyzing all resumes (this might take a while)"""
    print("Testing /analyze-all-resumes endpoint...")
    print("This might take a while depending on the number of resumes...")
    
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/analyze-all-resumes")
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"Analysis completed in {end_time - start_time:.2f} seconds")
        print(f"Total resumes analyzed: {data['total_resumes']}")
        
        # Show summary of results
        for filename, result in data['results'].items():
            match_percentage = "N/A"
            if 'match_analysis' in result and 'overall_match_percentage' in result['match_analysis']:
                match_percentage = result['match_analysis']['overall_match_percentage']
            print(f"  {filename}: {match_percentage}% match")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    print()

def main():
    """Run all tests"""
    print("Resume Matching API Test Suite")
    print("=" * 50)
    
    try:
        # Test basic endpoints
        test_list_resumes()
        test_default_jd()
        
        # Test analysis endpoints
        test_match_percentage()
        test_skills_analysis()
        test_analyze_specific_resume()
        
        # Test batch analysis (uncomment if you want to test all resumes)
        # test_analyze_all_resumes()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    main()
