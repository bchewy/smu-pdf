import os
import requests
from typing import Dict
import json
import re
import logging

class OpenRouterClient:
    def __init__(self, api_key: str, model: str = "google/gemini-pro"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": os.getenv('ALLOWED_HOST', 'http://localhost:5000'),
            "X-Title": "Academic PDF Summarizer",
            "Content-Type": "application/json"
        }
        
    def _validate_response(self, response) -> bool:
        """Validate API response"""
        try:
            response.raise_for_status()
            content = response.json()
            
            # Check for valid response structure
            if 'choices' not in content or not content['choices']:
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"API response validation error: {str(e)}")
            return False

    def _get_max_tokens(self) -> int:
        """Get max tokens based on model"""
        if self.model == "google/gemini-flash-1.5":
            return 1500
        elif self.model == "anthropic/claude-3.5-sonnet:beta":
            return 3000
        else:  # gemini-pro
            return 4000

    def _get_temperature(self) -> float:
        """Get temperature based on model"""
        if self.model == "google/gemini-flash-1.5":
            return 0.5  # More creative for faster model
        elif self.model == "anthropic/claude-3.5-sonnet:beta":
            return 0.2  # More precise for Claude
        else:  # gemini-pro
            return 0.3  # Balanced for default model

    def analyze_document_structure(self, text: str) -> Dict:
        """Analyze document structure using selected model"""
        try:
            prompt = (
                "You are an expert academic document analyzer. Analyze this academic document and extract its complete structure. "
                "Focus on identifying:\n\n"
                "1. Course Objectives (including all specific learning goals)\n"
                "2. Course Areas (all tracks and specializations)\n"
                "3. Competencies (required skills and outcomes)\n"
                "4. Course Assessments (all evaluation methods)\n"
                "5. Course Information (detailed course content)\n"
                "6. University Policies (including accessibility)\n"
                "7. Resources (all reading materials)\n"
                "8. Synopsis (course overview)\n"
                "9. Prerequisites (required background)\n"
                "10. Teaching Staff (instructor information)\n"
                "11. Lesson Plan (course schedule)\n\n"
                "Return ONLY a JSON object with this structure:\n"
                "{\n"
                '  "sections": [\n'
                '    {\n'
                '      "title": "Section Name",\n'
                '      "level": 1,\n'
                '      "subsections": [\n'
                '        {\n'
                '          "title": "Subsection Name",\n'
                '          "items": ["Item 1", "Item 2"]\n'
                '        }\n'
                '      ]\n'
                '    }\n'
                '  ],\n'
                '  "learning_objectives": ["Objective 1", "Objective 2"],\n'
                '  "competencies": ["Competency 1", "Competency 2"],\n'
                '  "resources": ["Resource 1", "Resource 2"]\n'
                "}\n\n"
                f"Text to analyze: {text}"
            )

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self._get_temperature(),
                    "max_tokens": self._get_max_tokens()
                }
            )
            
            if not self._validate_response(response):
                return {"error": "Invalid API response"}
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            
            return {"error": "Could not parse document structure"}

        except Exception as e:
            print(f"Document structure analysis error: {str(e)}")
            return {"error": str(e)}

    def extract_schedule(self, text: str) -> Dict:
        """Extract schedule information using selected model"""
        try:
            prompt = (
                "You are an expert course schedule analyzer. Extract the complete course schedule from this academic document. "
                "Identify:\n\n"
                "1. All course milestones and deadlines\n"
                "2. Weekly topics and activities\n"
                "3. Assessment dates\n"
                "4. Project timelines\n"
                "5. Important events\n\n"
                "Return ONLY a JSON object with this structure:\n"
                "{\n"
                '  "milestones": [\n'
                '    {\n'
                '      "type": "Assignment/Quiz/Project",\n'
                '      "description": "Detailed description",\n'
                '      "week": "Week number"\n'
                '    }\n'
                '  ],\n'
                '  "weekly_plan": [\n'
                '    {\n'
                '      "week": "Week number",\n'
                '      "topic": "Main topic",\n'
                '      "activities": ["Activity 1", "Activity 2"]\n'
                '    }\n'
                '  ]\n'
                "}\n\n"
                f"Text to analyze: {text}"
            )

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self._get_temperature(),
                    "max_tokens": self._get_max_tokens()
                }
            )
            
            if not self._validate_response(response):
                return {"error": "Invalid API response"}
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Extract JSON from response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            
            return {"error": "Could not parse schedule data"}

        except Exception as e:
            print(f"Schedule extraction error: {str(e)}")
            return {"error": str(e)}

    def generate_word_cloud_data(self, text: str) -> Dict:
        """Generate word cloud data using selected model"""
        try:
            prompt = (
                "You are an expert in academic content analysis. Analyze this academic document and identify the most important keywords and concepts. "
                "Consider:\n\n"
                "1. Course-specific terminology\n"
                "2. Key learning objectives\n"
                "3. Important skills and competencies\n"
                "4. Assessment types\n"
                "5. Core topics and concepts\n"
                "6. Resource types\n\n"
                "Return ONLY a JSON array of objects with words and their importance scores (1-100):\n"
                "[\n"
                '  {"word": "keyword", "score": importance_score}\n'
                "]\n\n"
                f"Text to analyze: {text}"
            )

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self._get_temperature(),
                    "max_tokens": self._get_max_tokens()
                }
            )
            
            if not self._validate_response(response):
                return {"error": "Invalid API response"}
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Extract JSON array from response
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return {"keywords": json.loads(json_str)}
            
            return {"error": "Could not parse word cloud data"}

        except Exception as e:
            print(f"Word cloud generation error: {str(e)}")
            return {"error": str(e)}

    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s\.\,\-\:\;\(\)]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def summarize_text(self, text: str) -> Dict:
        """Generate summary using selected model"""
        try:
            prompt = (
                "You are an expert academic document analyzer. Create a comprehensive summary of this academic document. "
                "Include the following sections:\n\n"
                "1. 🎯 TL;DR (Brief Overview)\n"
                "2. 🌟 Key Learning Objectives\n"
                "3. 📚 Course Content\n"
                "4. 📝 Assessment Methods\n"
                "5. 💡 Important Policies\n"
                "6. 📅 Key Dates and Milestones\n\n"
                "Make it engaging and student-friendly while maintaining academic accuracy. "
                "Use clear headings and bullet points where appropriate.\n\n"
                f"Text to analyze: {text}"
            )

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self._get_temperature(),
                    "max_tokens": self._get_max_tokens()
                }
            )
            
            if not self._validate_response(response):
                return {"error": "Invalid API response"}
            
            result = response.json()
            return {
                "Summary": result['choices'][0]['message']['content']
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Summary generation error: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Error response: {e.response.text}")
            return {
                "Summary": "Error generating summary. Please try again."
            }
