from flask import Flask, request, jsonify, render_template_string, send_file, session
from services.match_percentage import get_match_score
from services.skills_analysis import analyze_skills
from utils.resume_parser import get_all_resumes, extract_resume_text
import os
import json
import csv
import tempfile
from datetime import datetime
import zipfile
import shutil
from werkzeug.utils import secure_filename
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_folder(folder_path):
    """Check if folder contains allowed file types"""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not allowed_file(file):
                return False
    return True

@app.route("/", methods=["GET"])
def home():
    """Main application page with modern UI"""
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resume Matching System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .main-container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                margin: 20px auto;
                max-width: 1200px;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 20px 20px 0 0;
                text-align: center;
            }
            .form-section {
                padding: 30px;
                border-bottom: 1px solid #eee;
            }
            .form-section:last-child {
                border-bottom: none;
            }
            .section-title {
                color: #333;
                font-weight: 600;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .form-control, .form-select {
                border-radius: 10px;
                border: 2px solid #e9ecef;
                padding: 12px 15px;
                transition: all 0.3s ease;
            }
            .form-control:focus, .form-select:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 10px;
                padding: 12px 30px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                background: #f8f9ff;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .upload-area:hover {
                border-color: #764ba2;
                background: #f0f2ff;
            }
            .result-card {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                border-left: 5px solid #667eea;
            }
            .score-badge {
                background: linear-gradient(135deg, #d7e1ec 0%, #f3f4f6 100%);
                color: white;
                padding: 8px 20px;
                border-radius: 25px;
                font-weight: 700;
                font-size: 1.1rem;
                text-shadow: 0 1px 2px rgba(0,0,0,0.3);
                box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
                display: inline-block;
                min-width: 80px;
                text-align: center;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 40px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .download-buttons {
                margin-top: 20px;
                text-align: center;
            }
            .download-btn {
                margin: 5px;
                border-radius: 10px;
                padding: 10px 20px;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="main-container">
                <div class="header">
                    <h1><i class="fas fa-file-alt"></i> Resume Matching System</h1>
                    <p class="mb-0">AI-Powered Resume Analysis and Job Matching</p>
                </div>

                <form id="resumeForm" enctype="multipart/form-data">
                    <!-- API Key Section -->
                    <div class="form-section">
                        <h3 class="section-title">
                            <i class="fas fa-key"></i> OpenAI API Configuration
                        </h3>
                        <div class="row">
                            <div class="col-md-8">
                                <label for="apiKey" class="form-label">OpenAI API Key</label>
                                <input type="password" class="form-control" id="apiKey" name="apiKey" required>
                                <div class="form-text">Your API key will be used securely for analysis and won't be stored.</div>
                            </div>
                        </div>
                    </div>

                    <!-- Job Description Section -->
                    <div class="form-section">
                        <h3 class="section-title">
                            <i class="fas fa-briefcase"></i> Job Description
                        </h3>
                        <div class="row">
                            <div class="col-md-6">
                                <label for="jobTitle" class="form-label">Job Title</label>
                                <input type="text" class="form-control" id="jobTitle" name="jobTitle" placeholder="e.g., Senior Software Engineer" required>
                            </div>
                            <div class="col-md-6">
                                <label for="experience" class="form-label">Experience Required</label>
                                <input type="text" class="form-control" id="experience" name="experience" placeholder="e.g., 4-7 years">
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-6">
                                <label for="location" class="form-label">Location</label>
                                <input type="text" class="form-control" id="location" name="location" placeholder="e.g., Remote, New York">
                            </div>
                            <div class="col-md-6">
                                <label for="industry" class="form-label">Industry</label>
                                <input type="text" class="form-control" id="industry" name="industry" placeholder="e.g., Information Technology">
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-6">
                                <label for="mustHaveSkills" class="form-label">Must-Have Skills</label>
                                <textarea class="form-control" id="mustHaveSkills" name="mustHaveSkills" rows="3" placeholder="e.g., Java, Spring, MySQL"></textarea>
                            </div>
                            <div class="col-md-6">
                                <label for="niceToHaveSkills" class="form-label">Nice-to-Have Skills</label>
                                <textarea class="form-control" id="niceToHaveSkills" name="niceToHaveSkills" rows="3" placeholder="e.g., JavaScript, React, AWS"></textarea>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-12">
                                <label for="jobDescription" class="form-label">Detailed Job Description</label>
                                <textarea class="form-control" id="jobDescription" name="jobDescription" rows="6" placeholder="Enter the complete job description including roles, responsibilities, and requirements..." required></textarea>
                            </div>
                        </div>
                    </div>

                    <!-- Resume Upload Section -->
                    <div class="form-section">
                        <h3 class="section-title">
                            <i class="fas fa-upload"></i> Resume Upload
                        </h3>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="uploadType" id="singleFile" value="single" checked>
                                    <label class="form-check-label" for="singleFile">
                                        <i class="fas fa-file"></i> Single Resume
                                    </label>
                                </div>
                                <div id="singleUpload" class="mt-3">
                                    <div class="upload-area" onclick="document.getElementById('singleResume').click()">
                                        <i class="fas fa-cloud-upload-alt fa-3x text-primary mb-3"></i>
                                        <h5>Click to upload or drag & drop</h5>
                                        <p class="text-muted">Supports PDF, DOCX, DOC, TXT files</p>
                                        <input type="file" id="singleResume" name="singleResume" accept=".pdf,.docx,.doc,.txt" style="display: none;">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="uploadType" id="folderUpload" value="folder">
                                    <label class="form-check-label" for="folderUpload">
                                        <i class="fas fa-folder"></i> Folder of Resumes
                                    </label>
                                </div>
                                <div id="folderUploadArea" class="mt-3" style="display: none;">
                                    <div class="upload-area" onclick="document.getElementById('folderResumes').click()">
                                        <i class="fas fa-folder-open fa-3x text-primary mb-3"></i>
                                        <h5>Click to upload folder or drag & drop</h5>
                                        <p class="text-muted">Upload a ZIP file containing resumes</p>
                                        <input type="file" id="folderResumes" name="folderResumes" accept=".zip" style="display: none;">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Submit Button -->
                    <div class="form-section text-center">
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-search"></i> Analyze Resumes
                        </button>
                    </div>
                </form>

                <!-- Loading Section -->
                <div id="loading" class="loading">
                    <div class="spinner"></div>
                    <h4>Analyzing resumes...</h4>
                    <p>This may take a few minutes depending on the number of resumes.</p>
                </div>

                <!-- Results Section -->
                <div id="results" class="form-section" style="display: none;">
                    <h3 class="section-title">
                        <i class="fas fa-chart-bar"></i> Analysis Results
                    </h3>
                    <div id="resultsContent"></div>
                    <div id="downloadButtons" class="download-buttons" style="display: none;">
                        <button class="btn btn-success download-btn" onclick="downloadCSV()">
                            <i class="fas fa-download"></i> Download CSV
                        </button>
                        <button class="btn btn-danger download-btn" onclick="downloadPDF()">
                            <i class="fas fa-file-pdf"></i> Download PDF
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            let analysisResults = [];

            // Toggle upload type
            document.querySelectorAll('input[name="uploadType"]').forEach(radio => {
                radio.addEventListener('change', function() {
                    if (this.value === 'single') {
                        document.getElementById('singleUpload').style.display = 'block';
                        document.getElementById('folderUploadArea').style.display = 'none';
                    } else {
                        document.getElementById('singleUpload').style.display = 'none';
                        document.getElementById('folderUploadArea').style.display = 'block';
                    }
                });
            });

            // File upload handling
            document.getElementById('singleResume').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    document.querySelector('#singleUpload .upload-area h5').textContent = `Selected: ${file.name}`;
                }
            });

            document.getElementById('folderResumes').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    document.querySelector('#folderUploadArea .upload-area h5').textContent = `Selected: ${file.name}`;
                }
            });

            // Form submission
            document.getElementById('resumeForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const uploadType = formData.get('uploadType');
                
                // Validate file selection
                if (uploadType === 'single' && !formData.get('singleResume').name) {
                    alert('Please select a resume file.');
                    return;
                }
                if (uploadType === 'folder' && !formData.get('folderResumes').name) {
                    alert('Please select a folder/ZIP file.');
                    return;
                }

                // Show loading
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').style.display = 'none';
                
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        analysisResults = result.results;
                        displayResults(result.results);
                        document.getElementById('downloadButtons').style.display = 'block';
                    } else {
                        alert('Error: ' + result.error);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            });

            function displayResults(results) {
                const container = document.getElementById('resultsContent');
                container.innerHTML = '';

                // Sort results by overall match percentage
                const sortedResults = results.sort((a, b) => {
                    const scoreA = parseFloat(a.match_analysis.overall_match_percentage) || 0;
                    const scoreB = parseFloat(b.match_analysis.overall_match_percentage) || 0;
                    return scoreB - scoreA;
                });

                sortedResults.forEach((result, index) => {
                    const score = result.match_analysis.overall_match_percentage || 'N/A';
                    const scoreClass = score >= 80 ? 'text-success' : score >= 60 ? 'text-warning' : 'text-danger';
                    
                    const card = document.createElement('div');
                    card.className = 'result-card';
                    card.innerHTML = `
                        <div class="row">
                            <div class="col-md-8">
                                <h5><i class="fas fa-file-alt"></i> ${result.filename}</h5>
                                <div class="row mt-3">
                                    <div class="col-md-3">
                                        <strong>Overall Match:</strong><br>
                                        <span class="score-badge ${scoreClass}">${score}%</span>
                                    </div>
                                    <div class="col-md-3">
                                        <strong>Skills Match:</strong><br>
                                        <span class="text-primary">${result.match_analysis.skills_match_percentage || 'N/A'}%</span>
                                    </div>
                                    <div class="col-md-3">
                                        <strong>Experience Match:</strong><br>
                                        <span class="text-info">${result.match_analysis.experience_match_percentage || 'N/A'}%</span>
                                    </div>
                                    <div class="col-md-3">
                                        <strong>Education Match:</strong><br>
                                        <span class="text-secondary">${result.match_analysis.education_match_percentage || 'N/A'}%</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary btn-sm" onclick="toggleDetails(${index})">
                                    <i class="fas fa-eye"></i> View Details
                                </button>
                            </div>
                        </div>
                        <div id="details-${index}" class="mt-3" style="display: none;">
                            <hr>
                            <div class="row">
                                <div class="col-md-6">
                                    <h6><i class="fas fa-plus-circle"></i> Strengths</h6>
                                    <ul>
                                        ${(result.match_analysis.detailed_analysis?.strengths || []).map(s => `<li>${s}</li>`).join('')}
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h6><i class="fas fa-minus-circle"></i> Areas for Improvement</h6>
                                    <ul>
                                        ${(result.match_analysis.detailed_analysis?.weaknesses || []).map(w => `<li>${w}</li>`).join('')}
                                    </ul>
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-6">
                                    <h6><i class="fas fa-lightbulb"></i> Recommendations</h6>
                                    <ul>
                                        ${(result.match_analysis.detailed_analysis?.recommendations || []).map(r => `<li>${r}</li>`).join('')}
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h6><i class="fas fa-star"></i> Key Matches</h6>
                                    <ul>
                                        ${(result.match_analysis.key_matches || []).map(k => `<li>${k}</li>`).join('')}
                                    </ul>
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-6">
                                    <h6><i class="fas fa-check-circle"></i> Matched Skills</h6>
                                    <p><strong>Must-have:</strong> ${(result.skills_analysis.matched_skills?.must_have || []).join(', ') || 'None'}</p>
                                    <p><strong>Nice-to-have:</strong> ${(result.skills_analysis.matched_skills?.nice_to_have || []).join(', ') || 'None'}</p>
                                    <p><strong>Additional:</strong> ${(result.skills_analysis.matched_skills?.additional || []).join(', ') || 'None'}</p>
                                </div>
                                <div class="col-md-6">
                                    <h6><i class="fas fa-times-circle"></i> Missing Skills</h6>
                                    <p><strong>Critical:</strong> ${(result.skills_analysis.missing_skills?.critical || []).join(', ') || 'None'}</p>
                                    <p><strong>Important:</strong> ${(result.skills_analysis.missing_skills?.important || []).join(', ') || 'None'}</p>
                                    <p><strong>Optional:</strong> ${(result.skills_analysis.missing_skills?.optional || []).join(', ') || 'None'}</p>
                                </div>
                            </div>
                        </div>
                    `;
                    container.appendChild(card);
                });

                document.getElementById('results').style.display = 'block';
            }

            function toggleDetails(index) {
                const details = document.getElementById(`details-${index}`);
                const button = details.previousElementSibling.querySelector('button');
                
                if (details.style.display === 'none') {
                    details.style.display = 'block';
                    button.innerHTML = '<i class="fas fa-eye-slash"></i> Hide Details';
                } else {
                    details.style.display = 'none';
                    button.innerHTML = '<i class="fas fa-eye"></i> View Details';
                }
            }

            function downloadCSV() {
                const csvContent = generateCSV();
                const blob = new Blob([csvContent], { type: 'text/csv' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'resume_analysis_results.csv';
                a.click();
                window.URL.revokeObjectURL(url);
            }

            function generateCSV() {
                const headers = ['Filename', 'Overall Match %', 'Skills Match %', 'Experience Match %', 
                                'Education Match %', 'Matched Must-Have Skills', 'Matched Nice-to-Have Skills',
                                'Additional Skills', 'Missing Critical Skills', 'Missing Important Skills'];
                const rows = [headers];
                
                analysisResults.forEach(result => {
                    const row = [
                        result.filename,
                        result.match_analysis.overall_match_percentage || 'N/A',
                        result.match_analysis.skills_match_percentage || 'N/A',
                        result.match_analysis.experience_match_percentage || 'N/A',
                        result.match_analysis.education_match_percentage || 'N/A',
                        (result.skills_analysis.matched_skills?.must_have || []).join('; '),
                        (result.skills_analysis.matched_skills?.nice_to_have || []).join('; '),
                        (result.skills_analysis.matched_skills?.additional || []).join('; '),
                        (result.skills_analysis.missing_skills?.critical || []).join('; '),
                        (result.skills_analysis.missing_skills?.important || []).join('; ')
                    ];
                    rows.push(row);
                });
                
                return rows.map(row => row.map(cell => `"${cell}"`).join(',')).join('\\n');
            }

            function downloadPDF() {
                window.open('/download-pdf', '_blank');
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route("/analyze", methods=["POST"])
def analyze_resumes():
    """Analyze uploaded resumes against the job description"""
    try:
        # Get form data
        api_key = request.form.get('apiKey')
        job_title = request.form.get('jobTitle')
        experience = request.form.get('experience')
        location = request.form.get('location')
        industry = request.form.get('industry')
        must_have_skills = request.form.get('mustHaveSkills')
        nice_to_have_skills = request.form.get('niceToHaveSkills')
        job_description = request.form.get('jobDescription')
        upload_type = request.form.get('uploadType')

        # Validate required fields
        if not api_key or not job_description:
            return jsonify({"success": False, "error": "API key and job description are required"})

        # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = api_key

        # Construct complete job description
        complete_jd = f"""
{job_title}
Location: {location}
Experience Required: {experience}
Industry: {industry}

Key Skills:
Must-Have: {must_have_skills}
Nice-to-Have: {nice_to_have_skills}

Job Description:
{job_description}
        """.strip()

        resumes = {}
        
        if upload_type == 'single':
            # Handle single file upload
            if 'singleResume' not in request.files:
                return jsonify({"success": False, "error": "No file uploaded"})
            
            file = request.files['singleResume']
            if file.filename == '':
                return jsonify({"success": False, "error": "No file selected"})
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extract text from the uploaded file
                resume_text = extract_resume_text(filepath)
                if resume_text and not resume_text.startswith("Error"):
                    resumes[filename] = resume_text
                else:
                    return jsonify({"success": False, "error": f"Could not extract text from {filename}"})
            else:
                return jsonify({"success": False, "error": "Invalid file type"})

        elif upload_type == 'folder':
            # Handle folder/ZIP upload
            if 'folderResumes' not in request.files:
                return jsonify({"success": False, "error": "No ZIP file uploaded"})
            
            zip_file = request.files['folderResumes']
            if zip_file.filename == '':
                return jsonify({"success": False, "error": "No ZIP file selected"})
            
            if zip_file and zip_file.filename.endswith('.zip'):
                # Create temporary directory for extraction
                temp_dir = tempfile.mkdtemp()
                zip_path = os.path.join(temp_dir, 'resumes.zip')
                zip_file.save(zip_path)
                
                try:
                    # Extract ZIP file
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    # Process extracted files
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            if allowed_file(file):
                                file_path = os.path.join(root, file)
                                resume_text = extract_resume_text(file_path)
                                if resume_text and not resume_text.startswith("Error"):
                                    resumes[file] = resume_text
                finally:
                    # Improved cleanup with retry mechanism
                    try:
                        # Remove the ZIP file first
                        if os.path.exists(zip_path):
                            os.remove(zip_path)
                        
                        # Wait a moment for file handles to be released
                        import time
                        time.sleep(0.1)
                        
                        # Remove the temporary directory
                        if os.path.exists(temp_dir):
                            import shutil
                            shutil.rmtree(temp_dir, ignore_errors=True)
                    except Exception as cleanup_error:
                        print(f"Cleanup warning: {cleanup_error}")
                        # Try alternative cleanup method
                        try:
                            import shutil
                            shutil.rmtree(temp_dir, ignore_errors=True)
                        except:
                            pass
            else:
                return jsonify({"success": False, "error": "Invalid ZIP file"})

        if not resumes:
            return jsonify({"success": False, "error": "No valid resumes found"})

        # Analyze each resume
        results = []
        is_batch = len(resumes) > 1  # Check if this is a batch analysis
        
        print(f"Analysis Mode: {'BATCH' if is_batch else 'SINGLE'} - Processing {len(resumes)} resumes")
        
        for filename, resume_text in resumes.items():
            try:
                print(f"Analyzing: {filename} (Batch mode: {is_batch})")
                
                # Get match percentage with batch analysis flag
                match_result = get_match_score(resume_text, complete_jd, is_batch_analysis=is_batch)
                
                # Debug: Print the score for verification
                overall_score = match_result.get('overall_match_percentage', 'N/A')
                print(f"  {filename} Score: {overall_score}%")
                
                # Get skills analysis
                skills_result = analyze_skills(resume_text, complete_jd)
                
                results.append({
                    "filename": filename,
                    "match_analysis": match_result,
                    "skills_analysis": skills_result
                })
            except Exception as e:
                print(f"Error analyzing {filename}: {str(e)}")
                results.append({
                    "filename": filename,
                    "error": str(e),
                    "match_analysis": {"overall_match_percentage": "Error"},
                    "skills_analysis": {"matched_skills": {}, "missing_skills": {}}
                })

        # Store results in session for PDF generation
        session['analysis_results'] = results
        session['job_description'] = complete_jd
        
        print(f"Analysis Complete: Stored {len(results)} results in session")
        print(f"Resume filenames: {[r.get('filename', 'Unknown') for r in results]}")
        
        return jsonify({
            "success": True,
            "results": results,
            "total_resumes": len(results)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/download-csv")
def download_csv():
    """Download analysis results as CSV"""
    try:
        results = session.get('analysis_results', [])
        if not results:
            return jsonify({"error": "No results available"}), 404

        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            'Filename', 'Overall Match %', 'Skills Match %', 'Experience Match %', 
            'Education Match %', 'Matched Must-Have Skills', 'Matched Nice-to-Have Skills',
            'Additional Skills', 'Missing Critical Skills', 'Missing Important Skills', 
            'Missing Optional Skills', 'Strengths', 'Weaknesses', 'Recommendations',
            'Key Matches', 'Missing Requirements'
        ])
        
        # Write data
        for result in results:
            writer.writerow([
                result.get('filename', ''),
                result.get('match_analysis', {}).get('overall_match_percentage', 'N/A'),
                result.get('match_analysis', {}).get('skills_match_percentage', 'N/A'),
                result.get('match_analysis', {}).get('experience_match_percentage', 'N/A'),
                result.get('match_analysis', {}).get('education_match_percentage', 'N/A'),
                '; '.join(result.get('skills_analysis', {}).get('matched_skills', {}).get('must_have', [])),
                '; '.join(result.get('skills_analysis', {}).get('matched_skills', {}).get('nice_to_have', [])),
                '; '.join(result.get('skills_analysis', {}).get('matched_skills', {}).get('additional', [])),
                '; '.join(result.get('skills_analysis', {}).get('missing_skills', {}).get('critical', [])),
                '; '.join(result.get('skills_analysis', {}).get('missing_skills', {}).get('important', [])),
                '; '.join(result.get('skills_analysis', {}).get('missing_skills', {}).get('optional', [])),
                '; '.join(result.get('match_analysis', {}).get('detailed_analysis', {}).get('strengths', [])),
                '; '.join(result.get('match_analysis', {}).get('detailed_analysis', {}).get('weaknesses', [])),
                '; '.join(result.get('match_analysis', {}).get('detailed_analysis', {}).get('recommendations', [])),
                '; '.join(result.get('match_analysis', {}).get('key_matches', [])),
                '; '.join(result.get('match_analysis', {}).get('missing_requirements', []))
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'resume_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download-pdf")
def download_pdf():
    """Download analysis results as PDF"""
    try:
        results = session.get('analysis_results', [])
        job_description = session.get('job_description', '')
        
        print(f"PDF Generation Debug: Found {len(results)} results in session")
        print(f"Results: {[r.get('filename', 'Unknown') for r in results]}")
        
        if not results:
            return jsonify({"error": "No results available"}), 404

        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20
        )
        
        # Title
        story.append(Paragraph("Resume Analysis Report", title_style))
        story.append(Spacer(1, 20))
        
        # Job Description
        if job_description:
            story.append(Paragraph("Job Description", heading_style))
            story.append(Paragraph(job_description.replace('\n', '<br/>'), styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Results Summary
        story.append(Paragraph(f"Analysis Results ({len(results)} resumes)", heading_style))
        story.append(Spacer(1, 10))
        
        # Sort results by overall match percentage (handle errors gracefully)
        def safe_sort_key(result):
            try:
                score = result.get('match_analysis', {}).get('overall_match_percentage', '0')
                if isinstance(score, str) and score.replace('.', '').replace('%', '').isdigit():
                    return float(score.replace('%', ''))
                return 0.0
            except (ValueError, TypeError):
                return 0.0
        
        sorted_results = sorted(results, key=safe_sort_key, reverse=True)
        
        print(f"PDF Generation Debug: Processing {len(sorted_results)} sorted results")
        
        for i, result in enumerate(sorted_results, 1):
            filename = result.get('filename', 'Unknown')
            match_analysis = result.get('match_analysis', {})
            skills_analysis = result.get('skills_analysis', {})
            
            print(f"PDF Generation Debug: Processing resume {i}: {filename}")
            
            # Resume header
            story.append(Paragraph(f"{i}. {filename}", heading_style))
            
            # Match percentages
            match_data = [
                ['Metric', 'Score'],
                ['Overall Match', f"{match_analysis.get('overall_match_percentage', 'N/A')}%"],
                ['Skills Match', f"{match_analysis.get('skills_match_percentage', 'N/A')}%"],
                ['Experience Match', f"{match_analysis.get('experience_match_percentage', 'N/A')}%"],
                ['Education Match', f"{match_analysis.get('education_match_percentage', 'N/A')}%"]
            ]
            
            match_table = Table(match_data, colWidths=[2*inch, 1*inch])
            match_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(match_table)
            story.append(Spacer(1, 12))
            
            # Detailed Analysis Section
            detailed_analysis = match_analysis.get('detailed_analysis', {})
            if detailed_analysis:
                # Strengths
                strengths = detailed_analysis.get('strengths', [])
                if strengths:
                    story.append(Paragraph("<b>Strengths:</b>", styles['Normal']))
                    for strength in strengths:
                        story.append(Paragraph(f"• {strength}", styles['Normal']))
                    story.append(Spacer(1, 8))
                
                # Weaknesses
                weaknesses = detailed_analysis.get('weaknesses', [])
                if weaknesses:
                    story.append(Paragraph("<b>Areas for Improvement:</b>", styles['Normal']))
                    for weakness in weaknesses:
                        story.append(Paragraph(f"• {weakness}", styles['Normal']))
                    story.append(Spacer(1, 8))
                
                # Recommendations
                recommendations = detailed_analysis.get('recommendations', [])
                if recommendations:
                    story.append(Paragraph("<b>Recommendations:</b>", styles['Normal']))
                    for rec in recommendations:
                        story.append(Paragraph(f"• {rec}", styles['Normal']))
                    story.append(Spacer(1, 8))
            
            # Key Matches and Missing Requirements
            key_matches = match_analysis.get('key_matches', [])
            if key_matches:
                story.append(Paragraph("<b>Key Matches:</b>", styles['Normal']))
                for match in key_matches:
                    story.append(Paragraph(f"• {match}", styles['Normal']))
                story.append(Spacer(1, 8))
            
            missing_requirements = match_analysis.get('missing_requirements', [])
            if missing_requirements:
                story.append(Paragraph("<b>Missing Requirements:</b>", styles['Normal']))
                for req in missing_requirements:
                    story.append(Paragraph(f"• {req}", styles['Normal']))
                story.append(Spacer(1, 8))
            
            # Skills analysis
            matched_skills = skills_analysis.get('matched_skills', {})
            missing_skills = skills_analysis.get('missing_skills', {})
            
            # Add skills analysis as normal text instead of table
            story.append(Paragraph("<b>Skills Analysis:</b>", styles['Normal']))
            story.append(Spacer(1, 8))
            
            # Matched Skills
            must_have_skills = matched_skills.get('must_have', [])
            nice_to_have_skills = matched_skills.get('nice_to_have', [])
            additional_skills = matched_skills.get('additional', [])
            
            if must_have_skills:
                story.append(Paragraph(f"<b>Matched Must-Have Skills:</b> {', '.join(must_have_skills)}", styles['Normal']))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("<b>Matched Must-Have Skills:</b> None", styles['Normal']))
                story.append(Spacer(1, 6))
            
            if nice_to_have_skills:
                story.append(Paragraph(f"<b>Matched Nice-to-Have Skills:</b> {', '.join(nice_to_have_skills)}", styles['Normal']))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("<b>Matched Nice-to-Have Skills:</b> None", styles['Normal']))
                story.append(Spacer(1, 6))
            
            if additional_skills:
                story.append(Paragraph(f"<b>Additional Skills:</b> {', '.join(additional_skills)}", styles['Normal']))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("<b>Additional Skills:</b> None", styles['Normal']))
                story.append(Spacer(1, 6))
            
            # Missing Skills
            critical_skills = missing_skills.get('critical', [])
            important_skills = missing_skills.get('important', [])
            optional_skills = missing_skills.get('optional', [])
            
            if critical_skills:
                story.append(Paragraph(f"<b>Missing Critical Skills:</b> {', '.join(critical_skills)}", styles['Normal']))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("<b>Missing Critical Skills:</b> None", styles['Normal']))
                story.append(Spacer(1, 6))
            
            if important_skills:
                story.append(Paragraph(f"<b>Missing Important Skills:</b> {', '.join(important_skills)}", styles['Normal']))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("<b>Missing Important Skills:</b> None", styles['Normal']))
                story.append(Spacer(1, 6))
            
            if optional_skills:
                story.append(Paragraph(f"<b>Missing Optional Skills:</b> {', '.join(optional_skills)}", styles['Normal']))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("<b>Missing Optional Skills:</b> None", styles['Normal']))
                story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 20))
        
        print(f"PDF Generation Debug: Built PDF with {len(story)} elements")
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'resume_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Resume Matching System",
        "version": "2.0.0"
    })

@app.route("/debug-session", methods=["GET"])
def debug_session():
    """Debug endpoint to check session data"""
    try:
        results = session.get('analysis_results', [])
        job_description = session.get('job_description', '')
        
        debug_info = {
            "session_keys": list(session.keys()),
            "analysis_results_count": len(results),
            "job_description_length": len(job_description) if job_description else 0,
            "resume_filenames": [r.get('filename', 'Unknown') for r in results],
            "results_summary": []
        }
        
        for i, result in enumerate(results):
            debug_info["results_summary"].append({
                "index": i,
                "filename": result.get('filename', 'Unknown'),
                "has_match_analysis": 'match_analysis' in result,
                "has_skills_analysis": 'skills_analysis' in result,
                "overall_match": result.get('match_analysis', {}).get('overall_match_percentage', 'N/A')
            })
        
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
