from fastapi import HTTPException, status

class AppError(Exception):
    """Base class for all application errors."""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ExternalServiceError(AppError):
    """Raised when an external service (Gemini/Perplexity) fails."""
    def __init__(self, service_name: str, detail: str):
        super().__init__(
            message=f"External service '{service_name}' failed: {detail}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

class DatabaseError(AppError):
    """Raised when a database operation fails."""
    def __init__(self, detail: str):
        super().__init__(
            message=f"Database error: {detail}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class DataNotFoundError(AppError):
    """Raised when expected data is missing."""
    def __init__(self, item_name: str):
        super().__init__(
            message=f"{item_name} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
