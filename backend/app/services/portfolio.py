from sqlalchemy.orm import Session
from app.models.mutual_funds import PortfolioView
from typing import List, Dict, Any, Optional

class PortfolioService:
    def get_aggregated_portfolio(self, db: Session, user_id: str) -> List[Dict[str, Any]]:
        """
        Fetch & aggregate user's mutual fund portfolio.
        Adjusted to use ONLY the fields from the new local MySQL connection via SQLAlchemy ORM:
        - user_id
        - scheme_name
        - total_invested_amount
        - total_units
        - avg_sip_amount
        """
        # Fetch rows using SQLAlchemy ORM
        rows = db.query(PortfolioView).filter(PortfolioView.user_id == user_id).all()
        
        # Aggregate by scheme_name (since scheme_code is not available)
        portfolio = {}

        for row in rows:
            # Access fields by attribute on the ORM object
            s_name = row.scheme_name
            t_inv = float(row.total_invested_amount or 0)
            t_units = float(row.total_units or 0)
            sip_amt = float(row.sip_amount or 0)

            if s_name not in portfolio:
                portfolio[s_name] = {
                    "scheme_name": s_name,
                    "total_invested_amount": 0.0,
                    "total_units": 0.0,
                    "sip_amounts": [],
                }

            # Aggregation: Sum totals, collect sip amounts for averaging
            portfolio[s_name]["total_invested_amount"] += t_inv
            portfolio[s_name]["total_units"] += t_units
            
            if sip_amt:
                portfolio[s_name]["sip_amounts"].append(sip_amt)

        # Build final aggregated list
        final_list = []
        for s_name, data in portfolio.items():
            # Calculate average of SIP amounts if multiple rows exist
            sips = data["sip_amounts"]
            final_avg_sip = (sum(sips) / len(sips)) if sips else None

            final_list.append({
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
        rows = db.query(PortfolioView.user_id).distinct().all()
        return [r[0] for r in rows]

portfolio_service = PortfolioService()
