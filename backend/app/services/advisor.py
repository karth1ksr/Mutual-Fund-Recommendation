import json
from google import genai
from google.genai import types
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.utils.common import extract_json
from app.utils.prompt_loader import load_prompt
from app.schemas.fund import FundDetails
import logging

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
import logging

logger = logging.getLogger(__name__)

class AdvisorService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash-lite"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def recommend_fund_names(self, user_fund_details: List[dict], user_feedback: List[dict] = [], user_budget: float = 0) -> Dict[str, Any]:
        """
        Given user fund details, feedback and budget, recommend 5 fund NAMES.
        Returns dict with keys: 'feedback_classification', 'recommendations'
        """
        prompt = load_prompt(
            "fund_recommendation.txt",
            user_fund_details_json=json.dumps(user_fund_details, default=str),
            user_feedback_json=json.dumps(user_feedback, default=str),
            user_budget=str(user_budget)
        )
        try:
            resp = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            clean = extract_json(resp.text.strip())
            return clean if clean else {"feedback_classification": [], "recommendations": []}
        except Exception as e:
            logger.error(f"Gemini recommendation ERROR: {e}")
            raise e  # Reraise to trigger retry

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def enrich_recommendations(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds pros, cons, and ranking to final funds.
        """
        prompt = load_prompt(
            "fund_enrichment.txt",
            payload_json=json.dumps(payload, default=str)
        )
        try:
            resp = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            clean = extract_json(resp.text.strip())
            return clean
        except Exception as e:
            logger.error(f"Gemini enrichment ERROR: {e}")
            raise e

advisor_service = AdvisorService()
