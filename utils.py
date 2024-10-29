import base64
import json
from typing import Dict, Any
import re
from typing import Optional
import mimetypes  # Built-in Python library

def create_download_link(content: str, filename: str) -> str:
    """Create a download link for text content"""
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download Summary</a>'

def format_summary(summary_data: dict) -> str:
    """Format the summary data into a readable string"""
    if isinstance(summary_data, dict) and 'Summary' in summary_data:
        return summary_data['Summary']
    return "No summary available"

def validate_pdf_file(uploaded_file) -> bool:
    """
    Validate uploaded file for security
    """
    if uploaded_file is None:
        return False
        
    try:
        # Check file size (e.g., 10MB limit)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
        if uploaded_file.size > MAX_FILE_SIZE:
            return False
            
        # Check file type using file extension and MIME type
        file_type, _ = mimetypes.guess_type(uploaded_file.name)
        if file_type != 'application/pdf':
            return False
            
        # Check filename for security
        if not re.match(r'^[\w\-. ]+\.pdf$', uploaded_file.name):
            return False
            
        # Additional check: try to read first few bytes
        try:
            content_start = uploaded_file.read(5)
            uploaded_file.seek(0)  # Reset file pointer
            # Check for PDF file signature
            if content_start[:4] != b'%PDF':
                return False
        except:
            return False
            
        return True
        
    except Exception as e:
        print(f"File validation error: {str(e)}")
        return False

def sanitize_text(text: str) -> str:
    """
    Sanitize text input
    """
    # Remove potential HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.,!?\-()]', '', text)
    return text.strip()
