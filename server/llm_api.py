# server/llm_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Example endpoint

def get_groq_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-neo-3.5",  # or whichever LLM Groq provides
        "input": prompt,
        "max_output_tokens": 200
    }

    response = requests.post(GROQ_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("output", "Sorry, I didn't understand that.")
    else:
        return "Error contacting LLM API."
