# Codex Bin Directory

This directory contains utility scripts and tools used within the codex repository.

## Installation

The installation script automatically adds this directory to your PATH. If you need to manually add it:

```bash
# Add this line to your ~/.zshrc or ~/.bashrc to add local bin to PATH
export PATH="$PATH:$HOME/Development/codex/bin"
```

## Utilities

### thinktank-wrapper

A Python-based wrapper around the thinktank CLI that centralizes model configuration, manages prompt templates, and simplifies context file discovery.

**Key Features:**
- Embedded prompt templates (no need for symlinking across repositories)
- Template selection by name with `--template`
- Context injection into templates with `--inject`
- Automatic context file discovery
- Structured logging with correlation IDs
- Backward compatibility with the original Bash implementation

**Usage:**
```bash
thinktank-wrapper [OPTIONS] [CONTEXT_PATHS...]
```

**Common Options:**
- `--template <n>` - Use a named template from the embedded templates
- `--inject <file>` - Inject context from a file into the template's CONTEXT section
- `--list-templates` - List all available templates and exit
- `--model-set <set_name>` - Use predefined model set (all, high_context)
- `--include-glance` - Include glance.md files automatically
- `--include-philosophy` - Include DEVELOPMENT_PHILOSOPHY*.md files automatically
- `--dry-run` - Display the command that would be executed without running it
- `--instructions <file>` - Use an explicit instructions file (overrides --template)
- `-h, --help` - Show help message

**Examples:**
```bash
# Use a template by name
thinktank-wrapper --template plan ./src

# Use a template with injected context
thinktank-wrapper --template debug --inject bug-details.md ./src

# List available templates
thinktank-wrapper --list-templates

# Include glance.md files automatically with a specific template
thinktank-wrapper --template debug --include-glance --model-set high_context

# Include both glance and philosophy files with context injection
thinktank-wrapper --template ideate --inject context.md --include-glance --include-philosophy

# Show command without executing (dry run)
thinktank-wrapper --template review --dry-run file.md

# Backward compatibility with explicit instructions file
thinktank-wrapper --instructions custom-prompt.md --include-philosophy
```

For more detailed documentation, see the [thinktank_wrapper README](./thinktank_wrapper/README.md).

### tt-review

Automated script for generating comprehensive two-pass code reviews using thinktank analysis.

**Usage:**
```bash
tt-review [base_branch]
```

**Parameters:**
- `base_branch` - Branch to compare against (default: auto-detected main/master)

**Features:**
- **Two-pass review process:**
  1. Diff-focused review (bugs, functional issues)
  2. Philosophy alignment review (standards, patterns)
- Automatically generates diff against base branch
- Identifies all changed files (excluding deleted files)
- Runs thinktank-wrapper with specialized templates
- Handles errors gracefully
- Cleans up temporary files

**Examples:**
```bash
# Run full two-pass review against master
tt-review

# Review changes against specific branch
tt-review feature/new-feature
```

**Output:**
- Creates `CODE_REVIEW_DIFF.md` with functional issues analysis
- Creates `CODE_REVIEW_PHILOSOPHY.md` with philosophy alignment review
- Temporarily creates context files (cleaned up on success)

### tt-review-diff

Specialized script for diff-focused code reviews analyzing bugs and functional issues.

**Usage:**
```bash
tt-review-diff [base_branch]
```

**Parameters:**
- `base_branch` - Branch to compare against (default: auto-detected main/master)

**Features:**
- **Filters out deleted files** to prevent "file not found" warnings
- Focuses exclusively on functional issues and bugs
- Uses high_context model set for detailed analysis
- Dramatically reduces token usage by processing only existing files
- Automatically includes leyline documents for context

**Examples:**
```bash
# Run diff-focused review only
tt-review-diff

# Review against specific branch
tt-review-diff develop
```

**Output:**
- Creates `CODE_REVIEW_DIFF.md` with bug and functional issue analysis
- Temporarily creates `REVIEW-CONTEXT.md` (cleaned up on success)

### tt-address

Automated script for generating remediation plans from code review findings.

**Usage:**
```bash
tt-address
```

**Features:**
- Verifies existence of CODE_REVIEW.md
- Creates address context from review content
- Runs thinktank-wrapper with address template
- Uses high_context model set for comprehensive analysis
- Creates REMEDIATION_PLAN.md from synthesis output
- Handles errors gracefully
- Cleans up temporary files

