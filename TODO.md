# TODO: Remaining Test Failures (Pre-Merge Blockers)

*Critical test failures that must be resolved before merging to maintain code quality*

## BLOCKING TEST FAILURES (Must Fix Before Merge)

### 1. Context Finder Issues (4 failures)
- [x] **Remove philosophy file support and fix context finder tests**
  - Location: `tests/test_context_finder.py:51` 
  - Problem: Tests expected philosophy file discovery but philosophy files are not part of thinktank-wrapper scope
  - Root cause: Philosophy file functionality should not exist - thinktank-wrapper focuses on leyline files, glance files, explicit paths, and instruction files
  - Fix: ✅ Removed all philosophy file functionality and updated tests to focus on leyline and glance file discovery only

- [x] **Fix context file search path mismatch** 
  - Location: `tests/test_context_finder.py:89`
  - Problem: `test_find_context_files` returns current working directory files instead of temp directory files
  - Root cause: Search path logic mixing current directory with test fixture directories  
  - Fix: ✅ Added `monkeypatch.chdir(temp_dir)` to test so `find_glance_files([])` searches in temp directory where mock glance files are created

- [x] **Fix leyline file discovery in test fixtures**
  - Location: `tests/test_context_finder.py:40`
  - Problem: Leyline directory tests may not be finding files correctly in test environment
  - Root cause: macOS symlink path resolution causing `/var` vs `/private/var` mismatch in test comparisons
  - Fix: ✅ Used `Path.resolve()` to ensure consistent symlink resolution in test assertions

### 2. Gitignore Precedence Logic (1 failure) 
- [x] **Fix gitignore negation pattern precedence**
  - Location: `tests/test_nested_gitignore.py:223`
  - Problem: `src/important.log` incorrectly ignored despite `!important.log` negation in src/.gitignore  
  - Root cause: Gitignore precedence logic not properly handling negation patterns from subdirectories
  - Expected: `!important.log` in src/ should override `*.log` in root 
  - Fix: ✅ Implemented proper Git-style precedence by separating directory patterns from file patterns and applying correct precedence rules

### 3. Tokenizer API Mismatch (1 failure)
- [x] **Fix deprecated extension parameter usage**
  - Location: `tests/test_tokenizer.py:965`
  - Problem: Test calls `count_directory_tokens(extensions=...)` but method no longer accepts `extensions` parameter
  - Root cause: Test not updated after API refactoring to use TokenCounter constructor parameters
  - Fix: ✅ Updated test to use `TokenCounter(include_extensions=['.py'])` and fixed comparison logic

### 4. Tokenizer Binary/Encoding Detection (6 failures)
- [x] **Fix binary file detection logic**
  - Location: `tests/test_tokenizer.py:109,113` 
  - Problem: Binary file detection incorrectly identifies files as binary/non-binary
  - Root cause: Function checked extensions before file existence, and applied content override too broadly
  - Fix: ✅ Added file existence check first, refined content analysis to only override ambiguous extensions (.dat, .bin, .dump)

- [x] **Fix MIME type detection with magic**
  - Location: `tests/test_tokenizer.py:327`
  - Problem: MIME type detection returning None instead of expected type
  - Root cause: MAGIC_AVAILABLE patch not applied to all test assertions in mock test
  - Fix: ✅ Wrapped all mock assertions within MAGIC_AVAILABLE patch context

- [x] **Fix token counting accuracy**
  - Location: `tests/test_tokenizer.py:403,469`
  - Problem: Token counts off by 1 (expected 9 got 8, expected 24 got 23)
  - Root cause: Double truncation in approximation calculation and test fixture character count mismatch
  - Fix: ✅ Fixed test fixture to use 31 chars as intended, unified calculation to avoid double truncation when using approximation

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

**Critical (Must Fix)**: Context Finder Path Issues  
**High**: Binary Detection, Integration Tests  
**Medium**: Token Counting Edge Cases, Logging Tests, MIME Type Detection

## SUCCESS CRITERIA

- [ ] All remaining test failures resolved (14 tasks remaining)
- [ ] Test suite achieves 100% pass rate
- [ ] No regressions introduced during fixes
- [ ] Core functionality working correctly:
  - [x] Gitignore pattern precedence 
  - [ ] Context finding (leyline + glance files)
  - [ ] Tokenization and binary detection
- [ ] Integration tests demonstrate end-to-end workflow success