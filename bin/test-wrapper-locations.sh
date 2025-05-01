#!/usr/bin/env bash
# =============================================================================
# test-wrapper-locations.sh
# =============================================================================
# Tests thinktank-wrapper functionality from various locations
# Ensures the wrapper can be invoked properly regardless of the current directory

# Set script to exit immediately if any command fails
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

# Store the original directory
ORIGINAL_DIR=$(pwd)
CODEX_DIR="$HOME/Development/codex"
TEST_FILE="${CODEX_DIR}/bin/test-wrapper-locations-temp.md"

# Create a temporary test file
echo "# Test file for thinktank-wrapper location tests" > "$TEST_FILE"

# Function to run a test
run_test() {
    local test_num=$1
    local description=$2
    local command=$3
    
    echo -e "${BLUE}Test $test_num: $description${RESET}"
    echo "Directory: $(pwd)"
    echo "Command: $command"
    
    # Execute the command with dry-run to check command construction
    eval "$command"
    
    echo -e "${GREEN}✓ Test $test_num passed${RESET}"
    echo
}

# Clean up function
cleanup() {
    echo -e "${BLUE}Cleaning up...${RESET}"
    rm -f "$TEST_FILE"
    cd "$ORIGINAL_DIR"
    echo -e "${GREEN}Done!${RESET}"
}

# Register cleanup function to run on exit
trap cleanup EXIT

echo -e "${YELLOW}=======================================${RESET}"
echo -e "${YELLOW}   Testing wrapper from locations      ${RESET}"
echo -e "${YELLOW}=======================================${RESET}"
echo

# Test 1: Run from codex repository root
cd "$CODEX_DIR"
run_test 1 "Run from codex repository root" "bin/thinktank-wrapper --dry-run --model-set all \"$TEST_FILE\""

# Test 2: Run from bin directory
cd "$CODEX_DIR/bin"
run_test 2 "Run from bin directory" "./thinktank-wrapper --dry-run --model-set high_context \"$TEST_FILE\""

# Test 3: Run from home directory with absolute path
cd "$HOME"
run_test 3 "Run from home directory (absolute path)" "thinktank-wrapper --dry-run --include-glance \"$TEST_FILE\""

# Test 4: Run from home directory with relative path to test file
cd "$HOME"
run_test 4 "Run from home directory (relative path)" "thinktank-wrapper --dry-run --include-philosophy Development/codex/bin/test-wrapper-locations-temp.md"

# Test 5: Run from unrelated directory
cd "/tmp"
run_test 5 "Run from unrelated directory" "thinktank-wrapper --dry-run --include-glance --include-philosophy \"$TEST_FILE\""

# Test 6: Run with no arguments to test help display
cd "$HOME"
run_test 6 "Run with no arguments" "thinktank-wrapper --help | head -n 3"

echo -e "${GREEN}All tests completed successfully!${RESET}"
exit 0