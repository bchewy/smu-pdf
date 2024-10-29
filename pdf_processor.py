import io
import PyPDF2

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
