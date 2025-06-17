# Migration Example for tt-* Scripts

## Before: Fixed Model Set Selection

```bash
#!/bin/bash
# OLD: tt-plan (fixed high_context)
set -e

# ... context preparation ...

# Fixed model set - potentially wasteful for small contexts
thinktank-wrapper --template plan --inject PLAN-CONTEXT.md --model-set high_context --include-philosophy --include-leyline ./
```

## After: Dynamic Model Selection

```bash
#!/bin/bash
# NEW: tt-plan (dynamic selection)
set -e

# ... context preparation ...

# Automatic model selection based on token count
thinktank-wrapper --template plan --inject PLAN-CONTEXT.md --include-philosophy --include-leyline ./

# The wrapper will output:
# TOKEN_COUNT: 12543
# Using model set: high_context (threshold: 8000)
# [proceeds with appropriate model set]
```

## Advanced: Token-Aware Script Logic

```bash
#!/bin/bash
# ADVANCED: tt-plan with token awareness
set -e

# Prepare context as before...
cat > PLAN-CONTEXT.md << EOF
# Plan Details
$(cat PLAN.md)
EOF

# Get token count and capture output
OUTPUT=$(thinktank-wrapper --template plan --inject PLAN-CONTEXT.md --include-philosophy --include-leyline ./ 2>&1)

# Extract token count from output
TOKEN_COUNT=$(echo "$OUTPUT" | grep "TOKEN_COUNT:" | cut -d' ' -f2)

# Conditional logic based on token count
if [ "$TOKEN_COUNT" -gt 50000 ]; then
    echo "⚠️  Warning: Very large context ($TOKEN_COUNT tokens)"
    echo "   Consider reducing scope or using --token-threshold"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
elif [ "$TOKEN_COUNT" -gt 20000 ]; then
    echo "ℹ️  Large context detected ($TOKEN_COUNT tokens)"
    echo "   This may take longer and cost more"
fi

# The actual thinktank execution is already complete at this point
# (we captured its output above)
```

## Backward Compatibility

Existing scripts continue to work unchanged:

```bash
# This still works exactly as before
thinktank-wrapper --template plan --model-set high_context --include-philosophy ./

# Token counting can be disabled
thinktank-wrapper --template plan --disable-token-counting --model-set all ./
```

## Environment-Based Configuration

```bash
# Set organization-wide defaults
export LLM_CONTEXT_THRESHOLD=12000
export TOKEN_COUNT_PROVIDER=anthropic

# Scripts automatically use these settings
thinktank-wrapper --template review ./
```
