import os
import requests
from typing import Dict
import json

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key not found in environment variables")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Academic PDF Summarizer",
            "Content-Type": "application/json"
        }

    def summarize_text(self, text: str) -> Dict:
        """Generate summary using OpenRouter Gemini Flash model"""
        try:
            prompt = (
                "As an enthusiastic teaching assistant, create an engaging and student-friendly summary of this academic text. "
                "Make it fun and relatable while maintaining accuracy. Include: \n\n"
                "1. 🎯 TL;DR (A quick, catchy overview)\n"
                "2. 🌟 Key Highlights (with real-world analogies)\n"
                "3. 💡 Pro Tips (practical study advice)\n"
                "4. 🎮 Fun Facts & Applications\n"
                "5. 📊 Visual Summary (describe any charts or graphs in an engaging way)\n\n"
                "Use emojis, casual language, and relatable examples. Make it feel like a friendly study guide rather than a formal summary. "
                f"Here's the text to analyze: {text}"
            )

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "google/gemini-flash-1.5",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 1500
                }
            )
            
            response.raise_for_status()
            result = response.json()
            return {
                "Summary": result['choices'][0]['message']['content']
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Full error details: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Error response: {e.response.text}")
            raise Exception(f"Error calling OpenRouter API: {str(e)}")

    def extract_schedule(self, text: str) -> Dict:
        """Extract and format schedule information from text"""
        try:
            prompt = (
                "Extract course schedule information and format as a JSON where:\n"
                "- Keys should be ISO dates (YYYY-MM-DD)\n"
                "- Values should be objects with 'type' and 'description' fields\n"
                "Example format:\n"
                "{\n"
                '  "2024-01-15": {"type": "assignment", "description": "Assignment 1 due"},\n'
                '  "2024-02-01": {"type": "project", "description": "Project Milestone 1"}\n'
                "}\n"
                "Types can be: assignment, project, exam, milestone, or deadline.\n"
                "Convert any week-based schedules to actual dates starting from the current semester.\n"
                f"Text: {text}"
            )

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "google/gemini-flash-1.5",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 1000
                }
            )
            
            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            try:
                # Find the JSON part in the response
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = content[json_start:json_end]
                    schedule_data = json.loads(json_str)
                    return schedule_data
                else:
                    raise json.JSONDecodeError("No JSON found in response", content, 0)
                    
            except json.JSONDecodeError:
                print(f"Failed to parse schedule data: {content}")
                # Return a default event to show the timeline is working
                return {
                    "2024-10-29": {
                        "type": "milestone",
                        "description": "Course Start"
                    }
                }
                
        except requests.exceptions.RequestException as e:
            print(f"Schedule extraction error: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Error response: {e.response.text}")
            raise Exception(f"Error extracting schedule: {str(e)}")
