from flask import Flask, request, jsonify, render_template_string
from services.match_percentage import get_match_score
from services.skills_analysis import analyze_skills
from utils.resume_parser import get_all_resumes, extract_resume_text
import os
import json

app = Flask(__name__)

# Default Job Description for Senior Software Engineer
DEFAULT_JD = """
Senior Software Engineer
Locations: Remote

Experience Required: 4 - 7 years

Key Skills:
Must-Have: Java
Nice-to-Have: Javascript

Industry: Information Technology

Job Summary:
We are seeking a passionate and skilled Senior Software Engineer to join our dynamic team. The ideal candidate will have a strong background in Java and a keen interest in optimizing high-volume transactional enterprise websites. This role offers the opportunity to work on multiple projects, enhancing our technology platform and reinventing the online shopping experience.

Required Qualification:
Bachelor's or Master's Degree in Computer Science

Roles & Responsibilities:
Work independently and collaboratively to optimize high-volume transactional enterprise websites.
Demonstrate a deep understanding of software layers and enhance processes within the technology platform, including Linux, Tomcat, MySQL, Java, Spring, JavaScript, Object-Relational Mapping, and Direct SQL.
Develop internal software to automate and integrate business processes.
Manage multiple projects and transition seamlessly between them.
Exhibit a passion for building scalable systems capable of processing 30 million requests per day.
Engage in quick iterative development cycles while understanding business requirements.
"""

@app.route("/", methods=["GET"])
def home():
    """Home page with API documentation"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resume Matching API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
            .method { color: #007bff; font-weight: bold; }
            .url { color: #28a745; font-family: monospace; }
            .description { margin: 10px 0; }
            .example { background: #e9ecef; padding: 10px; border-radius: 3px; font-family: monospace; }
        </style>
    </head>
    <body>
        <h1>Resume Matching API</h1>
        <p>This API provides comprehensive resume matching and skills analysis using ChatGPT.</p>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/match-percentage</span></h3>
            <div class="description">Get detailed match percentage analysis for a resume against a job description.</div>
            <div class="example">
                Request Body: {"resume": "resume text", "job_description": "job description text"}
            </div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/skills-analysis</span></h3>
            <div class="description">Analyze skills match and gaps between resume and job description.</div>
            <div class="example">
                Request Body: {"resume": "resume text", "job_description": "job description text"}
            </div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/analyze-all-resumes</span></h3>
            <div class="description">Analyze all resumes in the resumes/ directory against the default job description.</div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/analyze-resume-file</span></h3>
            <div class="description">Analyze a specific resume file from the resumes/ directory.</div>
            <div class="example">
                Request Body: {"filename": "resume.pdf", "job_description": "optional custom job description"}
            </div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/list-resumes</span></h3>
            <div class="description">List all available resume files in the resumes/ directory.</div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/comprehensive-analysis</span></h3>
            <div class="description">Get comprehensive analysis including both match percentage and skills analysis in a single request.</div>
            <div class="example">
                Request Body: {"resume": "resume text", "job_description": "optional custom job description"}
            </div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/default-job-description</span></h3>
            <div class="description">Get the default job description for Senior Software Engineer position.</div>
        </div>
        
        <div class="endpoint">
            <h3><span class="method">GET</span> <span class="url">/health</span></h3>
            <div class="description">Health check endpoint for server monitoring.</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route("/match-percentage", methods=["POST"])
def match_percentage():
    """Get detailed match percentage analysis"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        resume = data.get("resume")
        jd = data.get("job_description", DEFAULT_JD)
        
        if not resume:
            return jsonify({"error": "Resume text is required"}), 400
        
        result = get_match_score(resume, jd)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/skills-analysis", methods=["POST"])
def skills_analysis():
    """Analyze skills match and gaps"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        resume = data.get("resume")
        jd = data.get("job_description", DEFAULT_JD)
        
        if not resume:
            return jsonify({"error": "Resume text is required"}), 400
        
        result = analyze_skills(resume, jd)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze-all-resumes", methods=["GET"])
def analyze_all_resumes():
    """Analyze all resumes against the default job description"""
    try:
        resumes = get_all_resumes()
        if not resumes:
            return jsonify({"error": "No resumes found in resumes/ directory"}), 404
        
        results = {}
        for filename, resume_text in resumes.items():
            # Get match percentage
            match_result = get_match_score(resume_text, DEFAULT_JD)
            # Get skills analysis
            skills_result = analyze_skills(resume_text, DEFAULT_JD)
            
            results[filename] = {
                "match_analysis": match_result,
                "skills_analysis": skills_result
            }
        
        return jsonify({
            "job_description": DEFAULT_JD,
            "total_resumes": len(resumes),
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze-resume-file", methods=["POST"])
def analyze_resume_file():
    """Analyze a specific resume file"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        filename = data.get("filename")
        custom_jd = data.get("job_description", DEFAULT_JD)
        
        if not filename:
            return jsonify({"error": "Filename is required"}), 400
        
        file_path = os.path.join("resumes", filename)
        if not os.path.exists(file_path):
            return jsonify({"error": f"File {filename} not found"}), 404
        
        resume_text = extract_resume_text(file_path)
        if not resume_text or resume_text.startswith("Error"):
            return jsonify({"error": f"Could not extract text from {filename}"}), 400
        
        # Get match percentage
        match_result = get_match_score(resume_text, custom_jd)
        # Get skills analysis
        skills_result = analyze_skills(resume_text, custom_jd)
        
        return jsonify({
            "filename": filename,
            "job_description": custom_jd,
            "match_analysis": match_result,
            "skills_analysis": skills_result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list-resumes", methods=["GET"])
def list_resumes():
    """List all available resume files"""
    try:
        resumes = get_all_resumes()
        return jsonify({
            "total_files": len(resumes),
            "files": list(resumes.keys())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/default-job-description", methods=["GET"])
def get_default_jd():
    """Get the default job description"""
    return jsonify({
        "job_description": DEFAULT_JD
    })

@app.route("/comprehensive-analysis", methods=["POST"])
def comprehensive_analysis():
    """Get comprehensive analysis including match percentage and skills analysis"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        resume = data.get("resume")
        jd = data.get("job_description", DEFAULT_JD)
        
        if not resume:
            return jsonify({"error": "Resume text is required"}), 400
        
        # Get both match percentage and skills analysis
        match_result = get_match_score(resume, jd)
        skills_result = analyze_skills(resume, jd)
        
        return jsonify({
            "job_description": jd,
            "match_percentage_analysis": match_result,
            "skills_analysis": skills_result,
            "summary": {
                "overall_match": match_result.get("overall_match_percentage", "N/A"),
                "technical_skills_match": skills_result.get("skill_analysis", {}).get("technical_skills_match", "N/A"),
                "matched_must_have_skills": len(skills_result.get("matched_skills", {}).get("must_have", [])),
                "missing_critical_skills": len(skills_result.get("missing_skills", {}).get("critical", []))
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for server monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "Resume Matching API",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
