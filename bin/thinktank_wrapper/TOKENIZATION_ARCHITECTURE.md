# Tokenization Architecture for Thinktank Wrapper

## Executive Summary

This document presents three architectural approaches for integrating token counting and dynamic model selection into the thinktank wrapper, enabling cost optimization and context window validation.

## Context & Requirements

### Current State
- Thinktank wrapper uses pre-defined model sets ("all" and "high_context")
- No awareness of actual context size before execution
- Risk of exceeding context windows or overpaying for small contexts

### Requirements
1. Pre-calculate token count before model selection
2. Dynamically choose model set based on context size
3. Support multiple LLM providers (OpenAI, Anthropic, Google)
4. Configurable threshold (default: 8000 tokens)
5. Output token count to stdout before execution

## Research Findings

### Tokenization Strategies

#### 1. **Provider-Specific Libraries**
- **OpenAI**: `tiktoken` - Native, highly accurate
- **Anthropic**: Custom tokenizer, no public library
- **Google**: Vertex AI SDK integration only
- **Challenge**: No unified solution across providers

#### 2. **Character-Based Approximation**
- **Approach**: Use empirical char-to-token ratios
- **OpenAI/Anthropic**: ~4 chars/token (0.25 ratio)
- **Google**: ~4.3 chars/token (0.23 ratio)
- **Pros**: Simple, fast, no dependencies
- **Cons**: ±15% accuracy variance

#### 3. **Hybrid Approach**
- Use `tiktoken` when available for OpenAI
- Fall back to character approximation for others
- Adjust ratios based on file types

### Context Window Analysis

From `models.yaml`:
- **Low Context Models**: 65K-200K tokens
- **High Context Models**: 200K-1M+ tokens
- **Threshold Rationale**: 8K tokens is ~12% of smallest model

## Architecture Plans

### Plan A: Integrated Module Approach

**Description**: Add tokenization as a core module within thinktank wrapper.

**Implementation**:
```python
# New module: src/thinktank_wrapper/tokenizer.py
# Integration in __main__.py:

# After context file discovery
token_counter = TokenCounter(provider="openai")
total_tokens, errors = token_counter.estimate_model_tokens(context_files)
print(f"TOKEN_COUNT: {total_tokens}")

# Dynamic model selection
if total_tokens <= config.LLM_CONTEXT_THRESHOLD:
    parsed_args.model_set = "all"
else:
    parsed_args.model_set = "high_context"
```

**Pros**:
- Seamless integration with existing codebase
- Access to all internal configurations
- Unified logging and error handling
- Easy to maintain and test

**Cons**:
- Requires modification of core wrapper logic
- Couples tokenization to wrapper implementation

**Performance**: O(n) where n is total characters in context files
**Accuracy**: 85-95% with hybrid approach
**Complexity**: Low - integrates naturally with existing flow

### Plan B: Preprocessing Script Approach

**Description**: Create a separate preprocessing script that wraps the wrapper.

**Implementation**:
```bash
#!/bin/bash
# bin/tt-smart-wrapper

# Count tokens
TOKEN_COUNT=$(python -m thinktank_wrapper.tokenizer "$@")
echo "TOKEN_COUNT: $TOKEN_COUNT"

# Select model set
if [ "$TOKEN_COUNT" -le "${LLM_CONTEXT_THRESHOLD:-8000}" ]; then
    MODEL_SET="all"
else
    MODEL_SET="high_context"
fi

# Execute wrapper with dynamic model set
exec thinktank-wrapper --model-set "$MODEL_SET" "$@"
```

**Pros**:
- No changes to existing wrapper code
- Can be added/removed without affecting core
- Language agnostic (shell script)

**Cons**:
- Requires parsing arguments twice
- Potential arg handling inconsistencies
- Additional maintenance overhead

**Performance**: Adds subprocess overhead (~50ms)
**Accuracy**: Same as Plan A
**Complexity**: Medium - requires careful argument forwarding

### Plan C: Configuration-Driven Approach

**Description**: Extend model configuration to include token limits and auto-selection rules.

**Implementation**:
```yaml
# models.yaml addition:
model_sets:
  all:
    models: [...]
    max_context_recommendation: 8000
  high_context:
    models: [...]
    min_context_recommendation: 8001

# New config module:
class ModelSelector:
    def select_model_set(self, token_count: int) -> str:
        for set_name, config in model_sets.items():
            if token_count <= config.get('max_context_recommendation', float('inf')):
                return set_name
        return 'high_context'  # fallback
```

**Pros**:
- Highly extensible for future model sets
- Configuration-driven (no code changes for thresholds)
- Supports complex selection rules

**Cons**:
- Over-engineered for current binary choice
- Requires YAML schema changes
- More complex testing

**Performance**: Negligible overhead
**Accuracy**: Same as Plan A
**Complexity**: High - requires config schema evolution

## Comparative Analysis

| Aspect | Plan A (Integrated) | Plan B (Script) | Plan C (Config) |
|--------|-------------------|-----------------|-----------------|
| **Token Accuracy** | 85-95% | 85-95% | 85-95% |
| **Performance** | <100ms | ~150ms | <100ms |
| **Implementation** | 2-3 hours | 1-2 hours | 4-5 hours |
| **Maintainability** | High | Medium | Medium |
| **Extensibility** | Good | Limited | Excellent |
| **Testing Effort** | Low | Medium | High |
| **Risk** | Low | Medium | Low |

## Recommendation: Plan A (Integrated Module)

### Rationale

1. **Optimal Balance**: Provides the best tradeoff between functionality and complexity
2. **Natural Integration**: Fits seamlessly into existing architecture
3. **Performance**: Minimal overhead with direct Python integration
4. **Maintainability**: Single codebase, unified testing strategy
5. **Future-Proof**: Easy to extend with provider-specific tokenizers

### Implementation Details

1. **Tokenizer Module** (`tokenizer.py`):
   - Hybrid tokenization (tiktoken + fallback)
   - File type awareness for better accuracy
   - Multi-provider support with provider-specific ratios

2. **Integration Points**:
   - Add token counting after context file discovery
   - Override model_set before command building
   - Add `--token-threshold` CLI option (optional)

3. **Configuration**:
   ```python
   # config.py additions
   LLM_CONTEXT_THRESHOLD = int(os.environ.get("LLM_CONTEXT_THRESHOLD", "8000"))
   TOKEN_COUNT_PROVIDERS = ["openai", "anthropic", "google", "openrouter"]
   ```

4. **Output Format**:
   ```
   TOKEN_COUNT: 12543
   Using model set: high_context (threshold: 8000)
   ```

### Migration Path

1. Implement tokenizer module with tests
2. Add token counting to main flow (behind feature flag initially)
3. Add CLI option for threshold override
4. Update documentation and examples
5. Remove feature flag after validation

This approach provides immediate value while maintaining flexibility for future enhancements such as per-model token counting or cost estimation.