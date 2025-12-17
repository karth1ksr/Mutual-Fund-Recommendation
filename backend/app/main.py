import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.db.mongo import mongo_db
from app.core.logging import setup_logging

from app.core.exceptions import AppError
from app.core.handlers import app_exception_handler, general_exception_handler

# Setup logging before app creation
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Register Exception Handlers
app.add_exception_handler(AppError, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mutualfundrecommendation.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    logger.info("Starting up Mutual Fund Recommendation Engine...")
    mongo_db.connect()
    logger.info("Database connection established.")

@app.on_event("shutdown")
def shutdown_db_client():
    logger.info("Shutting down Mutual Fund Recommendation Engine...")
    mongo_db.close()
    logger.info("Database connection closed.")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Mutual Fund Recommendation Engine API is running"}
