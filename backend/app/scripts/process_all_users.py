import sys
import os

# Ensure the app is in the python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app.db.session import SessionLocal
from app.db.mongo import mongo_db
from app.services.portfolio import portfolio_service
from app.services.recommendation import recommendation_service
from app.utils.helpers import pretty_print
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BatchProcessor")

def main():
    db = SessionLocal()
    try:
        mongo_db.connect()
        
        all_users = portfolio_service.get_all_user_ids(db)
        logger.info(f"Found {len(all_users)} users. Running pipeline...")

        for user_id in all_users:
            logger.info(f"Running recommendation workflow for user: {user_id}")
            
            try:
                # 1. Get Portfolio
                portfolio = portfolio_service.get_aggregated_portfolio(db, user_id)
                if not portfolio:
                    logger.warning(f"No portfolio found for user {user_id}, skipping.")
                    continue

                # 2. Calculate Budget (Logic duplicated from API, ideally moved to service but fine here for script)
                sip_amounts = [p.get("avg_sip_amount") for p in portfolio if p.get("avg_sip_amount")]
                invested_amounts = [p.get("total_invested_amount") for p in portfolio if p.get("total_invested_amount")]

                if sip_amounts:
                    budget = round(sum(sip_amounts) / len(sip_amounts))
                elif invested_amounts:
                    budget = round(sum(invested_amounts) / len(invested_amounts))
                else:
                    budget = 0

                fund_names = [p["scheme_name"] for p in portfolio]

                # 3. Run Pipeline
                result = recommendation_service.run_pipeline(fund_names)
                
                # 4. Save to Mongo
                mongo_db.collection.update_one(
                    {"user_id": user_id},
                    {"$set": {
                        "user_id": user_id,
                        "budget": budget,
                        "user_id": user_id,
                        "budget": budget,
                        "recommendation": result
                    }},
                    upsert=True
                )
                logger.info(f"Saved for user {user_id}")

            except Exception as e:
                logger.error(f"Error processing user {user_id}: {e}")

    finally:
        db.close()
        mongo_db.close()

if __name__ == "__main__":
    main()
