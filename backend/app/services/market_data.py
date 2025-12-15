import requests
from typing import Optional
from app.core.config import settings
from app.schemas.fund import FundDetails
from app.utils.common import extract_json
import logging

logger = logging.getLogger(__name__)

class MarketDataService:
    BASE_URL = "https://api.perplexity.ai/chat/completions"
    
    def fetch_fund_details(self, fund_name: str) -> Optional[FundDetails]:
        """
        Fetch accurate, real fund details for ONE fund using Perplexity.
        """
        prompt = f"""
Strictly return JSON. No commentary.
You should fetch details only from working reliable websites. DO NOT USE LLM.

Fetch accurate real time mutual fund data for: "{fund_name}"

Return ONLY:
- name
- category
- nav
- aum
- returns {{1Y, 3Y, 5Y}}
- risk_level
- resource_url

Ignore the fund if you can't find any reliable data for all the fields.

JSON FORMAT:
{{
  "name": "",
  "category": "",
  "nav": "",
  "aum": "",
  "returns": {{
    "1Y": "",
    "3Y": "",
    "5Y": ""
  }},
  "risk_level": "",
  "resource_url": ""
}}
"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
        }

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "Return ONLY JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 800
        }

        try:
            res = requests.post(self.BASE_URL, headers=headers, json=payload, timeout=40)
            res.raise_for_status()
            
            content = res.json()["choices"][0]["message"]["content"].strip()
            data = extract_json(content)
            
            if data:
                return FundDetails(**data)
            return None

        except Exception as e:
            logger.error(f"Perplexity ERROR for {fund_name}: {e}")
            return None

market_data_service = MarketDataService()
