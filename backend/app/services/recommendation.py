from typing import List, Dict, Any, Tuple
from app.services.market_data import market_data_service
from app.services.advisor import advisor_service
from app.utils.timer import Timer
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    def run_pipeline(self, fund_names: List[str]) -> Tuple[Dict[str, Any], Dict[str, float]]:
        """
        Orchestrates the recommendation flow:
        1. Fetch details of user's current funds from Perplexity.
        2. Get recommendations from Gemini (Funds names).
        3. Fetch details of recommended funds from Perplexity.
        4. Enrich and Rank with Gemini.
        """
        timing = {}
        
        # 1. Fetch user fund details
        with Timer() as t1:
            user_fund_details = []
            for name in fund_names:
                details = market_data_service.fetch_fund_details(name)
                if details:
                    # Convert Pydantic model to dict for JSON serialization later
                    user_fund_details.append(details.dict())
        timing["fetch_user_fund_seconds"] = round(t1.elapsed, 3)

        # 2. Get Recommended Names
        with Timer() as t2:
            name_response = advisor_service.recommend_fund_names(user_fund_details)
            recommended_names = name_response.get("recommended_fund_names", [])
        timing["gemini_recommend_seconds"] = round(t2.elapsed, 3)

        # 3. Fetch details for recommended funds
        with Timer() as t3:
            recommended_full = []
            for name in recommended_names:
                details = market_data_service.fetch_fund_details(name)
                if details:
                    recommended_full.append(details.dict())
        timing["fetch_recommended_details_seconds"] = round(t3.elapsed, 3)

        # 4. Enrich and Rank
        payload = {
            "user_fund_details": user_fund_details,
            "recommended_funds": recommended_full
        }

        with Timer() as t4:
            final_result = advisor_service.enrich_recommendations(payload)
        timing["gemini_enrich_seconds"] = round(t4.elapsed, 3)
        
        timing["total_seconds"] = round(sum(timing.values()), 3)
        
        return final_result, timing

recommendation_service = RecommendationService()
