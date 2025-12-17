from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import AppError
import logging

logger = logging.getLogger(__name__)

async def app_exception_handler(request: Request, exc: AppError):
    """
    Handle custom AppErrors.
    """
    logger.error(f"AppError: {exc.message} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.__class__.__name__, "message": exc.message}},
    )

async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unhandled exceptions.
    """
    logger.error(f"Unhandled Exception: {str(exc)} - Path: {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "InternalServerError", "message": "An unexpected error occurred."}},
    )
