from typing import List, Dict, Any, Tuple
from datetime import datetime
from app.services.market_data import market_data_service
from app.services.advisor import advisor_service
from app.utils.timer import Timer
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    def run_pipeline(self, fund_names: List[str]) -> Dict[str, Any]:
        """
        Orchestrates the recommendation flow:
        1. Fetch details of user's current funds from Perplexity.
        2. Get recommendations from Gemini (Funds names).
        3. Fetch details of recommended funds from Perplexity.
        4. Enrich and Rank with Gemini.
        """
        timing = {}
        start_time = datetime.now()
        logger.info(f"Recommendation pipeline started at {start_time.isoformat()}")
        
        # 1. Fetch user fund details
        with Timer() as t1:
            user_fund_details = []
            for name in fund_names:
                try:
                    details = market_data_service.fetch_fund_details(name)
                    if details:
                        # Convert Pydantic model to dict for JSON serialization later
                        user_fund_details.append(details.dict())
                except Exception as e:
                    logger.warning(f"Failed to fetch details for {name} after retries: {e}")
                    # Continue pipeline even if one fund fails
        timing["fetch_user_fund_seconds"] = round(t1.elapsed, 3)

        # 2. Get Recommended Names
        with Timer() as t2:
            try:
                name_response = advisor_service.recommend_fund_names(user_fund_details)
                recommended_names = name_response.get("recommended_fund_names", [])
            except Exception as e:
                logger.error(f"Gemini recommendation failed after retries: {e}")
                recommended_names = []
                # You might want to raise an ExternalServiceError here if this is critical
        timing["gemini_recommend_seconds"] = round(t2.elapsed, 3)

        # 3. Fetch details for recommended funds
        with Timer() as t3:
            recommended_full = []
            for name in recommended_names:
                try:
                    details = market_data_service.fetch_fund_details(name)
                    if details:
                        recommended_full.append(details.dict())
                except Exception as e:
                     logger.warning(f"Failed to fetch details for recommended fund {name}: {e}")
        timing["fetch_recommended_details_seconds"] = round(t3.elapsed, 3)

        # 4. Enrich and Rank
        payload = {
            "user_fund_details": user_fund_details,
            "recommended_funds": recommended_full
        }

        with Timer() as t4:
            try:
                final_result = advisor_service.enrich_recommendations(payload)
            except Exception as e:
                logger.error(f"Gemini enrichment failed after retries: {e}")
                final_result = None
        timing["gemini_enrich_seconds"] = round(t4.elapsed, 3)
        
        
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        timing["total_seconds"] = round(total_duration, 3)
        
        logger.info(f"Recommendation pipeline completed at {end_time.isoformat()}")
        logger.info(f"Pipeline Execution Timing: {timing}")
        
        # Sanitize result to ensure no timing metadata leaks into the DB
        if final_result and isinstance(final_result, dict):
            # Explicitly remove typical timing keys if they somehow appeared
            for key in ["timestamp", "generated_at", "execution_time", "timing"]:
                final_result.pop(key, None)

        return final_result

recommendation_service = RecommendationService()
