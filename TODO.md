# TODO: Implement thinktank-wrapper Shell Script

## Setup and Configuration
- [x] Create basic shell script structure (shebang, comments, help text)
- [x] Set proper script permissions (executable)
- [x] Define internal model configuration arrays for "all" model set
- [x] Define internal model configuration arrays for "high_context" model set
- [x] Define default synthesis model configuration
- [x] Add script version number and last updated date

## File Finding Functions
- [x] Implement `find_glance_files_internal()` function to find glance.md files
- [x] Add maxdepth parameter support (default 3) to glance file finder
- [x] Implement `find_philosophy_files_internal()` function to find DEVELOPMENT_PHILOSOPHY*.md files
- [x] Add proper sorting of found files
- [x] Test file finding functions with various directory structures

## Argument Parsing
- [x] Implement basic argument parsing loop
- [x] Add `--model-set` option parsing (with parameter validation)
- [x] Add `--include-glance` flag parsing
- [x] Add `--include-philosophy` flag parsing
- [x] Add `-h/--help` flag parsing
- [x] Add pass-through handling for other thinktank options
- [x] Implement storage for explicit file/directory paths
- [x] Handle edge cases in argument parsing (missing values, etc.)

## File Aggregation
- [x] Implement logic to initialize empty context_files array
- [x] Add conditional logic to include glance files when requested
- [x] Add conditional logic to include philosophy files when requested
- [x] Implement context file array population from file finding functions
- [x] Add explicit path handling to append to context files
- [x] Implement duplicate removal from context files (optional)

## Command Construction
- [x] Add validation for model set selection
- [x] Implement existence check for thinktank executable
- [x] Create command array construction logic
- [x] Ensure proper order of command components (options, models, synthesis model, paths)
- [x] Add proper quoting/escaping of paths with spaces
- [x] Implement command execution logic

## Error Handling
- [x] Add error handling for invalid model set names
- [x] Add error handling for missing thinktank executable
- [x] Handle empty file lists gracefully
- [x] Validate that required parameters are present
- [x] Add proper exit code propagation from thinktank command
- [x] Implement helpful error messages

## Documentation and Help
- [x] Create usage examples section in script header
- [x] Document all available options and their purpose
- [x] Implement comprehensive `--help` output
- [x] Add troubleshooting section to help text
- [x] Document environment considerations

## Testing
- [x] Test with default model set
- [x] Test with specified model set
- [x] Test with glance files inclusion
- [x] Test with philosophy files inclusion
- [x] Test with both file types included
- [x] Test with explicit paths
- [x] Test with mixed options and paths
- [x] Test error handling conditions
- [x] Verify correct command construction
- [x] Test in various directory structures

## Installation and Integration
- [x] Determine optimal installation location
- [x] Update installation script to add wrapper to PATH
- [x] Update documentation to reference new wrapper
- [x] Test wrapper functionality from various locations

## Command Migration
- [ ] Update claude-commands/address.md to use new wrapper
- [ ] Update claude-commands/align.md to use new wrapper
- [ ] Update claude-commands/audit.md to use new wrapper
- [ ] Update claude-commands/consult.md to use new wrapper
- [ ] Update claude-commands/debug.md to use new wrapper
- [ ] Update claude-commands/execute.md to use new wrapper
- [ ] Update claude-commands/extract.md to use new wrapper
- [ ] Update claude-commands/groom.md to use new wrapper
- [ ] Update claude-commands/ideate.md to use new wrapper
- [ ] Update claude-commands/plan.md to use new wrapper
- [ ] Update claude-commands/refactor.md to use new wrapper
- [ ] Update claude-commands/review.md to use new wrapper
- [ ] Update claude-commands/scope.md to use new wrapper
- [ ] Update claude-commands/shrink.md to use new wrapper
- [ ] Update claude-commands/ticket.md to use new wrapper

## Additional Features
- [ ] Implement override for synthesis model
- [ ] Add verbose mode to show constructed command
- [ ] Add dry-run option to show command without executing
- [ ] Implement additional error handling for find commands
- [ ] Add option to customize maxdepth for glance files
- [ ] Handle filenames with spaces and special characters properly
- [ ] Add configuration for custom model sets

## Documentation Updates
- [ ] Update README.md to include information on thinktank-wrapper
- [ ] Document example usage patterns
- [ ] Create sample commands for common scenarios
- [ ] Document migration path from direct thinktank calls

