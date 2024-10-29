from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pdf_processor import PDFProcessor
from openrouter_client import OpenRouterClient
from visualization_handler import VisualizationHandler
from utils import validate_pdf_file, sanitize_text
from time import sleep
import os

load_dotenv()  # Load environment variables from .env file

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def show_progress_bar(text="Processing"):
    """Shows a progress bar with custom text"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f"{text}: {i+1}%")
        sleep(0.01)
    progress_bar.empty()
    status_text.empty()

def process_pdf_with_progress(uploaded_file, pdf_processor, openrouter_client, viz_handler):
    """Process PDF with detailed progress updates"""
    progress = st.progress(0)
    status = st.empty()
    
    try:
        # Extract text
        status.text("📄 Extracting text from PDF...")
        progress.progress(10)
        raw_text = pdf_processor.extract_text(uploaded_file)
        
        # Preprocess text
        status.text("🔍 Preprocessing text...")
        progress.progress(20)
        processed_text = openrouter_client.preprocess_text(raw_text)
        
        # Analyze document structure
        status.text("📊 Analyzing document structure...")
        progress.progress(35)
        structure_data = openrouter_client.analyze_document_structure(processed_text)
        
        # Generate word cloud
        status.text("☁️ Generating word cloud...")
        progress.progress(50)
        word_cloud_data = openrouter_client.generate_word_cloud_data(processed_text)
        
        # Extract schedule
        status.text("📅 Extracting schedule information...")
        progress.progress(65)
        schedule_data = openrouter_client.extract_schedule(processed_text)
        
        # Generate summary
        status.text("📝 Generating summary...")
        progress.progress(80)
        summary_data = openrouter_client.summarize_text(processed_text)
        
        # Final processing
        status.text("✨ Finalizing analysis...")
        progress.progress(100)
        sleep(0.5)
        
        progress.empty()
        status.empty()
        
        return structure_data, word_cloud_data, schedule_data, summary_data
        
    except Exception as e:
        progress.empty()
        status.error(f"Error: {str(e)}")
        raise e

def check_api_key():
    """Verify API key is properly configured"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        st.error("⚠️ OpenRouter API key not configured. Please check server configuration.")
        st.stop()
    return api_key

def format_summary(summary_data: dict) -> str:
    """Format the summary data into a readable string"""
    if isinstance(summary_data, dict) and 'Summary' in summary_data:
        return summary_data['Summary']
    return "No summary available"

def main():
    st.set_page_config(
        page_title="Academic PDF Summarizer",
        page_icon="📚",
        layout="wide"
    )
    
    # Check API key before proceeding
    api_key = check_api_key()
    
    st.title("📚 Academic PDF Summarizer")
    
    # Add model selector in a sidebar
    st.sidebar.title("⚙️ Settings")
    model_options = {
        "Google Gemini Pro (Default)": "google/gemini-pro",
        "Anthropic Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet:beta",
        "Google Gemini Flash": "google/gemini-flash-1.5"
    }
    
    selected_model = st.sidebar.selectbox(
        "🤖 Select AI Model",
        options=list(model_options.keys()),
        help="Choose the AI model for analysis. Different models may have different strengths and processing speeds."
    )
    
    # Add after model selector
    st.sidebar.markdown("""
        <div class="model-info">
        <b>Model Characteristics:</b>
        
        🚀 <b>Gemini Pro (Default)</b>
        - Best all-around performance
        - Balanced speed and accuracy
        - Recommended for most uses
        
        🧠 <b>Claude 3.5 Sonnet</b>
        - More detailed analysis
        - Better at complex documents
        - Slower processing
        
        ⚡ <b>Gemini Flash</b>
        - Fastest processing
        - Good for quick overview
        - Less detailed analysis
        </div>
        """, unsafe_allow_html=True)
    
    # Add rate limiting per session
    if 'request_count' not in st.session_state:
        st.session_state.request_count = 0
    
    if st.session_state.request_count >= 10:
        st.error("⚠️ Request limit reached. Please try again later.")
        st.stop()
    
    uploaded_file = st.file_uploader("Upload your academic PDF", type="pdf")
    
    if uploaded_file is not None:
        if not validate_pdf_file(uploaded_file):
            st.error("Please upload a valid PDF file.")
            return
            
        try:
            # Initialize components with selected model
            pdf_processor = PDFProcessor()
            openrouter_client = OpenRouterClient(
                api_key=api_key,
                model=model_options[selected_model]
            )
            viz_handler = VisualizationHandler()

            # Process PDF with progress updates
            with st.spinner("Processing PDF..."):
                structure_data, word_cloud_data, schedule_data, summary_data = process_pdf_with_progress(
                    uploaded_file, pdf_processor, openrouter_client, viz_handler
                )
            
            # Create tabs
            tab1, tab2, tab3 = st.tabs([
                "📊 Document Structure", 
                "☁️ Word Cloud",
                "📅 Schedule Timeline"
            ])

            with tab1:
                if 'error' not in structure_data:
                    st.plotly_chart(
                        viz_handler.create_document_structure_visualization(structure_data),
                        use_container_width=True
                    )
                else:
                    st.error("Could not analyze document structure")

            with tab2:
                if 'error' not in word_cloud_data:
                    st.plotly_chart(
                        viz_handler.create_word_cloud_visualization(word_cloud_data),
                        use_container_width=True
                    )
                else:
                    st.error("Could not generate word cloud")

            with tab3:
                if 'error' not in schedule_data:
                    st.plotly_chart(
                        viz_handler.create_schedule_timeline(schedule_data),
                        use_container_width=True
                    )
                else:
                    st.error("Could not extract schedule information")

            # Summary section
            st.subheader("📝 Document Summary")
            if isinstance(summary_data, dict) and 'Summary' in summary_data:
                summary_text = summary_data['Summary']
                st.markdown(summary_text)
                
                col1, col2 = st.columns(2)
                with col1:
                    # Use Streamlit's built-in download button
                    st.download_button(
                        label="⬇️ Download Summary",
                        data=summary_text,
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                with col2:
                    if st.button("📋 Copy to Clipboard"):
                        st.code(summary_text)  # Display in a copyable code block
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    else:
        st.info("👆 Please upload a PDF file to begin.")

if __name__ == "__main__":
    main()
