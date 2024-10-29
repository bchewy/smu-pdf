import base64
import json
from typing import Dict, Any

def create_download_link(content: str, filename: str) -> str:
    """Create a download link for text content"""
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download Summary</a>'

def format_summary(summary_data: Dict[Any, Any]) -> str:
    """Format the summary data into a readable string"""
    formatted = []
    for section, content in summary_data.items():
        formatted.append(f"## {section}\n{content}\n")
    return "\n".join(formatted)

def validate_pdf_file(file):
    """Validate uploaded PDF file"""
    if file is None:
        return False
    return file.type == "application/pdf"
