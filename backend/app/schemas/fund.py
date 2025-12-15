from pydantic import BaseModel
from typing import Optional, Dict, List, Any

class FundReturns(BaseModel):
    OneY: Optional[str] = None
    ThreeY: Optional[str] = None
    FiveY: Optional[str] = None
    
    class Config:
        populate_by_name = True

class FundDetails(BaseModel):
    name: str
    category: Optional[str] = None
    nav: Optional[str] = None
    aum: Optional[str] = None
    returns: Optional[Dict[str, str]] = None
    risk_level: Optional[str] = None
    resource_url: Optional[str] = None
    
    # Enriched fields
    pros: Optional[List[str]] = None
    cons: Optional[List[str]] = None

class RecommendationResponse(BaseModel):
    user_fund_details: List[FundDetails]
    recommended_funds: List[FundDetails]
    ranking: Optional[List[str]] = None
