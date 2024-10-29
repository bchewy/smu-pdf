from flask import Flask, request, jsonify
from pdf_processor import PDFProcessor
from openrouter_client import OpenRouterClient
from visualization_handler import VisualizationHandler

app = Flask(__name__)

class App:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.client = OpenRouterClient()
        self.viz_handler = VisualizationHandler()

    def process_pdf(self, pdf_file):
        try:
            # Extract text from PDF
            raw_text = self.pdf_processor.extract_text(pdf_file)
            
            # Preprocess the text
            processed_text = self.client.preprocess_text(raw_text)
            
            # Get all analyses from OpenRouter
            results = {
                'summary': self.client.summarize_text(processed_text),
                'structure': self.client.analyze_document_structure(processed_text),
                'word_cloud': self.client.generate_word_cloud_data(processed_text),
                'schedule': self.client.extract_schedule(processed_text)
            }
            
            # Generate visualizations
            visualizations = {
                'structure_viz': self.viz_handler.create_document_structure_visualization(
                    results['structure']
                ).to_dict(),  # Convert Plotly figure to JSON-serializable format
                'word_cloud_viz': self.viz_handler.create_word_cloud_visualization(
                    results['word_cloud']
                ).to_dict()  # Convert Plotly figure to JSON-serializable format
            }
            
            return {
                'success': True,
                'data': {
                    'summary': results['summary'],
                    'schedule': results['schedule'],
                    'structure_fig': visualizations['structure_viz'],
                    'word_cloud_fig': visualizations['word_cloud_viz']
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
        
    if file and file.filename.endswith('.pdf'):
        app_instance = App()
        result = app_instance.process_pdf(file)
        
        if result['success']:
            return jsonify(result['data'])
        else:
            return jsonify({'error': result['error']}), 500
    
    return jsonify({'success': False, 'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)