from sqlalchemy.orm import Session
from app.models.mutual_funds import SIPTransaction, SIPInstallments, SIPSchedule, MutualFundSchemes
from typing import List, Dict, Any, Optional

class PortfolioService:
    def get_aggregated_portfolio(self, db: Session, user_id: str) -> List[Dict[str, Any]]:
        """
        Fetch & aggregate user's mutual fund portfolio.
        """
        # Fetch raw MF rows
        rows = (
            db.query(
                SIPTransaction.scheme_code,
                MutualFundSchemes.scheme_name,
                SIPTransaction.amount.label("sip_amount"),
                SIPSchedule.total_invested_amount,
                SIPSchedule.total_units_allocated, 
            )
            .join(SIPSchedule, SIPSchedule.sip_id == SIPTransaction.id)
            .outerjoin(SIPInstallments, SIPInstallments.sip_id == SIPTransaction.id)
            .join(MutualFundSchemes, MutualFundSchemes.scheme_code == SIPTransaction.scheme_code)
            .filter(SIPTransaction.user_id == user_id)
            .filter(SIPSchedule.total_invested_amount.isnot(None))
            .all()
        )

        if not rows:
            return []

        # Aggregate by scheme_code
        portfolio = {}

        for row in rows:
            sc = row.scheme_code

            if sc not in portfolio:
                portfolio[sc] = {
                    "scheme_code": sc,
                    "scheme_name": row.scheme_name,
                    "total_invested_amount": 0.0,
                    "total_units": 0.0,
                    "sip_amounts": [],
                }

            # Aggregation
            portfolio[sc]["total_invested_amount"] += float(row.total_invested_amount or 0)
            portfolio[sc]["total_units"] += float(row.total_units_allocated or 0)

            # SIP collection
            if row.sip_amount:
                portfolio[sc]["sip_amounts"].append(float(row.sip_amount))

        # Build final aggregated list
        final_list = []
        for sc, data in portfolio.items():
            avg_sip = (
                sum(data["sip_amounts"]) / len(data["sip_amounts"])
                if data["sip_amounts"] else None
            )

            final_list.append({
                "scheme_code": sc,
                "scheme_name": data["scheme_name"],
                "total_invested_amount": round(data["total_invested_amount"], 2),
                "total_units": round(data["total_units"], 4),
                "avg_sip_amount": round(avg_sip, 2) if avg_sip else None,
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
        Fetch all distinct user IDs from the transactions table.
        """
        rows = db.query(SIPTransaction.user_id).distinct().all()
        return [r[0] for r in rows]

portfolio_service = PortfolioService()
