from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pdf_processor import PDFProcessor
from openrouter_client import OpenRouterClient
from visualizer import Visualizer
from utils import create_download_link, format_summary, validate_pdf_file
from collections import Counter
import textstat

load_dotenv()  # Load environment variables from .env file

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Academic PDF Summarizer",
        page_icon="📚",
        layout="wide"
    )
    
    load_css()
    
    st.markdown('<h1 class="main-header">Academic PDF Summarizer</h1>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your academic PDF", type="pdf")
    
    if uploaded_file is not None:
        if not validate_pdf_file(uploaded_file):
            st.error("Please upload a valid PDF file.")
            return
            
        with st.spinner("Processing PDF..."):
            try:
                # Extract text from PDF
                pdf_processor = PDFProcessor()
                text_content = pdf_processor.extract_text(uploaded_file)
                sections = pdf_processor.get_structure(text_content)
                
                # Create visualizations using tabs
                visualizer = Visualizer()
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "Document Structure", 
                    "Word Cloud", 
                    "Readability", 
                    "Learning Objectives",
                    "Schedule Timeline"
                ])

                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(
                            visualizer.create_structure_chart(sections),
                            use_container_width=True
                        )
                    with col2:
                        st.plotly_chart(
                            visualizer.create_length_chart(sections),
                            use_container_width=True
                        )

                with tab2:
                    st.plotly_chart(
                        visualizer.create_word_cloud(text_content),
                        use_container_width=True
                    )

                with tab3:
                    st.plotly_chart(
                        visualizer.create_readability_chart(text_content),
                        use_container_width=True
                    )

                with tab4:
                    st.plotly_chart(
                        visualizer.create_objectives_tracker(sections),
                        use_container_width=True
                    )

                with tab5:
                    st.subheader("Course Schedule")
                    openrouter_client = OpenRouterClient()
                    schedule_data = openrouter_client.extract_schedule(text_content)
                    
                    if schedule_data:
                        st.plotly_chart(
                            visualizer.create_schedule_timeline(schedule_data),
                            use_container_width=True
                        )
                    else:
                        st.info("No schedule information found in the document.")
                
                # Generate summary
                openrouter_client = OpenRouterClient()
                summary = openrouter_client.summarize_text(text_content)
                
                st.markdown('<div class="summary-container">', unsafe_allow_html=True)
                st.subheader("Document Summary")
                
                for section, content in summary.items():
                    st.markdown(f"### {section}")
                    st.write(content)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download options
                formatted_summary = format_summary(summary)
                st.markdown(
                    create_download_link(formatted_summary, "summary.txt"),
                    unsafe_allow_html=True
                )
                
                # Copy to clipboard button
                st.button(
                    "Copy Summary to Clipboard",
                    on_click=lambda: st.write(formatted_summary)
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    else:
        st.info("Please upload a PDF file to begin.")

if __name__ == "__main__":
    main()
