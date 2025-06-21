# Token Counting Usage Guide

## Overview

The thinktank wrapper now includes automatic token counting and dynamic model selection to optimize costs and prevent context window overflows.

## How It Works

1. **Automatic Token Counting**: Before executing thinktank, the wrapper counts tokens in all context files
2. **Dynamic Model Selection**: Based on token count, it selects the appropriate model set:
   - `<= 8000 tokens`: Uses "all" model set (includes smaller, cheaper models)
   - `> 8000 tokens`: Uses "high_context" model set (only high-capacity models)

## Usage Examples

### Basic Usage (Automatic)
```bash
# Token counting is enabled by default
thinktank-wrapper --template plan --include-philosophy --include-leyline ./

# Output:
# TOKEN_COUNT: 5432
# [thinktank executes with "all" model set]
```

### Large Context Example
```bash
# With many files exceeding threshold
thinktank-wrapper --template review ./src ./tests ./docs

# Output:
# TOKEN_COUNT: 15234
# Using model set: high_context (threshold: 8000)
# [thinktank executes with "high_context" model set]
```

### Custom Threshold
```bash
# Set a higher threshold for model selection
thinktank-wrapper --template debug --token-threshold 20000 ./

# Output:
# TOKEN_COUNT: 15234
# [Uses "all" model set since 15234 < 20000]
```

### Disable Token Counting
```bash
# Use explicit model set without token counting
thinktank-wrapper --template plan --disable-token-counting --model-set high_context ./
```

## Configuration

### Environment Variables

```bash
# Set default token threshold (default: 8000)
export LLM_CONTEXT_THRESHOLD=10000

# Change token counting provider (default: openai)
export TOKEN_COUNT_PROVIDER=anthropic

# Disable token counting globally
export ENABLE_TOKEN_COUNTING=false
```

### Token Counting Accuracy

The wrapper uses a hybrid approach:
- **OpenAI**: Uses `tiktoken` if available (95%+ accuracy)
- **Other Providers**: Character-based approximation with provider-specific ratios
- **File Type Awareness**: Adjusts estimates based on file extensions

Typical accuracy: 85-95% of actual token count

### Performance Impact

Token counting adds minimal overhead:
- Small projects (<100 files): ~50ms
- Large projects (1000+ files): ~200ms

## Integration with Existing Scripts

### Update tt-* Scripts
```bash
#!/bin/bash
# Example: tt-plan with automatic model selection

# Old (fixed model set):
thinktank-wrapper --template plan --model-set high_context ...

# New (dynamic selection):
thinktank-wrapper --template plan ...
# Model set chosen automatically based on context size
```

### Conditional Logic Example
```bash
# Get token count for conditional logic
TOKEN_OUTPUT=$(thinktank-wrapper --template plan --dry-run ... 2>&1)
TOKEN_COUNT=$(echo "$TOKEN_OUTPUT" | grep "TOKEN_COUNT:" | cut -d' ' -f2)

if [ "$TOKEN_COUNT" -gt 50000 ]; then
    echo "Warning: Very large context ($TOKEN_COUNT tokens)"
fi
```

## Troubleshooting

### Token Counting Errors
```
TOKEN_COUNT: 5432
Token counting error: Error reading file /path/to/binary: 'utf-8' codec can't decode
```
- Binary files are skipped with a warning
- Token counting continues with readable files

### Unexpected Model Selection
Check the output for the actual token count and threshold:
```
TOKEN_COUNT: 8001
Using model set: high_context (threshold: 8000)
```

### Performance Issues
For very large codebases, consider:
1. Using explicit file paths instead of directories
2. Increasing the threshold to use "all" models when appropriate
3. Disabling token counting for repeated runs with `--disable-token-counting`

## Cost Optimization Tips

1. **Set Appropriate Thresholds**: The default 8000 tokens works well for most cases
2. **Use Specific Paths**: Instead of `./`, specify only needed directories
3. **Monitor Token Counts**: Use the output to understand your typical context sizes
4. **Leverage Caching**: The wrapper caches tokenization results within a run

## Future Enhancements

Planned improvements:
- Per-model token counting for more accurate selection
- Cost estimation output
- Token count caching across runs
- Support for more tokenization libraries
