from fastapi import APIRouter, HTTPException, Body
from app.db.mongo import mongo_db
from app.services.recommendation import recommendation_service
from pydantic import BaseModel
from typing import Any

router = APIRouter()

class UserFeedbackRequest(BaseModel):
    user_id: str
    feedback: str

@router.get("/recommendations/{user_id}", response_model=Any)
def read_recommendation(user_id: str):
    """
    Get existing recommendation for a user from MongoDB.
    """
    
    result = mongo_db.collection.find_one({"user_id": user_id}, {"_id": 0})
    if not result:
        raise HTTPException(status_code=404, detail="User recommendation not found")
    return result

@router.post("/feedback")
def submit_feedback(request: UserFeedbackRequest):
    """
    Submit user feedback for future recommendations.
    """
    try:
        recommendation_service.save_user_feedback(request.user_id, request.feedback)
        return {"message": "Feedback received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
