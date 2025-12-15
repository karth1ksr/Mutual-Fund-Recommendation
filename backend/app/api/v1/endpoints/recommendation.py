from fastapi import APIRouter, HTTPException
from app.db.mongo import mongo_db
from typing import Any

router = APIRouter()

@router.get("/recommendations/{user_id}", response_model=Any)
def read_recommendation(user_id: str):
    """
    Get existing recommendation for a user from MongoDB.
    """
    
    result = mongo_db.collection.find_one({"user_id": user_id}, {"_id": 0})
    if not result:
        raise HTTPException(status_code=404, detail="User recommendation not found")
    return result
