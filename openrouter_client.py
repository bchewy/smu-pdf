import os
import requests
from typing import Dict
import json

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
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
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            
            response.raise_for_status()
            result = response.json()
            return json.loads(result['choices'][0]['message']['content'])
            
        except Exception as e:
            raise Exception(f"Error calling OpenRouter API: {str(e)}")
