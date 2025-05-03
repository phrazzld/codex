"""Executor module for thinktank-wrapper.

This module provides functionality for executing the thinktank command 
using subprocess, handling output streaming and error propagation.
"""

import logging
import shlex
import subprocess
from typing import List

logger = logging.getLogger(__name__)


class ThinktankNotFoundError(Exception):
    """Raised when the thinktank executable cannot be found."""
    pass


class ThinktankExecutionError(Exception):
    """Raised when an error occurs during execution of thinktank."""
    def __init__(self, command: List[str], return_code: int, stderr: str = ""):
        command_str = " ".join(shlex.quote(arg) for arg in command)
        message = (
            f"Command '{command_str}' failed with return code {return_code}"
        )
        if stderr:
            message += f"\\nError output: {stderr}"
        super().__init__(message)
        self.command = command
        self.return_code = return_code
        self.stderr = stderr


def run_command(cmd: List[str], dry_run: bool = False) -> int:
    """Run the thinktank command.
    
    Args:
        cmd: The command to run, as a list of strings.
        dry_run: If True, print the command instead of executing it.
        
    Returns:
        The return code from the command.
        
    Raises:
        ThinktankNotFoundError: If the thinktank executable cannot be found.
        ThinktankExecutionError: If an error occurs during execution.
    """
    if dry_run:
        # Print the command as a shell-escaped string
        command_str = " ".join(shlex.quote(arg) for arg in cmd)
        print(f"Would execute: {command_str}")
        return 0
    
    logger.info(f"Executing thinktank command with {len(cmd)} arguments")
    try:
        # Run the command, streaming output to stdout/stderr
        result = subprocess.run(
            cmd,
            check=False,  # Don't raise an exception on non-zero return code
            shell=False,  # Avoid shell injection vulnerabilities
            text=True,
            stdout=None,  # Use parent process stdout
            stderr=None,  # Use parent process stderr
        )
        
        # Log the return code
        if result.returncode == 0:
            logger.info(f"Command succeeded with return code {result.returncode}")
        else:
            logger.error(f"Command failed with return code {result.returncode}")
        
        return result.returncode
    except FileNotFoundError as e:
        # This happens if the thinktank executable is not in the PATH
        logger.error("Thinktank executable not found in PATH")
        raise ThinktankNotFoundError(
            "Thinktank executable not found in PATH. "
            "Make sure thinktank is installed and available in your PATH."
        ) from e
    except subprocess.SubprocessError as e:
        # This happens for other subprocess-related errors
        logger.error(f"Error executing thinktank command: {e}")
        raise ThinktankExecutionError(cmd, -1, str(e)) from e