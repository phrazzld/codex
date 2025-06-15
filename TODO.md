# TODO: Thinktank-Wrapper Improvements

## Core Issues - COMPLETED ✅

**The main problems have been solved:**

- [x] **Gitignore Support**: Now respects .gitignore files and skips ignored files
- [x] **Binary File Detection**: Automatically skips binary files with smart detection  
- [x] **Fix Hardcoded Model Selection**: tt-plan now uses dynamic model selection
- [x] **Better Tokenizers**: Added Anthropic API support for accurate token counting

## Remaining Simple Improvements

### File Extension Filtering (Nice to Have) ✅
**Problem**: No way to limit processing to specific file types
- [x] Add `--include-ext .py .js` flag 
- [x] Add `--exclude-ext .log .tmp` flag
- [x] Basic test coverage

### Better Error Messages (Nice to Have)  
**Problem**: Some error messages could be clearer
- [ ] Improve file permission error messages
- [ ] Better encoding error handling
- [ ] Add `--verbose` flag for debugging (partially exists)

### Simple Configuration (Nice to Have)
**Problem**: No way to set default preferences
- [ ] Add `.thinktankrc` file support for default flags
- [ ] Basic validation

## Notes

- **Keep it simple**: Only add features that solve real problems
- **Maintain compatibility**: Don't break existing behavior  
- **Test what matters**: Focus on core functionality, not edge cases

**Current Status**: The main functionality works well. These remaining items are optional improvements, not critical fixes.