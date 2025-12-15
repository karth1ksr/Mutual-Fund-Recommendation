import re
import json
from typing import Optional, Dict, Any

def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Robust JSON extractor from LLM text responses.
    """
    if not text:
        return None
        
    # Remove markdown fences
    text = text.replace("```json", "").replace("```", "").strip()

    # Remove citations like [1], [23]
    text = re.sub(r"\[\d+\]", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object with regex
    match = re.search(r"\{(?:.|\n)*\}", text)
    if match:
        candidate = re.sub(r"\[\d+\]", "", match.group())
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None

    return None

def strip_citations(text: str) -> str:
    """Remove Perplexity-style citation markers like [3], [12]."""
    if not isinstance(text, str):
        return text
    return re.sub(r"\[\d+\]", "", text).strip()
