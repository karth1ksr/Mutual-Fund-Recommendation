import json
from google import genai
from google.genai import types
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.utils.common import extract_json
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
    def recommend_fund_names(self, user_fund_details: List[dict]) -> Dict[str, List[str]]:
        """
        Given user fund details, recommend 5 fund NAMES only.
        """
        prompt = f"""
You are a mutual fund expert.

Given these user fund holdings:

{json.dumps(user_fund_details, default=str)}

Recommend EXACTLY 5 mutual funds for diversification.
Return ONLY their names.
Do NOT return URLs, NAV, AUM, returns, risk or descriptions.

Strict JSON format:
{{
  "recommended_fund_names": []
}}
"""
        try:
            resp = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            clean = extract_json(resp.text.strip())
            return clean if clean else {"recommended_fund_names": []}
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
        prompt = f"""
You are a mutual fund analyst.

Analyze the following JSON:
{json.dumps(payload, default=str)}

For EACH recommended fund add:
- pros
- cons

Then produce a RANKING (best to worst) based on:
- long-term return potential
- risk-adjusted performance
- stability
- rank only for top 3 or top 5 (if available)

Do not return the fund if you don't have all the required details and urls.

RETURN STRICT JSON ONLY:
{{
  "user_fund_details": [...],
  "recommendations": [...],
  "ranking": ["Fund1", "Fund2", "Fund3",..]
}}
"""
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
