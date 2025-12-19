import sys
import os
import logging
from typing import Optional

# Ensure the app is in the python path
# Adjusted path since this file is in backend/testing/
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app.db.session import SessionLocal
from app.db.mongo import mongo_db
from app.services.portfolio import portfolio_service
from app.services.recommendation import recommendation_service
from app.utils.helpers import pretty_print

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SingleUserTest")

def process_single_user(user_id: str):
    db = SessionLocal()
    try:
        mongo_db.connect()
        
        logger.info(f"Running recommendation workflow for user: {user_id}")
        
        try:
            # 1. Get Portfolio
            portfolio = portfolio_service.get_aggregated_portfolio(db, user_id)
            if not portfolio:
                logger.warning(f"No portfolio found for user {user_id}. Cannot proceed.")
                return

            logger.info(f"Fetched portfolio with {len(portfolio)} funds.")

            # 2. Calculate Budget
            sip_amounts = [p.get("sip_amount") for p in portfolio if p.get("sip_amount")]
            invested_amounts = [p.get("total_invested_amount") for p in portfolio if p.get("total_invested_amount")]

            if sip_amounts:
                budget = round(sum(sip_amounts) / len(sip_amounts))
            elif invested_amounts:
                budget = round(sum(invested_amounts) / len(invested_amounts))
            else:
                budget = 0
            
            logger.info(f"Calculated budget: {budget}")

            fund_names = [p["scheme_name"] for p in portfolio]

            # 3. Run Pipeline
            result = recommendation_service.run_pipeline(fund_names, user_id=user_id)
            
            # 4. Save to Mongo
            mongo_db.collection.update_one(
                {"user_id": user_id},
                {"$set": {
                    "user_id": user_id,
                    "budget": budget,
                    "recommendation": result
                }},
                upsert=True
            )
            logger.info(f"Saved recommendations for user {user_id}")
            pretty_print(result)

        except Exception as e:
            logger.error(f"Error processing user {user_id}: {e}", exc_info=True)

    finally:
        db.close()
        mongo_db.close()

def main():
    db = SessionLocal()
    target_user_id = None
    
    try:
        # Check if user provided an ID argument
        if len(sys.argv) > 1:
            target_user_id = sys.argv[1]
        else:
            # List available users
            all_users = portfolio_service.get_all_user_ids(db)
            if not all_users:
                logger.error("No users found in database.")
                return
            
            print("Available Users:", ", ".join(all_users[:10]))
            target_user_id = input("Enter User ID to process (leave blank for first one): ").strip()
            
            if not target_user_id:
                target_user_id = all_users[0]
                
        process_single_user(target_user_id)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
