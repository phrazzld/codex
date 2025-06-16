# Enhanced Tokenization Support

This document describes the enhanced tokenization capabilities added to thinktank-wrapper, providing more accurate token counting for various LLM providers.

## Overview

The tokenizer module now supports multiple tokenization methods:

1. **Character-based approximation** (fallback/default)
2. **OpenAI tiktoken** (for GPT models) 
3. **Anthropic API** (for Claude models)

## Installation

To use the enhanced tokenizers, install the optional dependencies:

```bash
pip install -e ".[tokenizers]"
```

This installs:
- `tiktoken>=0.5.0` - OpenAI tokenizer
- `anthropic>=0.28.0` - Anthropic API client
- `python-magic>=0.4.25` - Enhanced binary file detection

## Configuration

### Anthropic API Token Counting

To use Anthropic's accurate token counting API, set your API key:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

The Anthropic tokenizer uses the official `count_tokens` endpoint for precise token counts before sending content to Claude models.

### OpenAI tiktoken

For OpenAI models, tiktoken is automatically used when available. No additional configuration required.

## Behavior

### Provider Selection

Each provider uses its most accurate available tokenizer:

- **anthropic**: Uses Anthropic API → falls back to character approximation
- **openai**: Uses tiktoken → falls back to character approximation  
- **google**: Uses character approximation (no specific tokenizer available)
- **openrouter**: Uses character approximation (mixed models)

### Fallback Strategy

If the preferred tokenizer fails or is unavailable, the system gracefully falls back to character-based approximation using empirically-determined ratios.

### File Type Adjustments

After getting base token counts, file-type specific adjustments are applied:

- `.py`, `.js`, `.ts`: +15% (code density)
- `.java`: +18% (verbose syntax)
- `.md`: -5% (lower token density)
- `.json`: +20% (structural overhead)
- `.xml`, `.html`: +25% (markup overhead)

## Usage Examples

### Basic Usage

```python
from thinktank_wrapper.tokenizer import TokenCounter

# Use Anthropic API for accurate Claude token counting
counter = TokenCounter("anthropic")
tokens = counter.count_text_tokens("Your text here")

# Use tiktoken for accurate GPT token counting  
counter = TokenCounter("openai")
tokens = counter.count_text_tokens("Your text here")
```

### File Processing

```python
# Count tokens in a file
tokens, error = counter.count_file_tokens("path/to/file.py")

# Count tokens in a directory
tokens, errors = counter.count_directory_tokens("path/to/directory")
```

### Multi-Provider Comparison

```python
from thinktank_wrapper.tokenizer import MultiProviderTokenCounter

multi_counter = MultiProviderTokenCounter()
results = multi_counter.count_all_providers(["file1.py", "file2.md"])

for provider, (tokens, errors) in results.items():
    print(f"{provider}: {tokens} tokens")
```

## API Costs

The Anthropic tokenizer makes API calls to count tokens. Consider these costs:

- Token counting calls are separate from generation calls
- Uses Claude 3 Haiku (cost-effective model) for counting
- Only called for Anthropic provider when API key is available
- Automatically falls back to free approximation if API fails

## Error Handling

The system includes comprehensive error handling:

- Missing API keys → falls back to character approximation
- Network failures → falls back to character approximation
- Malformed responses → falls back to character approximation
- Missing libraries → falls back to character approximation

All errors are logged at appropriate levels for debugging.

## Performance

- **Character approximation**: Instant
- **tiktoken**: Very fast (local tokenization)
- **Anthropic API**: Network latency (typically <1 second)

For large files, consider using the character approximation mode to avoid API costs and network delays.

## Accuracy Comparison

Accuracy varies by provider and content type:

1. **Anthropic API**: Most accurate for Claude models
2. **tiktoken**: Most accurate for GPT models  
3. **Character approximation**: Conservative estimates, generally within 10-20% of actual

## Integration with thinktank-wrapper

The enhanced tokenization is automatically used by:

- Dynamic model selection (chooses model sets based on token counts)
- Context size validation (prevents exceeding model context windows)
- Performance optimization (enables better resource planning)

Token counts are displayed during execution:

```
TOKEN_COUNT: 1500
Using model set: all (threshold: 200000)
```

## Best Practices

1. **Set API keys** for most accurate counting when using respective providers
2. **Monitor API costs** if using Anthropic token counting extensively  
3. **Use character approximation** for development/testing to avoid API calls
4. **Test with real content** to validate token counting accuracy for your use case
5. **Consider file type adjustments** when estimating tokens for mixed content

## Troubleshooting

### Anthropic API Issues

```bash
# Check API key is set
echo $ANTHROPIC_API_KEY

# Test API access
python -c "import anthropic; print(anthropic.__version__)"
```

### tiktoken Issues

```bash
# Test tiktoken installation
python -c "import tiktoken; print(tiktoken.__version__)"
```

### Fallback Behavior

If you see character approximation being used when you expected API tokenization:

1. Check API key environment variables
2. Verify library installations
3. Check network connectivity
4. Review logs for error messages

The system is designed to continue working even when enhanced tokenizers fail, ensuring robust operation in all environments.