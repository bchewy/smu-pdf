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
                "Please analyze and summarize the following academic text. "
                "Provide a structured summary including: \n"
                "1. Main Findings\n"
                "2. Key Concepts\n"
                "3. Methodology\n"
                "4. Conclusions\n\n"
                f"Text: {text}"
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
