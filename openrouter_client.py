import os
import requests
from typing import Dict
import json

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key not found in environment variables")
        print(f"API key length: {len(self.api_key)}")  # Debug line
        
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
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print(f"Response body: {response.text}")
            
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
        """Extract schedule information from text"""
        try:
            prompt = (
                "Extract and structure all schedule-related information from this text. Include:\n"
                "- Course timeline\n"
                "- Assignment due dates\n"
                "- Project milestones\n"
                "- Important deadlines\n"
                "Format the response as a JSON with dates as keys and events as values.\n"
                f"Text: {text}"
            )

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "google/gemini-flash-1.5",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 1000,
                    "response_format": {"type": "json_object"}
                }
            )
            
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Schedule extraction error: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Error response: {e.response.text}")
            raise Exception(f"Error extracting schedule: {str(e)}")
