"""
Logger module providing standardized logging functionality across Autonoma.
"""

import os
import sys
from datetime import datetime
from loguru import logger

# Default log configuration
DEFAULT_LOG_LEVEL = "INFO"
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

def get_logger(name="autonoma"):
    """
    Configure and return a logger instance with appropriate settings.

    Args:
        name (str): Name for the logger, used in log messages

    Returns:
        logger: Configured logger instance
    """
    # Clear existing handlers
    logger.remove()

    # Determine log level from environment or use default
    log_level = os.environ.get("AUTONOMA_LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()

    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"{name}_{timestamp}.log")

    # Add handlers for both console and file
    logger.add(sys.stderr, level=log_level, format=LOG_FORMAT)
    logger.add(log_file, level=log_level, format=LOG_FORMAT, rotation="100 MB", retention="1 week")

    # Return configured logger
    logger.info(f"Logger initialized for {name} at level {log_level}")
    return logger
