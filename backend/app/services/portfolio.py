from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.mutual_funds import SIPTransaction, SIPInstallments, SIPSchedule, MutualFundSchemes
from typing import List, Dict, Any, Optional

class PortfolioService:
    # PRE-CONFIGURATION: Set your table name here
    TABLE_NAME = "portfolio_view" 

    def get_aggregated_portfolio(self, db: Session, user_id: str) -> List[Dict[str, Any]]:
        """
        Fetch & aggregate user's mutual fund portfolio.
        Adjusted to use ONLY the fields from the new local MySQL connection:
        - user_id
        - scheme_name
        - total_invested_amount
        - total_units
        - avg_sip_amount
        """
        # Fetch raw MF rows using raw SQL to match the new local DB schema fields
        # Using the defined TABLE_NAME
        query = text(f"""
            SELECT 
                scheme_name, 
                total_invested_amount, 
                total_units, 
                avg_sip_amount 
            FROM {self.TABLE_NAME} 
            WHERE user_id = :user_id
        """)
        
        # Execute the query
        result = db.execute(query, {"user_id": user_id})
        
        # Aggregate by scheme_name (since scheme_code is not available)
        portfolio = {}

        for row in result:
            # Access fields by attribute
            s_name = row.scheme_name
            t_inv = float(row.total_invested_amount or 0)
            t_units = float(row.total_units or 0)
            avg_sip = float(row.avg_sip_amount or 0)

            if s_name not in portfolio:
                portfolio[s_name] = {
                    "scheme_code": None, # Not available in new source
                    "scheme_name": s_name,
                    "total_invested_amount": 0.0,
                    "total_units": 0.0,
                    "avg_sip_amounts": [],
                }

            # Aggregation: Sum totals, collect averages from rows (in case of duplicates)
            portfolio[s_name]["total_invested_amount"] += t_inv
            portfolio[s_name]["total_units"] += t_units
            
            if avg_sip:
                portfolio[s_name]["avg_sip_amounts"].append(avg_sip)

        # Build final aggregated list
        final_list = []
        for s_name, data in portfolio.items():
            # Calculate average of SIP amounts if multiple rows exist
            sips = data["avg_sip_amounts"]
            final_avg_sip = (sum(sips) / len(sips)) if sips else None

            final_list.append({
                "scheme_code": data["scheme_code"],
                "scheme_name": data["scheme_name"],
                "total_invested_amount": round(data["total_invested_amount"], 2),
                "total_units": round(data["total_units"], 4),
                "avg_sip_amount": round(final_avg_sip, 2) if final_avg_sip else None,
            })

        # Select only top 3 if more than 3 funds
        if len(final_list) > 3:
            final_list = sorted(
                final_list,
                key=lambda x: x["total_invested_amount"],
                reverse=True
            )[:3]

        return final_list

    def get_all_user_ids(self, db: Session) -> List[str]:
        """
        Fetch all distinct user IDs from the new source.
        """
        query = text(f"SELECT DISTINCT user_id FROM {self.TABLE_NAME}")
        rows = db.execute(query).fetchall()
        return [r.user_id for r in rows]

portfolio_service = PortfolioService()
