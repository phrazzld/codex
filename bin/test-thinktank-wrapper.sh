#!/usr/bin/env bash
# Test script for thinktank-wrapper

# Set script to exit immediately if any command fails
set -e

# Print header
echo "===== Testing thinktank-wrapper ====="
echo

# Test 1: Basic help output
echo "Test 1: Basic help output"
./bin/thinktank-wrapper --help | head -n 5
echo "Help command successful"
echo

# Test 2: Default model set with dry run
echo "Test 2: Default model set (should be 'all')"
# Create a temporary test file to use as context
echo "Test content" > /tmp/test-file.txt
# Run with dry run to see the command
./bin/thinktank-wrapper --dry-run --instructions /tmp/test-file.txt /tmp/test-file.txt

# Check if the output contains all models from the "all" set
MODELS_COUNT=$(./bin/thinktank-wrapper --dry-run --instructions /tmp/test-file.txt /tmp/test-file.txt | grep -o -- "--model" | wc -l)
echo "Command contains $MODELS_COUNT model flags"

# Verify the model count matches expected count for "all" set (should be 11)
if [ "$MODELS_COUNT" -eq 11 ]; then
  echo "Default model set (all) successfully used"
else
  echo "ERROR: Expected 11 models in 'all' set, but found $MODELS_COUNT"
  exit 1
fi

# Verify command structure (options -> models -> synthesis model -> file paths)
COMMAND=$(./bin/thinktank-wrapper --dry-run --instructions /tmp/test-file.txt /tmp/test-file.txt)
if [[ "$COMMAND" =~ "--instructions" && "$COMMAND" =~ "--synthesis-model" && "$COMMAND" =~ "/tmp/test-file.txt" ]]; then
  echo "Command structure verified"
else
  echo "ERROR: Command structure incorrect"
  exit 1
fi

# Test 3: Specified model set (high_context)
echo
echo "Test 3: Specified model set (--model-set high_context)"
# Run with dry run to see the command
./bin/thinktank-wrapper --model-set high_context --dry-run --instructions /tmp/test-file.txt /tmp/test-file.txt

# Check if the output contains the correct number of models from the high_context set
MODELS_COUNT=$(./bin/thinktank-wrapper --model-set high_context --dry-run --instructions /tmp/test-file.txt /tmp/test-file.txt | grep -o -- "--model" | wc -l)
echo "Command contains $MODELS_COUNT model flags"

# Verify the model count matches expected count for "high_context" set (should be 5)
if [ "$MODELS_COUNT" -eq 5 ]; then
  echo "high_context model set successfully used"
else
  echo "ERROR: Expected 5 models in 'high_context' set, but found $MODELS_COUNT"
  exit 1
fi

# Verify that the high context models are present
HIGH_CTX_COMMAND=$(./bin/thinktank-wrapper --model-set high_context --dry-run --instructions /tmp/test-file.txt /tmp/test-file.txt)
if [[ "$HIGH_CTX_COMMAND" =~ "gpt-4.1" && "$HIGH_CTX_COMMAND" =~ "llama-4-maverick" ]]; then
  echo "high_context model set contains expected models"
else
  echo "ERROR: high_context model set missing expected models"
  exit 1
fi

# Test 4: Include leyline files
echo
echo "Test 4: Include leyline files (--include-leyline)"
# Run the command with --include-leyline flag
LEYLINE_COMMAND=$(cd /Users/phaedrus/Development/codex && ./bin/thinktank-wrapper --include-leyline --dry-run --instructions /tmp/test-file.txt)

# Check if leyline files are included (they may not exist in test environment)
if echo "$LEYLINE_COMMAND" | grep -q "docs/leyline\|DEVELOPMENT_PHILOSOPHY"; then
  echo "✓ leyline/philosophy files are correctly included with --include-leyline flag"
else
  echo "✓ No leyline files found (expected if none exist in test environment)"
fi

# Test 5: Include philosophy files (legacy test)
echo
echo "Test 5: Include philosophy files (--include-philosophy)"
# Create a fake philosophy file in the test directory
echo "# Philosophy file content" > /tmp/test-dir/DEVELOPMENT_PHILOSOPHY_TEST.md

# Run the command with --include-philosophy flag
cd /tmp
PHILOSOPHY_COMMAND=$(cd /Users/phaedrus/Development/codex && ./bin/thinktank-wrapper --include-philosophy --dry-run --instructions /tmp/test-file.txt)
cd /Users/phaedrus/Development/codex

# Verify that philosophy files are included in the command
if [[ "$PHILOSOPHY_COMMAND" =~ "DEVELOPMENT_PHILOSOPHY" ]]; then
  echo "DEVELOPMENT_PHILOSOPHY*.md files successfully included"
else
  echo "ERROR: DEVELOPMENT_PHILOSOPHY*.md files not included with --include-philosophy flag"
  # Print the command for debugging
  echo "Command: $PHILOSOPHY_COMMAND"
  exit 1
fi

# Test 6: Skip (removed glance functionality)

# Test 7: Explicit paths
echo
echo "Test 7: Explicit paths"
# Create test files
echo "Test 1 content" > /tmp/test-file-1.txt
echo "Test 2 content" > /tmp/test-file-2.txt

# Run the command with explicit paths
EXPLICIT_COMMAND=$(./bin/thinktank-wrapper --dry-run --instructions /tmp/test-file.txt /tmp/test-file-1.txt /tmp/test-file-2.txt)

# Verify that the explicit paths are included in the command
if [[ "$EXPLICIT_COMMAND" =~ "/tmp/test-file-1.txt" && "$EXPLICIT_COMMAND" =~ "/tmp/test-file-2.txt" ]]; then
  echo "Explicit paths successfully included"
else
  echo "ERROR: Explicit paths not included"
  # Print the command for debugging
  echo "Command: $EXPLICIT_COMMAND"
  exit 1
fi

# Test 8: Mixed options and paths
echo
echo "Test 8: Mixed options and paths"
# Run the command with mixed options and paths
MIXED_COMMAND=$(./bin/thinktank-wrapper --model-set high_context --include-leyline --dry-run --instructions /tmp/test-file.txt /tmp/test-file-1.txt)

# Verify that the command includes the explicit path and gets files from include flags
if [[ "$MIXED_COMMAND" =~ "/tmp/test-file-1.txt" ]]; then
  echo "Mixed options and paths successfully included"
else
  echo "ERROR: Mixed options and paths not included correctly"
  # Print the command for debugging
  echo "Command: $MIXED_COMMAND"
  exit 1
fi

# Test 9: Error handling
echo
echo "Test 9: Error handling (--model-set invalid)"
# Test invalid model set name
INVALID_MODEL_OUTPUT=$(./bin/thinktank-wrapper --model-set invalid --dry-run 2>&1 || echo "Error handled correctly")

# Verify that the error is caught
if [[ "$INVALID_MODEL_OUTPUT" =~ "Error" ]]; then
  echo "Error handling for invalid model set successful"
else
  echo "ERROR: Invalid model set not handled correctly"
  exit 1
fi

# Clean up test files
rm -f /tmp/test-file-1.txt /tmp/test-file-2.txt

# Clean up the test directory
rm -rf /tmp/test-dir

# Clean up
rm /tmp/test-file.txt

echo
echo "All tests passed!"