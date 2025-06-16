# TODO: Pre-Merge Critical Issues

*Issues identified by comprehensive AI code review that must be addressed before merging*

## BLOCKING ISSUES (Must Fix Before Merge)

### Test Suite Failures
- [x] **Fix test API mismatch in extension filtering tests**
  - Location: `tests/test_tokenizer.py:477`
  - Problem: Test calls `count_directory_tokens(tmp_path, extensions=['.py'])` but method no longer accepts `extensions` parameter
  - Fix: Update test to use `TokenCounter("openai", include_extensions=['.py']).count_directory_tokens(tmp_path)`
  - Verification: Run `python -m pytest tests/test_tokenizer.py::TestExtensionFiltering -v` to confirm all tests pass

## HIGH PRIORITY FUNCTIONAL BUGS

### Gitignore Rule Precedence Logic Error  
- [~] **Fix gitignore precedence to match Git's "last rule wins" behavior**
  - Location: `src/thinktank_wrapper/gitignore.py:139-158` (`should_ignore` method)
  - Problem: Current logic processes from root→deepest and returns on first match, preventing deeper `.gitignore` files from overriding parent rules
  - Expected behavior: `!important.log` in subdirectory should override `*.log` in root `.gitignore`
  - Fix strategy:
    1. Reverse iteration order: process from deepest→root directory  
    2. Let last matching rule determine final ignore status
    3. Ensure negation patterns (`!`) work correctly
  - Test case: Create nested directories with conflicting gitignore rules and verify deeper rules win

### Explicit Directory Filtering Inconsistency
- [ ] **Apply gitignore filtering to explicit directories for consistency**
  - Location: `src/thinktank_wrapper/context_finder.py:252-253`
  - Problem: Explicit directories bypass all gitignore/extension filtering, potentially including massive irrelevant directories
  - Current behavior: `thinktank-wrapper src/ node_modules/` includes `node_modules/` even if gitignored
  - Options:
    - **Recommended**: Apply gitignore filtering to directories and warn user when ignored dirs are skipped
    - **Alternative**: Keep current behavior but add prominent warning when including gitignored directories
  - Test case: Verify `thinktank-wrapper .` respects `.gitignore` rules for both files and directories

## TESTING REQUIREMENTS

### Integration Tests for Fixed Issues
- [ ] **Add gitignore precedence integration test**
  - Create test with nested directories containing conflicting `.gitignore` rules
  - Verify subdirectory rules override parent rules
  - Test negation patterns (`!`) work correctly
  
- [ ] **Add explicit directory gitignore test**
  - Test behavior when user explicitly includes gitignored directories
  - Verify consistent filtering behavior or appropriate warnings

### Pre-merge Validation
- [ ] **Run full test suite and verify all tests pass**
  - Command: `python -m pytest tests/ -v` (requires pytest installation)
  - All extension filtering tests must pass
  - All gitignore tests must pass
  - No regressions in existing functionality

## NOTES

- **Priority**: Address blocking issues first, then high-priority functional bugs
- **Timeline**: These issues affect core functionality and user trust - should be fixed before any production deployment
- **Testing**: Each fix should include test coverage to prevent regression
- **Documentation**: Update any user-facing docs if behavior changes significantly

## VERIFICATION CHECKLIST

Before marking complete:
- [ ] All test failures resolved
- [ ] Gitignore behavior matches Git's actual precedence rules  
- [ ] Explicit directory handling has consistent, documented behavior
- [ ] No new test failures introduced
- [ ] Manual testing with real-world repositories confirms expected behavior