# TODO: Remaining Test Failures (Pre-Merge Blockers)

*Critical test failures that must be resolved before merging to maintain code quality*

## BLOCKING TEST FAILURES (Must Fix Before Merge)

### 1. Context Finder Issues (4 failures)
- [ ] **Fix philosophy file discovery in tests**
  - Location: `tests/test_context_finder.py:51` 
  - Problem: `test_find_philosophy_files` expects files in temporary CODEX_DIR but finds empty list
  - Root cause: Philosophy file discovery logic looks in wrong directory or path resolution issue
  - Fix: Update context finder to correctly resolve philosophy file paths in test environment

- [ ] **Fix context file search path mismatch** 
  - Location: `tests/test_context_finder.py:89`
  - Problem: `test_find_context_files` returns current working directory files instead of temp directory files
  - Root cause: Search path logic mixing current directory with test fixture directories  
  - Fix: Ensure context file search respects test fixture directories

- [ ] **Fix leyline files fallback to philosophy**
  - Location: `tests/test_context_finder.py:116,149`
  - Problem: Both leyline directory and fallback tests return empty lists instead of expected philosophy files
  - Root cause: Leyline discovery and philosophy fallback logic not finding files in test environment
  - Fix: Update leyline file discovery to work correctly with test fixtures

### 2. Gitignore Precedence Logic (1 failure) 
- [ ] **Fix gitignore negation pattern precedence**
  - Location: `tests/test_nested_gitignore.py:223`
  - Problem: `src/important.log` incorrectly ignored despite `!important.log` negation in src/.gitignore  
  - Root cause: Gitignore precedence logic not properly handling negation patterns from subdirectories
  - Expected: `!important.log` in src/ should override `*.log` in root 
  - Fix: Implement proper Git-style precedence where deeper negation patterns override parent ignore patterns

### 3. Tokenizer API Mismatch (1 failure)
- [x] **Fix deprecated extension parameter usage**
  - Location: `tests/test_tokenizer.py:965`
  - Problem: Test calls `count_directory_tokens(extensions=...)` but method no longer accepts `extensions` parameter
  - Root cause: Test not updated after API refactoring to use TokenCounter constructor parameters
  - Fix: ✅ Updated test to use `TokenCounter(include_extensions=['.py'])` and fixed comparison logic

### 4. Tokenizer Binary/Encoding Detection (6 failures)
- [ ] **Fix binary file detection logic**
  - Location: `tests/test_tokenizer.py:109,113` 
  - Problem: Binary file detection incorrectly identifies files as binary/non-binary
  - Root cause: Binary detection heuristics or magic number detection not working as expected
  - Fix: Review and correct binary file detection algorithm

- [ ] **Fix MIME type detection with magic**
  - Location: `tests/test_tokenizer.py:327`
  - Problem: MIME type detection returning None instead of expected type
  - Root cause: python-magic library integration or mock setup issue
  - Fix: Ensure MIME type detection works correctly with available libraries

- [ ] **Fix token counting accuracy**
  - Location: `tests/test_tokenizer.py:403,469`
  - Problem: Token counts off by 1 (expected 9 got 8, expected 24 got 23)
  - Root cause: Tokenization logic boundary conditions or encoding handling
  - Fix: Review tokenization algorithm for edge cases and encoding issues

- [x] **Fix encoding detection for binary files**
  - Location: `tests/test_tokenizer.py:1483`
  - Problem: `detect_file_encoding` returns 'latin1' instead of None for binary files  
  - Root cause: Encoding detection fallback being too permissive for binary data
  - Fix: ✅ Improved binary file detection with null byte and printable character checks before encoding analysis

- [x] **Fix encoding error messages**
  - Location: `tests/test_tokenizer.py:1508,1540`
  - Problem: Error messages don't contain expected text ("binary data", "UTF-8 encoding issues")
  - Root cause: Error message generation logic using generic encoding advice instead of specific detection
  - Fix: ✅ Enhanced error message generation with encoding detection priority and UTF-8 corruption detection

### 5. Integration and Infrastructure (5 failures)
- [ ] **Fix command builder IO error handling**
  - Location: `tests/test_command_builder.py` 
  - Problem: Mock expectations for file operations not being met
  - Root cause: Error handling path not triggering expected file cleanup operations
  - Fix: Review command builder error handling and file cleanup logic

- [ ] **Fix logging configuration tests**
  - Location: `tests/test_logging_config.py:134,163`
  - Problem: Logging setup and message capture not working in test environment
  - Root cause: Logging configuration isolation or capture mechanism issues  
  - Fix: Ensure logging tests properly isolate and capture log output

- [ ] **Fix integration test execution**
  - Location: `tests/test_integration.py:157`
  - Problem: Integration test assertion failure (assert False)
  - Root cause: End-to-end workflow not executing correctly in test environment
  - Fix: Debug integration test workflow and fix execution path

- [ ] **Fix main gitignore integration test**
  - Location: `tests/test_main_gitignore_integration.py:192` 
  - Problem: Expected return code 1 but got 0
  - Root cause: Main function not returning expected error code for gitignore scenarios
  - Fix: Review main function error handling and return code logic

## PRIORITY MATRIX

**Critical (Must Fix)**: Context Finder, Gitignore Precedence, Tokenizer API  
**High**: Binary Detection, Error Messages, Integration Tests  
**Medium**: Token Counting Edge Cases, Logging Tests

## SUCCESS CRITERIA

- [ ] All 19 test failures resolved 
- [ ] Test suite achieves 100% pass rate (207/207 passing)
- [ ] No regressions introduced during fixes
- [ ] Core functionality (gitignore, context finding, tokenization) working correctly
- [ ] Integration tests demonstrate end-to-end workflow success