**Workflow:**
1. Run `tt-review` to generate CODE_REVIEW.md
2. Run `tt-address` to create REMEDIATION_PLAN.md

**Examples:**
```bash
# Generate remediation plan from existing review
tt-address
```

**Output:**
- Creates `REMEDIATION_PLAN.md` with actionable implementation steps
- Temporarily creates `ADDRESS-CONTEXT.md` (cleaned up on success)

### tt-ticket

Automated script for generating task breakdowns from implementation plans.

**Usage:**
```bash
tt-ticket [plan_file]
```

**Parameters:**
- `plan_file` - Path to plan file (default: PLAN.md)

**Features:**
- Verifies existence of plan file
- Creates ticket context with task requirements
- Runs thinktank-wrapper with ticket template
- Uses all model set for comprehensive breakdown
- Creates TODO.md from synthesis output
- Provides summary of generated tasks
- Handles errors gracefully
- Cleans up temporary files

**Examples:**
```bash
# Generate tasks from PLAN.md
tt-ticket

# Generate tasks from specific plan file
tt-ticket feature-plan.md
```

**Output:**
- Creates `TODO.md` with atomic, actionable tasks
- Shows task count summary
- Temporarily creates `TICKET-CONTEXT.md` (cleaned up on success)

### tt-shrink

Automated script for analyzing codebase size optimization opportunities.

**Usage:**
```bash
tt-shrink
```

**Features:**
- Checks for existing BACKLOG.md (creates if missing)
- Creates shrink context with current backlog
- Runs thinktank-wrapper with shrink template
- Uses high_context model set for deep analysis
- Generates optimization backlog items from synthesis
- Shows preview of generated items
- Prompts before appending to BACKLOG.md
- Preserves generated items file for reference
- Handles errors gracefully
- Cleans up temporary files

**Examples:**
```bash
# Analyze codebase for size optimization opportunities
tt-shrink
```

**Output:**
- Creates `SHRINK_BACKLOG_ITEMS.md` with optimization tasks
- Optionally appends items to `BACKLOG.md`
- Shows preview of generated items
- Temporarily creates `SHRINK-CONTEXT.md` (cleaned up on success)

### tt-refactor

Automated script for analyzing codebase refactoring opportunities.

**Usage:**
```bash
tt-refactor
```

**Features:**
- Checks for existing BACKLOG.md (creates if missing)
- Creates refactor context with current backlog
- Runs thinktank-wrapper with refactor template
- Uses high_context model set for deep analysis
- Generates refactoring backlog items from synthesis
- Shows preview of generated items
- Prompts before appending to BACKLOG.md
- Preserves generated items file for reference
- Handles errors gracefully
- Cleans up temporary files

**Examples:**
```bash
# Analyze codebase for refactoring opportunities
tt-refactor
```

**Output:**
- Creates `REFACTOR_BACKLOG_ITEMS.md` with refactoring tasks
- Optionally appends items to `BACKLOG.md`
- Shows preview of generated items
- Temporarily creates `REFACTOR-CONTEXT.md` (cleaned up on success)

### tt-plan

Automated script for generating detailed implementation plans from task context.

**Usage:**
```bash
tt-plan
```

**Prerequisites:**
- Must have `PLAN-CONTEXT.md` file with task details

**Features:**
- Verifies existence of PLAN-CONTEXT.md
- Runs thinktank-wrapper with plan template
- Uses high_context model set for comprehensive planning
- Creates PLAN.md from synthesis output
- Shows preview of generated plan
- Reminds about branch creation for implementation
- Handles errors gracefully
- Works with any content format (from sentence fragments to detailed markdown)

**Examples:**
```bash
# Generate plan from existing context
tt-plan
```

**Output:**
- Creates `PLAN.md` with detailed implementation plan
- Shows preview of the plan
- Provides next steps guidance

### tt-ideate

Automated script for generating innovative ideas as backlog items.

**Usage:**
```bash
tt-ideate
```

**Features:**
- No context file needed - analyzes entire codebase directly
- Runs thinktank-wrapper with ideate template
- Uses high_context model set for comprehensive analysis
- Generates backlog-formatted items from synthesis
- Shows preview of generated ideas
- Prompts before appending to BACKLOG.md
- Preserves generated items file for reference
- Handles errors gracefully

**Examples:**
```bash
# Generate innovative backlog ideas
tt-ideate
```

**Output:**
- Creates `IDEATE_BACKLOG_ITEMS.md` with formatted backlog entries
- Optionally appends items to `BACKLOG.md`
- Shows preview of generated ideas

