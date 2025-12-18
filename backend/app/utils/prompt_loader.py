import os
import logging
from string import Template
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Determine the absolute path to the prompts directory
# This assumes the file structure: backend/app/utils/prompt_loader.py -> backend/app/prompts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

def load_prompt(filename: str, **kwargs) -> str:
    """
    Loads a prompt template from a file and substitutes variables using string.Template.
    
    Args:
        filename (str): The name of the prompt file (e.g., 'fund_recommendation.txt').
        **kwargs: Key-value pairs matching the ${variable} placeholders in the template.
        
    Returns:
        str: The fully substituted prompt string.
        
    Raises:
        FileNotFoundError: If the prompt file is not found.
        KeyError: If a required placeholder is missing in kwargs.
    """
    file_path = os.path.join(PROMPTS_DIR, filename)
    
    if not os.path.exists(file_path):
        error_msg = f"Prompt file not found: {file_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        template = Template(content)
        # safe_substitute could be used if we want to ignore missing keys, 
        # but strict substitute is better for ensuring prompt correctness.
        return template.substitute(**kwargs)
        
    except KeyError as e:
        logger.error(f"Missing variable for prompt template '{filename}': {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading prompt '{filename}': {e}")
        raise
