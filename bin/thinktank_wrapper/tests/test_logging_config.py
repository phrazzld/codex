"""Tests for the logging_config module."""

import json
import logging
import re
import uuid
from io import StringIO
from unittest.mock import patch

import pytest

from thinktank_wrapper import logging_config


# Note: Using pytest's built-in capfd fixture for log capture instead of custom fixture


def test_structured_log_formatter():
    """Test that StructuredLogFormatter correctly formats log records."""
    # Set up
    correlation_id = str(uuid.uuid4())
    formatter = logging_config.StructuredLogFormatter(correlation_id)
    
    # Create a log record
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=123,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    
    # Format the record
    formatted = formatter.format(record)
    
    # Parse the JSON
    parsed = json.loads(formatted)
    
    # Assert the basic fields are present
    assert parsed["timestamp"]
    assert parsed["level"] == "INFO"
    assert parsed["name"] == "test_logger"
    assert parsed["message"] == "Test message"
    assert parsed["correlation_id"] == correlation_id


def test_structured_log_formatter_with_exception():
    """Test that StructuredLogFormatter correctly formats log records with exceptions."""
    # Set up
    formatter = logging_config.StructuredLogFormatter()
    
    # Create a log record with an exception
    try:
        raise ValueError("Test exception")
    except ValueError:
        record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname="test_path",
            lineno=123,
            msg="Error occurred",
            args=(),
            exc_info=logging.sys.exc_info(),
        )
    
    # Format the record
    formatted = formatter.format(record)
    
    # Parse the JSON
    parsed = json.loads(formatted)
    
    # Assert the exception info is present
    assert "exc_info" in parsed
    assert "ValueError: Test exception" in parsed["exc_info"]


def test_structured_log_formatter_with_extra_fields():
    """Test that StructuredLogFormatter includes extra fields in the log record."""
    # Set up
    formatter = logging_config.StructuredLogFormatter()
    
    # Create a log record with extra fields
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path",
        lineno=123,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    record.custom_field = "custom value"
    
    # Format the record
    formatted = formatter.format(record)
    
    # Parse the JSON
    parsed = json.loads(formatted)
    
    # Assert the extra field is present
    assert parsed["custom_field"] == "custom value"


def test_setup_logging_structured(capfd):
    """Test that setup_logging correctly configures structured logging."""
    # Call the function
    correlation_id = logging_config.setup_logging(
        level=logging.DEBUG, structured=True
    )
    
    # Log a message
    logging.info("Test message")
    
    # Get the log output
    captured = capfd.readouterr()
    log_output = captured.out
    
    # Assert the log output is in JSON format
    assert log_output.startswith("{")
    assert log_output.endswith("}\n")
    
    # Parse the last JSON line (our test message)
    lines = log_output.strip().split('\n')
    last_line = lines[-1]
    parsed = json.loads(last_line)
    
    # Assert the fields are present
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "Test message"
    assert parsed["correlation_id"] == correlation_id


def test_setup_logging_unstructured(capfd):
    """Test that setup_logging correctly configures unstructured logging."""
    # Call the function
    correlation_id = logging_config.setup_logging(
        level=logging.DEBUG, structured=False
    )
    
    # Log a message
    logging.info("Test message")
    
    # Get the log output
    captured = capfd.readouterr()
    log_output = captured.out
    
    # Assert the log output is not in JSON format
    assert not log_output.startswith("{")
    
    # Assert the message is present
    assert "Test message" in log_output
    
    # Assert the correlation ID is present
    assert correlation_id in log_output


def test_setup_logging_with_correlation_id():
    """Test that setup_logging uses the provided correlation ID."""
    # Set up
    correlation_id = str(uuid.uuid4())
    
    # Call the function
    returned_id = logging_config.setup_logging(correlation_id=correlation_id)
    
    # Assert the returned correlation ID matches the provided one
    assert returned_id == correlation_id


def test_setup_logging_generates_correlation_id():
    """Test that setup_logging generates a correlation ID if none is provided."""
    # Mock uuid.uuid4 to return a known UUID
    mock_uuid = "12345678-1234-5678-1234-567812345678"
    with patch("uuid.uuid4") as mock_uuid4:
        mock_uuid4.return_value = uuid.UUID(mock_uuid)
        
        # Call the function
        correlation_id = logging_config.setup_logging()
    
    # Assert the correlation ID is the expected one
    assert correlation_id == mock_uuid


def test_correlation_id_filter():
    """Test that the CorrelationIDFilter adds the correlation ID to log records."""
    # Set up logging with a correlation ID
    correlation_id = str(uuid.uuid4())
    logging_config.setup_logging(correlation_id=correlation_id)
    
    # Create a StringIO to capture the log output
    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)
    formatter = logging.Formatter("%(correlation_id)s: %(message)s")
    handler.setFormatter(formatter)
    
    # Add the handler to the root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    
    # Log a message
    logging.info("Test message")
    
    # Get the log output
    log_output = log_capture.getvalue()
    
    # Assert the correlation ID is present
    assert correlation_id in log_output