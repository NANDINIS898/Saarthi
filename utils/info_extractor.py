# utils/info_extractor.py
import json
import re
from typing import Dict, Optional
from server.llm_api import get_groq_response
from utils.conversation_prompts import EXTRACTION_PROMPT


def extract_information_from_conversation(conversation_history: list) -> Dict[str, Optional[any]]:
    """
    Extract structured loan information from conversation history using LLM.
    
    Args:
        conversation_history: List of conversation messages
        
    Returns:
        Dictionary with extracted information
    """
    # For now, use simple regex-based extraction as fallback
    # This ensures the system works while we can improve LLM extraction later
    
    all_text = " ".join([msg.get("content", "") for msg in conversation_history])
    
    extracted = get_empty_info()
    
    # Extract name (look for "I am X" or "my name is X")
    name_patterns = [
        r"(?:I am|I'm|my name is|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:here|speaking)"
    ]
    for pattern in name_patterns:
        match = re.search(pattern, all_text, re.IGNORECASE)
        if match:
            extracted["name"] = match.group(1).strip()
            break
    
    # Extract amount (look for numbers with lakh/crore)
    amount_match = re.search(r'(\d+(?:\.\d+)?)\s*(lakh|lac|crore|cr|thousand|k|₹|rupees?)', all_text, re.IGNORECASE)
    if amount_match:
        extracted["amount"] = convert_amount_to_number(amount_match.group(0))
    
    # Extract tenure (look for X years/months)
    tenure_match = re.search(r'(\d+)\s*(year|yr|month)', all_text, re.IGNORECASE)
    if tenure_match:
        years = int(tenure_match.group(1))
        if 'month' in tenure_match.group(2).lower():
            years = years / 12
        extracted["tenure"] = int(years) if years >= 1 else None
    
    return extracted


def parse_json_from_response(response: str) -> dict:
    """
    Parse JSON from LLM response, handling various formats.
    """
    try:
        # Try direct JSON parsing
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to find JSON block with better regex
        # Look for content between first { and last }
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = response[start_idx:end_idx+1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                print(f"Attempted to parse: {json_str[:200]}")
        
        # Return empty info if parsing fails
        print(f"Could not extract JSON from response: {response[:200]}")
        return get_empty_info()


def validate_and_clean_info(info: dict) -> dict:
    """
    Validate and clean extracted information.
    """
    cleaned = get_empty_info()
    
    # Validate name (string)
    if info.get("name") and isinstance(info["name"], str):
        cleaned["name"] = info["name"].strip()
    
    # Validate amount (number, positive)
    if info.get("amount"):
        try:
            amount = float(info["amount"])
            if amount > 0:
                cleaned["amount"] = int(amount)
        except (ValueError, TypeError):
            pass
    
    # Validate tenure (number, 1-30 years)
    if info.get("tenure"):
        try:
            tenure = float(info["tenure"])
            if 1 <= tenure <= 30:
                cleaned["tenure"] = int(tenure)
        except (ValueError, TypeError):
            pass
    
    # Validate purpose (string)
    if info.get("purpose") and isinstance(info["purpose"], str):
        cleaned["purpose"] = info["purpose"].strip().lower()
    
    # Validate income (number, positive)
    if info.get("income"):
        try:
            income = float(info["income"])
            if income > 0:
                cleaned["income"] = int(income)
        except (ValueError, TypeError):
            pass
    
    # Validate employment (string)
    if info.get("employment") and isinstance(info["employment"], str):
        cleaned["employment"] = info["employment"].strip().lower()
    
    # Validate email (basic check)
    if info.get("email") and isinstance(info["email"], str):
        if "@" in info["email"]:
            cleaned["email"] = info["email"].strip()
    
    # Validate phone (basic check)
    if info.get("phone"):
        phone_str = str(info["phone"]).strip()
        # Remove common separators
        phone_clean = re.sub(r'[^\d+]', '', phone_str)
        if len(phone_clean) >= 10:
            cleaned["phone"] = phone_clean
    
    return cleaned


def get_empty_info() -> dict:
    """
    Return empty information dictionary.
    """
    return {
        "name": None,
        "amount": None,
        "tenure": None,
        "purpose": None,
        "income": None,
        "employment": None,
        "email": None,
        "phone": None
    }


def convert_amount_to_number(amount_str: str) -> Optional[int]:
    """
    Convert amount string to number (handles lakhs, crores, etc.)
    
    Examples:
        "5 lakhs" -> 500000
        "10 lakh" -> 1000000
        "2 crore" -> 20000000
        "500000" -> 500000
    """
    if not amount_str:
        return None
    
    amount_str = amount_str.lower().strip()
    
    # Extract number
    number_match = re.search(r'[\d.]+', amount_str)
    if not number_match:
        return None
    
    try:
        number = float(number_match.group())
    except ValueError:
        return None
    
    # Check for lakhs/crores
    if 'crore' in amount_str or 'cr' in amount_str:
        number *= 10000000
    elif 'lakh' in amount_str or 'lac' in amount_str or 'l' in amount_str:
        number *= 100000
    elif 'thousand' in amount_str or 'k' in amount_str:
        number *= 1000
    
    return int(number)
