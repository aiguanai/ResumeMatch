import textract
import os
from typing import Optional

def extract_resume_text(file_path: str) -> Optional[str]:
    """
    Extract text from resume files (PDF, DOCX, etc.)
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        # Handle different file extensions
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in ['.pdf', '.docx', '.doc', '.txt']:
            text = textract.process(file_path).decode('utf-8')
            return text.strip()
        else:
            return f"Unsupported file format: {file_extension}"
            
    except Exception as e:
        return f"Error extracting text from {file_path}: {str(e)}"

def get_all_resumes(resumes_dir: str = "resumes") -> dict:
    """
    Get all resumes from the resumes directory
    """
    resumes = {}
    
    if not os.path.exists(resumes_dir):
        return resumes
    
    for filename in os.listdir(resumes_dir):
        if filename.lower().endswith(('.pdf', '.docx', '.doc', '.txt')):
            file_path = os.path.join(resumes_dir, filename)
            text = extract_resume_text(file_path)
            if text and not text.startswith("Error"):
                resumes[filename] = text
    
    return resumes
