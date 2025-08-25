import textract
import os
import PyPDF2
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
            # Try textract first
            try:
                text = textract.process(file_path).decode('utf-8')
                if text and text.strip():
                    return text.strip()
            except Exception as e:
                print(f"textract failed for {file_path}: {str(e)}")
            
            # If textract fails for PDF, try PyPDF2 as fallback
            if file_extension == '.pdf':
                try:
                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        text = ""
                        for page in pdf_reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        if text.strip():
                            return text.strip()
                except Exception as e:
                    print(f"PyPDF2 failed for {file_path}: {str(e)}")
            
            return f"Error extracting text from {file_path}: All methods failed"
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
        print(f"Resumes directory '{resumes_dir}' does not exist")
        return resumes
    
    print(f"Scanning directory: {resumes_dir}")
    
    # Get all files
    all_files = os.listdir(resumes_dir)
    pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    docx_files = [f for f in all_files if f.lower().endswith('.docx')]
    doc_files = [f for f in all_files if f.lower().endswith('.doc')]
    txt_files = [f for f in all_files if f.lower().endswith('.txt')]
    
    print(f"Found {len(pdf_files)} PDF files, {len(docx_files)} DOCX files, {len(doc_files)} DOC files, {len(txt_files)} TXT files")
    
    # Process all supported files
    supported_files = pdf_files + docx_files + doc_files + txt_files
    
    for filename in supported_files:
        print(f"Processing: {filename}")
        file_path = os.path.join(resumes_dir, filename)
        
        # Check file permissions
        if not os.access(file_path, os.R_OK):
            print(f"  ❌ Cannot read file: {filename}")
            continue
        
        # Extract text
        text = extract_resume_text(file_path)
        
        if text and not text.startswith("Error"):
            resumes[filename] = text
            print(f"  ✅ Success: {len(text)} characters")
        else:
            print(f"  ❌ Failed: {text}")
    
    print(f"Successfully processed {len(resumes)} out of {len(supported_files)} files")
    return resumes
