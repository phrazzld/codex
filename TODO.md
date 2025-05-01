# TODO: Implement thinktank-wrapper Shell Script

## Setup and Configuration
- [x] Create basic shell script structure (shebang, comments, help text)
- [x] Set proper script permissions (executable)
- [ ] Define internal model configuration arrays for "all" model set
- [ ] Define internal model configuration arrays for "high_context" model set
- [ ] Define default synthesis model configuration
- [x] Add script version number and last updated date

## File Finding Functions
- [ ] Implement `find_glance_files_internal()` function to find glance.md files
- [ ] Add maxdepth parameter support (default 3) to glance file finder
- [ ] Implement `find_philosophy_files_internal()` function to find DEVELOPMENT_PHILOSOPHY*.md files
- [ ] Add proper sorting of found files
- [ ] Test file finding functions with various directory structures

## Argument Parsing
- [ ] Implement basic argument parsing loop
- [ ] Add `--model-set` option parsing (with parameter validation)
- [ ] Add `--include-glance` flag parsing
- [ ] Add `--include-philosophy` flag parsing
- [ ] Add `-h/--help` flag parsing
- [ ] Add pass-through handling for other thinktank options
- [ ] Implement storage for explicit file/directory paths
- [ ] Handle edge cases in argument parsing (missing values, etc.)

## File Aggregation
- [ ] Implement logic to initialize empty context_files array
- [ ] Add conditional logic to include glance files when requested
- [ ] Add conditional logic to include philosophy files when requested
- [ ] Implement context file array population from file finding functions
- [ ] Add explicit path handling to append to context files
- [ ] Implement duplicate removal from context files (optional)

## Command Construction
- [ ] Add validation for model set selection
- [ ] Implement existence check for thinktank executable
- [ ] Create command array construction logic
- [ ] Ensure proper order of command components (options, models, synthesis model, paths)
- [ ] Add proper quoting/escaping of paths with spaces
- [ ] Implement command execution logic

## Error Handling
- [ ] Add error handling for invalid model set names
- [ ] Add error handling for missing thinktank executable
- [ ] Handle empty file lists gracefully
- [ ] Validate that required parameters are present
- [ ] Add proper exit code propagation from thinktank command
- [ ] Implement helpful error messages

## Documentation and Help
- [ ] Create usage examples section in script header
- [ ] Document all available options and their purpose
- [ ] Implement comprehensive `--help` output
- [ ] Add troubleshooting section to help text
- [ ] Document environment considerations

## Testing
- [ ] Test with default model set
- [ ] Test with specified model set
- [ ] Test with glance files inclusion
- [ ] Test with philosophy files inclusion
- [ ] Test with both file types included
- [ ] Test with explicit paths
- [ ] Test with mixed options and paths
- [ ] Test error handling conditions
- [ ] Verify correct command construction
- [ ] Test in various directory structures

## Installation and Integration
- [ ] Determine optimal installation location
- [ ] Update installation script to add wrapper to PATH
- [ ] Update documentation to reference new wrapper
- [ ] Test wrapper functionality from various locations

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

