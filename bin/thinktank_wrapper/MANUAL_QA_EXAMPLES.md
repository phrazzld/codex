# Manual QA Examples for Token Counting

## Test 1: Small Context (Should select "all" models)

```bash
cd /Users/phaedrus/Development/codex/bin/thinktank_wrapper

# Test with just the pyproject.toml file (small context)
PYTHONPATH=src python -m thinktank_wrapper --template plan --dry-run pyproject.toml

# Expected output:
# TOKEN_COUNT: ~200-300
# [Should NOT show "Using model set" since it uses default "all"]
# Would execute: ... [many models including o4-mini, o3, deepseek, etc.]
```

## Test 2: Medium Context (Should select "high_context" models)

```bash
# Test with the entire source directory
PYTHONPATH=src python -m thinktank_wrapper --template plan --dry-run --include-philosophy src/

# Expected output:
# TOKEN_COUNT: ~15000-25000 
# Using model set: high_context (threshold: 8000)
# Would execute: ... [fewer models, only gpt-4.1, gemini-2.5-*, llama-4-*]
```

## Test 3: Large Context (Should definitely select "high_context")

```bash
# Test with philosophy docs (large context)
PYTHONPATH=src python -m thinktank_wrapper --template plan --dry-run --include-philosophy ../../docs/

# Expected output:
# TOKEN_COUNT: ~70000+
# Using model set: high_context (threshold: 8000)  
# Would execute: ... [only high-capacity models]
```

## Test 4: Custom Threshold

```bash
# Set a very high threshold to force "all" models even with large context
PYTHONPATH=src python -m thinktank_wrapper --template plan --dry-run --token-threshold 100000 --include-philosophy ../../docs/

# Expected output:
# TOKEN_COUNT: ~70000+
# [Should NOT show "Using model set" since 70000 < 100000, uses "all"]
# Would execute: ... [many models including smaller ones]
```

## Test 5: Disable Token Counting

```bash
# Disable token counting entirely
PYTHONPATH=src python -m thinktank_wrapper --template plan --dry-run --disable-token-counting --model-set high_context src/

# Expected output:
# [NO TOKEN_COUNT line]
# [NO "Using model set" line]
# Would execute: ... [only high-context models as explicitly requested]
```

## Test 6: Environment Variable Override

```bash
# Set environment variable to change default threshold
LLM_CONTEXT_THRESHOLD=1000 PYTHONPATH=src python -m thinktank_wrapper --template plan --dry-run src/

# Expected output:
# TOKEN_COUNT: ~15000+
# Using model set: high_context (threshold: 1000)
# [Should select high_context because even medium context > 1000]
```

## Test 7: Different Providers

```bash
# Test with different token counting provider
TOKEN_COUNT_PROVIDER=anthropic PYTHONPATH=src python -m thinktank_wrapper --template plan --dry-run pyproject.toml

# Expected output:
# TOKEN_COUNT: ~200-300 (slightly different from OpenAI)
# [Should still select "all" models]
```