### tt-groom

Automated script for organizing, expanding, and prioritizing the project backlog.

**Usage:**
```bash
tt-groom
```

**Features:**
- Verifies existence of BACKLOG.md
- Creates groom context with current backlog content
- Runs thinktank-wrapper with groom template
- Uses high_context model set with comprehensive codebase analysis
- Creates backup of current backlog before changes
- Shows preview of groomed backlog
- Prompts before replacing current backlog
- Preserves original backlog as backup
- Handles errors gracefully
- Cleans up temporary files

**Workflow:**
1. Creates backup: `BACKLOG.md.backup`
2. Generates groomed version: `BACKLOG.md.groomed`
3. Optionally replaces `BACKLOG.md` with groomed version

**Examples:**
```bash
# Groom and prioritize the backlog
tt-groom
```

**Output:**
- Creates `BACKLOG.md.backup` (original backlog)
- Creates `BACKLOG.md.groomed` (reorganized backlog)
- Optionally updates `BACKLOG.md` with groomed version
- Temporarily creates `GROOM-CONTEXT.md` (cleaned up on success)

### tt-gordian

Automated script for identifying radical simplification opportunities in the codebase.

**Usage:**
```bash
tt-gordian
```

**Philosophy:**
Inspired by Alexander's solution to the Gordian Knot and Elon Musk's principle that "the number one mistake great engineers make is optimizing something that shouldn't exist."

**Features:**
- Analyzes entire codebase for unnecessary complexity
- Runs thinktank-wrapper with gordian template
- Uses high_context model set for deep analysis
- Generates radical simplification recommendations
- Shows preview of analysis results
- Creates GORDIAN_ANALYSIS.md from synthesis
- Handles errors gracefully

**Focus Areas:**
- Components that should be eliminated rather than optimized
- Opportunities for radical simplification
- Unnecessarily complex or tightly coupled code
- Places to "cut the knot" rather than untangle it

**Examples:**
```bash
# Analyze codebase for radical simplification
tt-gordian
```

**Output:**
- Creates `GORDIAN_ANALYSIS.md` with specific, actionable recommendations
- Shows preview of simplification opportunities

### tt-security

Automated script for performing security audits and generating remediation backlog items.

**Usage:**
```bash
tt-security
```

**Features:**
- No context file needed - analyzes entire codebase directly
- Runs thinktank-wrapper with audit template
- Uses high_context model set for thorough analysis
- Generates security backlog items from synthesis
- Groups findings by severity (CRITICAL, HIGH, MEDIUM, LOW)
- Shows preview of security findings
- Prompts before appending to BACKLOG.md
- Preserves findings file for reference
- Handles errors gracefully

**Security Focus:**
- OWASP Top 10 vulnerabilities
- Hardcoded secrets and credentials
- Injection flaws (SQL, XSS, etc.)
- Authentication and authorization issues  
- Input validation vulnerabilities
- Dependency vulnerabilities
- Configuration security

**Examples:**
```bash
# Run security audit and generate backlog items
tt-security
```

**Output:**
- Creates `SECURITY_BACKLOG_ITEMS.md` with prioritized security tasks
- Optionally appends items to `BACKLOG.md`
- Shows preview of security findings with severity levels

### tt-align

Automated script for analyzing codebase alignment with development philosophy.

**Usage:**
```bash
tt-align
```

**Features:**
- Checks for existing BACKLOG.md (creates if missing)
- Creates alignment context with current backlog
- Runs thinktank-wrapper with align template
- Uses high_context model set for comprehensive analysis
- Generates philosophy-aligned backlog items
- Groups items by priority (CRITICAL, HIGH, MEDIUM, LOW)
- Shows preview of alignment findings
- Prompts before appending to BACKLOG.md
- Preserves generated items file for reference
- Handles errors gracefully
- Cleans up temporary files

**Philosophy Areas Analyzed:**
- Simplicity vs complexity
- Modularity and component boundaries
- Separation of concerns
- Testability and structure
- Coding standards compliance
- Error handling consistency
- Security best practices
- Logging structure
- Documentation quality
- Configuration management

**Examples:**
```bash
# Analyze codebase philosophy alignment
tt-align
```

**Output:**
- Creates `ALIGN_BACKLOG_ITEMS.md` with philosophy-driven tasks
- Optionally appends items to `BACKLOG.md`
- Shows preview of highest priority alignment issues