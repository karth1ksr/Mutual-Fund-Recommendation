import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Configure logging for the application.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Basic configuration with the default level coming from settings
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=log_format,
        datefmt=date_format,
        stream=sys.stdout,
    )

    # Set specific levels for third-party libraries if needed to reduce noise
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    
    # Ensure our app's loggers are at the requested level
    root_logger = logging.getLogger("app")
    root_logger.setLevel(settings.LOG_LEVEL)
