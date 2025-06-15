# TODO: Thinktank-Wrapper Improvements

## Overview
This document outlines the necessary improvements to thinktank-wrapper to handle edge cases, improve performance, and ensure robust operation.

## High Priority Tasks

### 1. Implement Gitignore Support
**Problem**: Currently processes all files, including those in .gitignore (node_modules, build artifacts, etc.)
**Solution**:
- [x] Add gitignore parsing library (e.g., `pathspec` or `gitignore-parser`)
- [x] Integrate gitignore checking in `context_finder.py` when collecting files
- [ ] Integrate gitignore checking in `tokenizer.py` when processing directories
- [ ] Add `--no-gitignore` flag to bypass gitignore (similar to ripgrep)
- [ ] Handle nested .gitignore files correctly
- [ ] Add tests for gitignore functionality

### 2. Implement Binary File Detection
**Problem**: Attempts to read binary files as UTF-8, causing errors or nonsense token counts
**Solution**:
- [x] Add binary file detection before reading (check first 8KB for null bytes)
- [x] Create a list of known binary extensions to skip (.exe, .dll, .so, .dylib, .jar, .zip, .tar, .gz, .png, .jpg, .jpeg, .gif, .pdf, .ico, .wav, .mp3, .mp4, .avi, .mov, .ttf, .woff, .eot)
- [ ] Add mime-type detection as fallback
- [ ] Log skipped binary files in verbose mode
- [ ] Add `--include-binary` flag to force processing (with warning)
- [ ] Add tests for binary file handling

### 3. Fix Hardcoded Model Selection
**Problem**: tt-plan hardcodes `--model-set high_context`
**Solution**:
- [ ] Update tt-plan to use dynamic model selection based on token count
- [ ] Remove hardcoded `--model-set high_context` from line 28
- [ ] Test tt-plan with various file sizes to ensure proper model selection

### 4. Improve Token Counting Accuracy
**Problem**: Character-based approximation may be inaccurate for some file types
**Solution**:
- [ ] Add support for more tokenizer libraries (anthropic-tokenizer for Claude models)
- [ ] Implement file-type specific token counting strategies
- [ ] Add caching for token counts to improve performance on large codebases
- [ ] Add `--token-cache` flag to enable/disable caching
- [ ] Add tests for token counting accuracy

### 5. Add File Extension Filtering
**Problem**: No way to limit processing to specific file types
**Solution**:
- [ ] Add `--include-ext` flag (e.g., `--include-ext .py .js`)
- [ ] Add `--exclude-ext` flag (e.g., `--exclude-ext .log .tmp`)
- [ ] Integrate with directory traversal in tokenizer and context finder
- [ ] Add tests for extension filtering

## Medium Priority Tasks

### 6. Performance Optimization
- [ ] Implement parallel file processing for token counting
- [ ] Add progress bar for large directory processing
- [ ] Optimize file reading with chunked processing for very large files
- [ ] Add `--max-file-size` flag to skip huge files

### 7. Error Handling Improvements
- [ ] Better error messages for common failures (file permissions, encoding issues)
- [ ] Add retry logic for transient failures
- [ ] Implement graceful degradation when optional features fail
- [ ] Add `--strict` mode that fails on any error

### 8. Logging and Debugging
- [ ] Add `--verbose` flag for detailed operation logging
- [ ] Add `--debug` flag for full debug output
- [ ] Log all skipped files and reasons
- [ ] Add timing information for performance analysis

### 9. Configuration File Support
- [ ] Add support for `.thinktankrc` configuration file
- [ ] Allow setting default flags and preferences
- [ ] Support project-specific configuration
- [ ] Add configuration validation

## Low Priority Tasks

### 10. Additional Features
- [ ] Add `--stats` flag to show detailed token statistics
- [ ] Support for custom token multipliers per project
- [ ] Integration with git hooks for pre-commit token checking
- [ ] Add `--format` flag for output formatting (json, csv, table)

### 11. Documentation Updates
- [ ] Document all new flags and features
- [ ] Add examples for common use cases
- [ ] Create troubleshooting guide
- [ ] Add performance tuning guide

## Testing Requirements

### Unit Tests
- [ ] Test gitignore parsing with various patterns
- [ ] Test binary file detection accuracy
- [ ] Test token counting with known inputs
- [ ] Test file extension filtering
- [ ] Test error handling scenarios

### Integration Tests
- [ ] Test with real repositories of various sizes
- [ ] Test with mixed content (text, binary, various languages)
- [ ] Test performance with large codebases
- [ ] Test model selection thresholds

### Manual QA Tests
- [ ] Test with symlinks and special files
- [ ] Test with various encodings (UTF-8, UTF-16, etc.)
- [ ] Test with permission-restricted files
- [ ] Test cross-platform compatibility

## Implementation Order

1. **Phase 1**: Gitignore support + Binary file detection (Critical for correctness)
2. **Phase 2**: Fix tt-plan + Extension filtering (Improves usability)
3. **Phase 3**: Performance optimization + Better error handling
4. **Phase 4**: Configuration support + Additional features

## Notes

- All changes should maintain backward compatibility
- Default behavior should be sensible for most use cases
- Performance impact should be measured and minimized
- Code should follow existing patterns in the codebase