import io
import PyPDF2
from typing import List

class PDFProcessor:
    @staticmethod
    def extract_text(pdf_file) -> str:
        """Extract text content from uploaded PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    @staticmethod
    def get_structure(text: str) -> List[dict]:
        """Analyze PDF structure and return sections"""
        sections = []
        current_section = ""
        current_text = []
        
        for line in text.split('\n'):
            # Check for important notice markers
            is_important = any(keyword in line.lower() for keyword in 
                ['important', 'notice', 'warning', 'attention', 'note'])
            
            if line.strip().isupper() or line.strip().startswith('#') or is_important:
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': ' '.join(current_text),
                        'type': 'important' if any(keyword in current_section.lower() 
                               for keyword in ['important', 'notice', 'warning', 'attention', 'note']) 
                               else 'regular'
                    })
                current_section = line.strip()
                current_text = []
            else:
                current_text.append(line.strip())
        
        if current_section:
            sections.append({
                'title': current_section,
                'content': ' '.join(current_text),
                'type': 'important' if any(keyword in current_section.lower() 
                       for keyword in ['important', 'notice', 'warning', 'attention', 'note']) 
                       else 'regular'
            })
        
        return sections
