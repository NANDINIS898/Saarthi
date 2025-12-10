# server/llm_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_response(prompt: str):
    """
    Call Groq API with OpenAI-compatible format.
    Available models: llama-3.3-70b-versatile, mixtral-8x7b-32768, gemma2-9b-it
    """
    if not GROQ_API_KEY:
        print("Warning: GROQ_API_KEY not found in environment")
        return "LLM API key not configured."
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Use OpenAI-compatible chat completions format
    data = {
        "model": "llama-3.3-70b-versatile",  # Groq's fastest model
        "messages": [
            {
                "role": "system",
                "content": "You are Saarthi, a helpful and professional loan assistant. Provide clear, concise, and friendly responses."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            # Extract the assistant's message from the response
            return result.get("choices", [{}])[0].get("message", {}).get("content", "No response from LLM.")
        else:
            error_detail = response.json() if response.text else {"error": "Unknown error"}
            print(f"Groq API Error {response.status_code}: {error_detail}")
            return f"Error contacting LLM API (Status: {response.status_code})."
            
    except requests.exceptions.Timeout:
        print("Groq API request timed out")
        return "LLM API request timed out."
    except Exception as e:
        print(f"Groq API Exception: {str(e)}")
        return f"Error contacting LLM API: {str(e)}"


def get_conversational_response(conversation_history: list, system_prompt: str) -> str:
    """
    Get a conversational response using full conversation history.
    
    Args:
        conversation_history: List of {"role": "user/assistant", "content": "..."}
        system_prompt: System prompt defining agent personality and behavior
        
    Returns:
        Assistant's response
    """
    if not GROQ_API_KEY:
        print("Warning: GROQ_API_KEY not found in environment")
        return "LLM API key not configured."
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Build messages array with system prompt and conversation history
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    for msg in conversation_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0.8  # Slightly higher for more natural conversation
    }

    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "I'm sorry, I couldn't generate a response.")
        else:
            error_detail = response.json() if response.text else {"error": "Unknown error"}
            print(f"Groq API Error {response.status_code}: {error_detail}")
            return "I'm having trouble connecting right now. Please try again in a moment."
            
    except requests.exceptions.Timeout:
        print("Groq API request timed out")
        return "I'm taking a bit longer than usual. Please try again."
    except Exception as e:
        print(f"Groq API Exception: {str(e)}")
        return "I encountered an error. Please try again."
