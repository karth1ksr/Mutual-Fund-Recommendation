from fastapi import APIRouter
from app.api.v1.endpoints import recommendation

api_router = APIRouter()
api_router.include_router(recommendation.router, prefix="/mf", tags=["mutual-funds"])
