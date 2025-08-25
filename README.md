# Resume Matching API

A Flask-based API service that provides comprehensive resume matching and skills analysis using ChatGPT. This service can analyze resumes against job descriptions and provide detailed insights about match percentages, skills gaps, and recommendations.

## Features

1. **Resume Matching Percentage**: Get detailed match analysis including overall, skills, experience, and education match percentages
2. **Skills Analysis**: Analyze matched skills, missing skills, and skill gaps with priority levels
3. **ChatGPT Integration**: Uses OpenAI's GPT-4 for intelligent analysis and recommendations
4. **Multi-format Support**: Supports PDF, DOCX, DOC, and TXT resume formats
5. **Batch Processing**: Analyze multiple resumes at once
6. **Comprehensive Analysis**: Get both match percentage and skills analysis in a single request

## Prerequisites

- Python 3.7+
- OpenAI API key
- Virtual environment (recommended)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Resume_Match
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env file and add your OpenAI API key
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### 1. Health Check
- **GET** `/health`
- Returns server status and version information

#### 2. Get Default Job Description
- **GET** `/default-job-description`
- Returns the default Senior Software Engineer job description

#### 3. List Available Resumes
- **GET** `/list-resumes`
- Lists all resume files in the `resumes/` directory

#### 4. Resume Match Percentage
- **POST** `/match-percentage`
- Analyzes resume against job description and returns match percentages

**Request Body**:
```json
{
    "resume": "resume text content",
    "job_description": "optional custom job description"
}
```

**Response**:
```json
{
    "overall_match_percentage": 85,
    "skills_match_percentage": 90,
    "experience_match_percentage": 80,
    "education_match_percentage": 95,
    "detailed_analysis": {
        "strengths": ["Strong Java experience", "Relevant project experience"],
        "weaknesses": ["Limited JavaScript experience"],
        "recommendations": ["Consider learning more JavaScript frameworks"]
    },
    "key_matches": ["Java development", "Spring Framework"],
    "missing_requirements": ["Advanced JavaScript skills"]
}
```

#### 5. Skills Analysis
- **POST** `/skills-analysis`
- Analyzes skills match and gaps between resume and job description

**Request Body**:
```json
{
    "resume": "resume text content",
    "job_description": "optional custom job description"
}
```

**Response**:
```json
{
    "matched_skills": {
        "must_have": ["Java", "Spring"],
        "nice_to_have": ["JavaScript"],
        "additional": ["MySQL", "Linux"]
    },
    "missing_skills": {
        "critical": ["Advanced JavaScript"],
        "important": ["React", "Node.js"],
        "optional": ["Docker", "Kubernetes"]
    },
    "skill_gaps": {
        "high_priority": ["Advanced JavaScript"],
        "medium_priority": ["React"],
        "low_priority": ["Docker"]
    },
    "skill_analysis": {
        "technical_skills_match": 85,
        "soft_skills_match": 90,
        "domain_knowledge_match": 80
    },
    "recommendations": ["Focus on JavaScript frameworks", "Learn React"]
}
```

#### 6. Comprehensive Analysis
- **POST** `/comprehensive-analysis`
- Get both match percentage and skills analysis in a single request

**Request Body**:
```json
{
    "resume": "resume text content",
    "job_description": "optional custom job description"
}
```

#### 7. Analyze Specific Resume File
- **POST** `/analyze-resume-file`
- Analyze a specific resume file from the `resumes/` directory

**Request Body**:
```json
{
    "filename": "resume.pdf",
    "job_description": "optional custom job description"
}
```

#### 8. Analyze All Resumes
- **GET** `/analyze-all-resumes`
- Analyze all resumes in the `resumes/` directory against the default job description

### Testing the API

Run the test script to verify all endpoints:

```bash
python test_resume_matching.py
```

### Example Usage with curl

```bash
# Health check
curl http://localhost:5000/health

# Get match percentage
curl -X POST http://localhost:5000/match-percentage \
  -H "Content-Type: application/json" \
  -d '{"resume": "Sample resume text", "job_description": "Sample job description"}'

# Analyze all resumes
curl http://localhost:5000/analyze-all-resumes
```

## Default Job Description

The API comes with a pre-configured job description for a Senior Software Engineer position:

- **Experience Required**: 4-7 years
- **Must-Have Skills**: Java
- **Nice-to-Have Skills**: JavaScript
- **Industry**: Information Technology
- **Education**: Bachelor's or Master's Degree in Computer Science

## File Structure

```
Resume_Match/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── test_resume_matching.py # Test script
├── .env                   # Environment variables (create from env_example.txt)
├── resumes/              # Directory containing resume files
├── services/             # Business logic services
│   ├── llm_utils.py      # OpenAI API integration
│   ├── match_percentage.py # Match percentage analysis
│   └── skills_analysis.py # Skills analysis
└── utils/                # Utility functions
    ├── jd_parser.py      # Job description parsing
    └── resume_parser.py  # Resume text extraction
```

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider using:
- Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- Docker containerization
- Cloud platforms (AWS, Google Cloud, Azure)

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Debug mode (True/False)

## Error Handling

The API includes comprehensive error handling:
- Invalid JSON requests
- Missing required fields
- File not found errors
- OpenAI API errors
- Resume parsing errors

## Limitations

- Requires OpenAI API key and credits
- Resume parsing depends on file format and quality
- Analysis quality depends on ChatGPT's understanding
- Rate limits apply based on OpenAI API tier

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the API documentation at `http://localhost:5000`
2. Review the test script for usage examples
3. Check the logs for error details
