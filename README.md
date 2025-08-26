# Resume Matching System

An AI-powered resume analysis and job matching system built with Flask and OpenAI GPT-4. This application provides both a modern web interface and comprehensive API endpoints for analyzing resumes against job descriptions and generating detailed matching reports.

## 📋 **Table of Contents**

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#features)
- [🛠️ Installation & Setup](#️-installation--setup)
- [🌐 Web Interface Usage](#-web-interface-usage)
- [📡 API Endpoints & Postman Usage](#-api-endpoints--postman-usage)
- [🐳 Docker Deployment](#-docker-deployment)
- [📁 File Structure](#-file-structure)
- [📋 Technical Specifications](#-technical-specifications)
- [🚨 Troubleshooting & Common Issues](#-troubleshooting--common-issues)
- [🧪 Testing & Development](#-testing--development)
- [🚀 Quick Start Examples](#-quick-start-examples)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🆘 Support & Help](#-support--help)
- [⚠️ Important Notes](#️-important-notes)
- [🎯 Ready to Get Started?](#-ready-to-get-started)

## 🚀 **Quick Start**

Choose your preferred method:

- **🌐 Web Interface**: Modern UI for easy resume analysis
- **📡 API Endpoints**: Use with Postman, curl, or any HTTP client
- **🐳 Docker**: Containerized deployment (recommended for production)
- **📱 Batch Processing**: Analyze multiple resumes at once

### **🚀 Get Started in 5 Minutes**

```bash
# Option 1: Local Development
git clone <repository-url>
cd Resume_Match
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py

# Option 2: Docker (Fastest)
docker-compose up -d

# Option 3: Windows Script
start_server.bat
```

**🎯 Next Steps:**
1. **Start the server** using one of the options above
2. **Open your browser** and go to `http://localhost:5000`
3. **Enter your OpenAI API key** and job description
4. **Upload resumes** and start analyzing!

## ✨ **Features**

### 🎯 Core Functionality
- **OpenAI API Integration**: Secure API key input for AI-powered analysis
- **Custom Job Descriptions**: Structured input for job details including:
  - Job Title
  - Experience Requirements
  - Location
  - Industry
  - Must-Have Skills
  - Nice-to-Have Skills
  - Detailed Job Description

### 📁 Resume Upload Options
- **Single Resume Upload**: Upload individual resume files (PDF, DOCX, DOC, TXT)
- **Batch Processing**: Upload ZIP files containing multiple resumes for bulk analysis

### 📊 Analysis & Results
- **Comprehensive Matching**: Overall, Skills, Experience, and Education match percentages
- **Detailed Skills Analysis**: Matched and missing skills categorization with priority levels
- **Strengths & Weaknesses**: Detailed analysis of candidate strengths and areas for improvement
- **Ranked Results**: Results sorted by overall match percentage (highest to lowest)
- **Batch Analysis**: Intelligent scoring that prevents identical scores for different candidates
- **Skills Gap Analysis**: Critical, important, and optional missing skills identification

### 📥 Export Options
- **CSV Download**: Export results as a structured CSV file
- **PDF Report**: Generate professional PDF reports with detailed analysis

## 🛠️ **Installation & Setup**

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Git (for cloning)

### Setup Options

#### **Option 1: Local Development**
1. Clone the repository:
```bash
git clone <repository-url>
cd Resume_Match
```

2. Create virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create the uploads directory:
```bash
mkdir uploads
```

#### **Option 2: Docker (Recommended for Production)**
```bash
# Using Docker Compose
docker-compose up -d

# Or manual Docker build
docker build -t resume-matcher .
docker run -p 5000:5000 resume-matcher
```

#### **Option 3: Windows Batch Script**
```bash
# Run the provided batch script
start_server.bat
```

## 🌐 **Web Interface Usage**

### Starting the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Using the Web Interface

1. **OpenAI API Configuration**
   - Enter your OpenAI API key in the secure input field
   - The API key is used only for analysis and is not stored

2. **Job Description Setup**
   - Fill in the job title, experience requirements, location, and industry
   - Specify must-have and nice-to-have skills
   - Provide a detailed job description with roles and responsibilities

3. **Resume Upload**
   - Choose between single resume or folder upload
   - For single upload: Select a PDF, DOCX, DOC, or TXT file
   - For batch upload: Create a ZIP file containing multiple resumes

4. **Analysis**
   - Click "Analyze Resumes" to start the AI-powered analysis
   - The system will process each resume and provide detailed matching scores

5. **Results Review**
   - View ranked results with overall match percentages
   - Expand individual results to see detailed analysis
   - Review strengths, weaknesses, and skill matches

6. **Export Results**
   - Download results as CSV for spreadsheet analysis
   - Generate PDF reports for professional presentations

## 📡 **API Endpoints & Postman Usage**

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main application interface |
| `POST` | `/analyze` | Analyze uploaded resumes |
| `GET` | `/download-csv` | Download results as CSV |
| `GET` | `/download-pdf` | Download results as PDF |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/debug-session` | Debug session data |

### 🚀 **Postman Setup Guide**

#### **Step 1: Create a New Request**
1. Open Postman
2. Click "New" → "Request"
3. Name it "Resume Analysis"

#### **Step 2: Configure the Request**
- **Method**: POST
- **URL**: `http://localhost:5000/analyze`

#### **Step 3: Set Headers**
- Go to "Headers" tab
- Add: `Content-Type: multipart/form-data`

#### **Step 4: Set Body**
- Go to "Body" tab
- Select "form-data"
- Add your fields:

| Key | Type | Value |
|-----|------|-------|
| `apiKey` | Text | Your OpenAI API key |
| `jobTitle` | Text | Senior Software Engineer |
| `experience` | Text | 4-7 years |
| `location` | Text | Remote |
| `industry` | Text | Information Technology |
| `mustHaveSkills` | Text | Java, Spring, MySQL |
| `niceToHaveSkills` | Text | JavaScript, React |
| `jobDescription` | Text | Your detailed job description |
| `uploadType` | Text | `single` or `folder` |
| `singleResume` | File | Select your resume file |
| `folderResumes` | File | Select ZIP file (for batch) |

#### **Step 5: Send Request**
Click "Send" and you'll get a JSON response with the analysis results!

### 📋 **Example Postman Request**

**URL:** `http://localhost:5000/analyze`

**Method:** POST

**Headers:**
```
Content-Type: multipart/form-data
```

**Body (form-data):**
```
apiKey: sk-your-openai-api-key-here
jobTitle: Senior Software Engineer
experience: 4-7 years
location: Remote
industry: Information Technology
mustHaveSkills: Java, Spring, MySQL
niceToHaveSkills: JavaScript, React
jobDescription: We are seeking a Senior Software Engineer with strong Java experience...
uploadType: single
singleResume: [Select your PDF/DOCX file]
```

### 🔧 **Quick Test Commands (curl)**

```bash
# Health check
curl http://localhost:5000/health

# Download CSV
curl http://localhost:5000/download-csv

# Download PDF
curl http://localhost:5000/download-pdf
```

### 📊 **API Response Format**

```json
{
  "success": true,
  "results": [
    {
      "filename": "resume.pdf",
      "match_analysis": {
        "overall_match_percentage": 85,
        "skills_match_percentage": 80,
        "experience_match_percentage": 90,
        "education_match_percentage": 100,
        "detailed_analysis": {
          "strengths": ["Strong Java experience", "Good leadership skills"],
          "weaknesses": ["Limited cloud experience"],
          "recommendations": ["Consider AWS certification"]
        },
        "key_matches": ["Java expertise", "Team leadership"],
        "missing_requirements": ["Cloud platform experience"]
      },
      "skills_analysis": {
        "matched_skills": {
          "must_have": ["Java"],
          "nice_to_have": ["JavaScript"],
          "additional": ["Spring", "MySQL"]
        },
        "missing_skills": {
          "critical": [],
          "important": ["AWS", "Docker"],
          "optional": ["Kubernetes"]
        }
      }
    }
  ],
  "total_resumes": 1
}
```

## 🐳 **Docker Deployment**

### Using Docker Compose
```bash
docker-compose up -d
```

### Manual Docker Build
```bash
docker build -t resume-matcher .
docker run -p 5000:5000 resume-matcher
```

## 📁 **File Structure**

```
Resume_Match/
├── app.py                    # Main Flask application with web UI
├── requirements.txt          # Python dependencies
├── README.md                # This documentation file
├── uploads/                 # Upload directory for resumes
├── services/
│   ├── llm_utils.py         # OpenAI API integration utilities
│   ├── match_percentage.py  # Intelligent match scoring with batch analysis
│   └── skills_analysis.py   # Skills analysis and gap identification
├── utils/
│   ├── jd_parser.py         # Job description parsing utilities
│   └── resume_parser.py     # Resume text extraction (PDF, DOCX, DOC, TXT)
├── test_resume_matching.py  # Comprehensive API testing script
├── test_batch_scoring.py    # Batch scoring verification script
├── deploy.py                # Local deployment helper
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Multi-container deployment
└── start_server.bat         # Windows server startup script
```

## 📋 **Technical Specifications**

### **Supported File Formats**
- **Resume Files**: PDF (.pdf), Microsoft Word (.docx, .doc), Plain Text (.txt)
- **Batch Upload**: ZIP files containing supported resume formats
- **File Size Limit**: Maximum 50MB per upload

### **Security Features**
- **Secure API Key Handling**: API keys are not stored and are used only for analysis
- **File Validation**: Strict file type validation for uploads
- **Session Management**: Secure session handling for temporary data storage

### **Performance Considerations**
- **Processing Time**: Analysis time depends on the number of resumes and API response time
- **Memory Usage**: Efficient processing with temporary file cleanup
- **Scalability**: Optimized for both single and batch resume processing

## 🚨 **Troubleshooting & Common Issues**

### **Common Issues & Solutions**

#### **1. API Key Errors**
- **Problem**: "Invalid API key" or "Insufficient credits"
- **Solution**: 
  - Verify your OpenAI API key is valid
  - Check API key has sufficient credits
  - Ensure no extra spaces in the key

#### **2. File Upload Issues**
- **Problem**: "Invalid file type" or "File too large"
- **Solution**:
  - Use supported formats: PDF, DOCX, DOC, TXT
  - Keep files under 50MB
  - For batch uploads, ensure ZIP contains only supported formats

#### **3. Analysis Failures**
- **Problem**: "Could not extract text" or "Analysis failed"
- **Solution**:
  - Check internet connection for API calls
  - Ensure job description is complete and detailed
  - Verify resume files contain extractable text (not just images)

#### **4. Batch Scoring Issues**
- **Problem**: All resumes getting identical scores
- **Solution**: 
  - The system now automatically detects batch analysis
  - Uses specialized prompts for varied scoring
  - Check console logs for "BATCH" mode confirmation

#### **5. Skills Analysis Errors**
- **Problem**: "Could not parse response" in skills section
- **Solution**:
  - The system now has robust JSON parsing
  - Automatically extracts skills even with extra text
  - Check console for detailed error logs

### **Error Messages & Meanings**

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| "No valid resumes found" | No supported files in upload | Check file formats and content |
| "Could not extract text" | Resume is image-based or corrupted | Use text-based resumes |
| "Invalid file type" | Unsupported file format | Use PDF, DOCX, DOC, or TXT |
| "API key required" | Missing OpenAI API key | Enter valid API key |
| "File too large" | Exceeds 50MB limit | Compress or split files |

### **Debug Commands**

```bash
# Check server health
curl http://localhost:5000/health

# Debug session data
curl http://localhost:5000/debug-session

# Test batch scoring
python test_batch_scoring.py
```

### **Console Logs to Watch For**

```
Analysis Mode: BATCH - Processing 3 resumes
Analyzing: resume1.pdf (Batch mode: True)
  resume1.pdf Score: 85%
Analyzing: resume2.pdf (Batch mode: True)
  resume2.pdf Score: 72%
```

## 🧪 **Testing & Development**

### **Running Tests**
```bash
# Comprehensive API testing
python test_resume_matching.py

# Batch scoring verification
python test_batch_scoring.py

# Local deployment helper
python deploy.py
```

### **Development Features**
- **Debug Mode**: Automatic console logging
- **Batch Analysis Detection**: Smart scoring for multiple resumes
- **Robust Error Handling**: Graceful fallbacks for parsing issues
- **Session Management**: Temporary data storage for exports

## 🚀 **Quick Start Examples**

### **Example 1: Single Resume Analysis (API)**
1. Start the server: `python app.py`
2. Open Postman and create a POST request to `http://localhost:5000/analyze`
3. Set body to form-data with your API key, job description, and resume file
4. Send request and get detailed analysis

### **Example 2: Batch Resume Analysis (API)**
1. Create a ZIP file with multiple resumes
2. Use Postman with `uploadType: folder`
3. Upload the ZIP file
4. Get ranked results for all candidates

### **Example 3: Web Interface (Browser)**
1. Open `http://localhost:5000` in your browser
2. Fill in job details and upload resumes
3. View results and download reports

### **Example 4: Docker Deployment**
```bash
# Quick start with Docker
docker-compose up -d
# Access at http://localhost:5000
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly with the provided test scripts
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 **Support & Help**

### **Getting Help**
1. Check the troubleshooting section above
2. Review console logs for detailed error information
3. Use the debug endpoints: `/health` and `/debug-session`
4. Create an issue in the repository with:
   - Error messages
   - Console logs
   - Steps to reproduce

### **Common Questions & Answers**

| Question | Answer |
|----------|---------|
| **Why are all my batch resumes getting the same score?** | The system now automatically detects batch analysis and uses specialized prompts for varied scoring. Check console logs for "BATCH" mode confirmation. |
| **How do I use Postman with this API?** | See the detailed Postman setup guide in the "API Endpoints & Postman Usage" section above. |
| **Can I analyze resumes without the web interface?** | Yes! Use the `/analyze` endpoint directly with Postman, curl, or any HTTP client. |
| **How do I get different scores for different candidates?** | The system automatically handles this. For batch analysis, it uses higher temperature and specialized prompts to ensure varied scoring. |
| **What file formats are supported?** | PDF, DOCX, DOC, and TXT files. For batch processing, use ZIP files containing these formats. |
| **Is there a file size limit?** | Yes, maximum 50MB per upload. |

---

## ⚠️ **Important Notes**

- **OpenAI API Key Required**: You need an active OpenAI API key for AI-powered analysis
- **Internet Connection**: Required for API calls to OpenAI
- **File Size Limit**: Maximum 50MB per upload
- **Supported Formats**: PDF, DOCX, DOC, TXT for resumes
- **Batch Processing**: ZIP files for multiple resume analysis
- **Session Data**: Analysis results are temporarily stored for export functionality

---

## 🎯 **Ready to Get Started?**

### **Choose Your Method:**

| Method | Command | Best For |
|--------|---------|----------|
| **🌐 Web Interface** | `python app.py` | Beginners, visual users |
| **📡 API Testing** | Use Postman guide above | Developers, automation |
| **🐳 Docker** | `docker-compose up -d` | Production, deployment |
| **🧪 Testing** | `python test_resume_matching.py` | Development, debugging |

### **🚀 Quick Commands:**
```bash
# Start web interface
python app.py

# Docker deployment
docker-compose up -d

# Run tests
python test_resume_matching.py

# Health check
curl http://localhost:5000/health
```
