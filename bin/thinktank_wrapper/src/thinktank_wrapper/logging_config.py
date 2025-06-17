"""Logging configuration module for thinktank-wrapper.

This module provides functionality for configuring structured logging
with appropriate formats, handlers, and correlation IDs.
"""

import json
import logging
import sys
import uuid
from typing import Any, Dict, Optional


class StructuredLogFormatter(logging.Formatter):
    """Custom formatter for structured JSON logs.
    
    This formatter outputs logs as JSON objects with consistent fields,
    including a correlation ID for tracing requests.
    """
    
    def __init__(self, correlation_id: Optional[str] = None):
        """Initialize the formatter with an optional correlation ID.
        
        Args:
            correlation_id: A correlation ID to include in all log records.
                If not provided, a new UUID will be generated.
        """
        super().__init__()
        self.correlation_id = correlation_id or str(uuid.uuid4())
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON object.
        
        Args:
            record: The log record to format.
            
        Returns:
            A JSON string representation of the log record.
        """
        # Start with the basic log record attributes
        log_data: Dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "correlation_id": self.correlation_id,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)
        
        # Add any additional attributes from the record
        for key, value in record.__dict__.items():
            if key not in {
                "args", "asctime", "created", "exc_info", "exc_text",
                "filename", "funcName", "id", "levelname", "levelno",
                "lineno", "module", "msecs", "message", "msg", "name",
                "pathname", "process", "processName", "relativeCreated",
                "stack_info", "thread", "threadName",
            }:
                log_data[key] = value
        
        # Convert to JSON and return
        return json.dumps(log_data)


def setup_logging(
    level: int = logging.INFO,
    correlation_id: Optional[str] = None,
    structured: bool = True,
) -> str:
    """Set up logging with the specified configuration.
    
    Args:
        level: The logging level to use.
        correlation_id: A correlation ID to include in all log records.
            If not provided, a new UUID will be generated.
        structured: Whether to use structured JSON logging.
        
    Returns:
        The correlation ID that was used (either the one provided or a new one).
    """
    # Generate a correlation ID if one wasn't provided
    correlation_id = correlation_id or str(uuid.uuid4())
    
    # Create and configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create a handler for stdout
    handler = logging.StreamHandler(sys.stdout)
    
    # Set the correlation ID as a filter for all log records
    class CorrelationIDFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            record.correlation_id = correlation_id
            return True
    
    # Add the filter to the handler first
    handler.addFilter(CorrelationIDFilter())
    
    # Configure the formatter based on the structured flag
    if structured:
        formatter = StructuredLogFormatter(correlation_id)
    else:
        # For non-structured logging, skip the correlation ID in the format
        # to avoid clutter in the output
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"
        )
    
    # Set the formatter and add the handler to the root logger
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    # Log that logging has been set up
    logging.info("Logging initialized", extra={"correlation_id": correlation_id})
    
    return correlation_id