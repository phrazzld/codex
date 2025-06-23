#!/bin/bash
# Claude usage window trigger with enhanced logging and Max plan authentication
# Logs to both system log and dedicated logfile with detailed output

LOGFILE="/Users/phaedrus/Development/codex/logs/claude-trigger.log"
mkdir -p "$(dirname "$LOGFILE")"

log_message() {
    local message="$1"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "[$timestamp] $message" | tee -a "$LOGFILE"
    echo "$timestamp: $message" | logger -t claude-trigger
}

log_message "=== Starting Claude usage window trigger ==="

# Ensure we're using Max plan authentication
# Remove any API key environment variables that might interfere
unset ANTHROPIC_API_KEY

# Try various approaches to ensure Max plan usage
log_message "Attempting to trigger Claude Code with Max plan authentication..."

# Method 1: Standard print mode
claude -p "hello" >> "$LOGFILE" 2>&1
exit_code=$?

if [ $exit_code -eq 0 ]; then
    log_message "SUCCESS: Claude Code executed successfully (exit code $exit_code)"
    log_message "Usage window should now be active for your Max plan"
else
    log_message "FAILED: Claude Code failed with exit code $exit_code"
    
    # Method 2: Try with explicit model selection
    log_message "Retrying with explicit model selection..."
    claude --model sonnet -p "hello" >> "$LOGFILE" 2>&1
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_message "SUCCESS: Claude Code executed with explicit model (exit code $exit_code)"
    else
        log_message "FAILED: Both attempts failed. Manual intervention may be required."
        log_message "Try running 'claude /logout' then 'claude /login' interactively"
        log_message "When prompted, deny API key usage to ensure Max plan authentication"
    fi
fi

log_message "=== Claude trigger complete ==="