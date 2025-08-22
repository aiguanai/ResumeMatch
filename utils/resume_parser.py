import textract

def extract_resume_text(file_path):
    text = textract.process(file_path).decode('utf-8')
    return text
