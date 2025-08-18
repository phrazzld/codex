#!/bin/bash
# tt-common.sh - Shared library for tt-* scripts

set -e

# Global configuration variables
TT_CONFIG_TEMPLATE_NAME=""
TT_CONFIG_OUTPUT_FILE=""
TT_CONFIG_DESCRIPTION=""
TT_CONFIG_REQUIRES_INPUT_FILE=""
TT_CONFIG_TARGET_DIRECTORY="."
TT_TEMPLATE_CONTENT=""
TT_CONTEXT_CONTENT=""
TT_TARGET_FILES=""
TT_TEMP_DIR=""
TT_DRY_RUN=false
TT_OUTPUT_DIR=""

# Configuration functions
tt_set_config() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --template-name)
                TT_CONFIG_TEMPLATE_NAME="$2"
                shift 2
                ;;
            --output-file)
                TT_CONFIG_OUTPUT_FILE="$2"
                shift 2
                ;;
            --description)
                TT_CONFIG_DESCRIPTION="$2"
                shift 2
                ;;
            --requires-input-file)
                TT_CONFIG_REQUIRES_INPUT_FILE="$2"
                shift 2
                ;;
            --target-directory)
                TT_CONFIG_TARGET_DIRECTORY="$2"
                shift 2
                ;;
            *)
                echo "Unknown config option: $1" >&2
                exit 1
                ;;
        esac
    done
}

tt_set_template() {
    TT_TEMPLATE_CONTENT=$(cat)
}

tt_set_context() {
    TT_CONTEXT_CONTENT="$1"
}

tt_set_target_files() {
    TT_TARGET_FILES="$1"
}

# Bulletproof temp file creation - works on any system
tt_create_temp_files() {
    # Create temp directory instead of relying on mktemp extensions
    TT_TEMP_DIR=$(mktemp -d -t "tt-${TT_CONFIG_TEMPLATE_NAME}-XXXXXX")
    
    # Create instruction file with known name and extension
    local instruction_file="$TT_TEMP_DIR/instructions.md"
    
    # Build the complete instruction content
    local full_content="$TT_TEMPLATE_CONTENT"
    
    # Add context if provided
    if [[ -n "$TT_CONTEXT_CONTENT" ]]; then
        full_content="$TT_TEMPLATE_CONTENT

## Context

$TT_CONTEXT_CONTENT"
    fi
    
    # Write instruction file
    echo "$full_content" > "$instruction_file"
    
    echo "$instruction_file"
}

# Robust cleanup function
tt_cleanup() {
    if [[ -n "$TT_TEMP_DIR" && -d "$TT_TEMP_DIR" ]]; then
        rm -rf "$TT_TEMP_DIR"
    fi
}

# Set up cleanup trap
trap tt_cleanup EXIT INT TERM

# Find leyline documentation files
tt_find_leyline_files() {
    local leyline_files=""
    if [[ -d "./docs/leyline" ]]; then
        leyline_files=$(find ./docs/leyline -name "*.md" -type f 2>/dev/null | tr '\n' ' ' || true)
    fi
    echo "$leyline_files"
}

# Parse command line arguments consistently
tt_parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                tt_show_usage
                exit 0
                ;;
            --dry-run)
                TT_DRY_RUN=true
                shift
                ;;
            *)
                # Pass remaining args back to caller
                echo "$@"
                return
                ;;
        esac
    done
}

# Show usage information
tt_show_usage() {
    local script_name
    script_name=$(basename "$0")
    echo "Usage: $script_name [options] [base_branch]"
    echo "  $TT_CONFIG_DESCRIPTION"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  --dry-run      Show what would be executed without running"
    
    # Add PR option for diff-based reviews
    if [[ "$script_name" =~ ^tt-review- ]]; then
        echo "  --pr <number>  Review a specific PR by number"
    fi
    
    echo ""
    
    if [[ "$script_name" =~ ^tt-review- ]]; then
        echo "Arguments:"
        echo "  base_branch    Branch to compare against (default: auto-detect)"
        echo ""
        echo "Examples:"
        echo "  $script_name                  # Auto-detect PR or use default branch"
        echo "  $script_name --pr 123         # Review specific PR #123"
        echo "  $script_name origin/main      # Compare against origin/main"
        echo "  $script_name --dry-run        # Show what would be done"
        echo ""
    fi
    
    if [[ -n "$TT_CONFIG_REQUIRES_INPUT_FILE" ]]; then
        echo "Requires: $TT_CONFIG_REQUIRES_INPUT_FILE"
        echo ""
    fi
}

# Check for required input files
tt_check_requirements() {
    if [[ -n "$TT_CONFIG_REQUIRES_INPUT_FILE" && ! -f "$TT_CONFIG_REQUIRES_INPUT_FILE" ]]; then
        echo "Error: $TT_CONFIG_REQUIRES_INPUT_FILE not found" >&2
        echo "Please create the required input file first" >&2
        exit 1
    fi
}

# Execute thinktank with robust error handling
tt_execute_thinktank() {
    local instruction_file="$1"
    local target_files="$2"
    local leyline_files="$3"
    
    # Check if thinktank is available
    if ! command -v thinktank >/dev/null 2>&1; then
        echo "Error: thinktank CLI not found in PATH" >&2
        echo "Please install thinktank or ensure it's in your PATH" >&2
        exit 1
    fi
    
    # Build command
    local cmd_args=("$instruction_file")
    
    # Get system temp directory base for validation
    local temp_base
    temp_base=$(dirname "$(mktemp -u)")
    
    # Smart validation for instruction file path
    if [[ "$instruction_file" = /* ]]; then
        # Absolute paths allowed only in temp directory
        if [[ "$instruction_file" != "$temp_base"/* ]] || [[ "$instruction_file" = *..* ]]; then
            echo "Error: Absolute paths only allowed in temp directory" >&2
            return 1
        fi
        # Additional security: check for symlinks
        if [[ -L "$instruction_file" ]]; then
            echo "Error: Symbolic links not allowed for instruction files" >&2
            return 1
        fi
    elif [[ "$instruction_file" = *..* ]]; then
        echo "Error: Path traversal not allowed" >&2
        return 1
    fi
    
    # Add target files if specified
    if [[ -n "$target_files" ]]; then
        read -ra target_array <<< "$target_files"
        # Validate each target file path
        for file in "${target_array[@]}"; do
            if [[ "$file" = /* ]] || [[ "$file" = *..* ]]; then
                echo "Error: Target file paths must be relative without '..' components: $file" >&2
                return 1
            fi
        done
        cmd_args+=("${target_array[@]}")
    else
        cmd_args+=("$TT_CONFIG_TARGET_DIRECTORY")
    fi
    
    # Add leyline files if found
    if [[ -n "$leyline_files" ]]; then
        read -ra leyline_array <<< "$leyline_files"
        # Validate each leyline file path
        for file in "${leyline_array[@]}"; do
            if [[ "$file" = /* ]] || [[ "$file" = *..* ]]; then
                echo "Error: Leyline file paths must be relative without '..' components: $file" >&2
                return 1
            fi
        done
        cmd_args+=("${leyline_array[@]}")
    fi
    
    if [[ "$TT_DRY_RUN" == true ]]; then
        echo "DRY RUN - Would execute:"
        echo "thinktank ${cmd_args[*]}"
        echo ""
        if [[ -n "$leyline_files" ]]; then
            echo "Leyline files found: $(echo "$leyline_files" | wc -w | tr -d ' ') files"
        else
            echo "No leyline files found"
        fi
        echo ""
        echo "Instruction file preview:"
        echo "========================="
        head -30 "$instruction_file"
        echo ""
        echo "[...instruction file continues...]"
        echo ""
        echo "✓ Dry run completed successfully"
        return 0
    fi
    
    # Execute thinktank and capture output while showing in real-time
    echo "Running thinktank analysis..."
    local thinktank_output
    local thinktank_exit_code
    
    # Run thinktank and capture both stdout/stderr while also displaying to user
    # Using tee to show output in real-time via /dev/tty (terminal)
    thinktank_output=$(thinktank "${cmd_args[@]}" 2>&1 | tee /dev/tty)
    thinktank_exit_code=${PIPESTATUS[0]}  # Get exit code of thinktank, not tee
    
    # Handle different exit codes
    # Exit code 0: Complete success
    # Exit code 4: Partial success (some models failed but synthesis completed)
    # Other codes: Failure
    if [[ $thinktank_exit_code -eq 0 ]]; then
        echo "Thinktank completed successfully"
    elif [[ $thinktank_exit_code -eq 4 ]]; then
        echo "Thinktank completed with partial success (some models failed)"
        # Continue to check for synthesis output
    else
        echo "Error: thinktank failed with exit code $thinktank_exit_code" >&2
        return 1
    fi
    
    # Extract the output directory from thinktank's output
    # Look for "Output directory:" or "Outputs saved to:" patterns
    local output_dir
    output_dir=$(echo "$thinktank_output" | grep -E "(Output directory:|Outputs saved to:)" | tail -1 | sed -E 's/.*(thinktank_[0-9]+_[0-9]+_[0-9]+).*/\1/')
    
    if [[ -z "$output_dir" ]]; then
        # Fallback: look for the most recent thinktank directory
        output_dir=$(find . -maxdepth 1 -name "thinktank_*" -type d -mmin -1 2>/dev/null | sort -r | head -1 | xargs basename 2>/dev/null)
    fi
    
    # Check if we found an output directory
    if [[ -n "$output_dir" && -d "$output_dir" ]]; then
        TT_OUTPUT_DIR="$output_dir"
        # Check for synthesis completion
        if [[ "$thinktank_output" =~ "Synthesis: ✓ completed" ]] || [[ "$thinktank_output" =~ synthesis\.md ]]; then
            if [[ $thinktank_exit_code -eq 4 ]]; then
                echo "✓ Synthesis completed despite some model failures"
            else
                echo "✓ Synthesis completed successfully"
            fi
            return 0
        else
            echo "Warning: Output directory found but no synthesis detected" >&2
            echo "Check $output_dir for partial results" >&2
        fi
    else
        echo "Warning: Could not find thinktank output directory" >&2
    fi
    
    # If we got here, we couldn't complete the synthesis
    return 1
}

# Handle thinktank output robustly
tt_handle_output() {
    # Use the output directory we found
    local output_dir="$TT_OUTPUT_DIR"
    
    if [[ -z "$output_dir" ]]; then
        echo "Error: No output directory recorded" >&2
        return 1
    fi
    
    if [[ -d "$output_dir" ]]; then
        # Look specifically for synthesis files first
        local synthesis_file
        synthesis_file=$(find "$output_dir" -name "*-synthesis.md" -type f | head -1)
        
        # If no synthesis file, look for any .md file
        local output_file
        if [[ -n "$synthesis_file" ]]; then
            output_file="$synthesis_file"
        else
            local md_files
            mapfile -t md_files < <(find "$output_dir" -name "*.md" -type f)
            if [[ ${#md_files[@]} -eq 1 ]]; then
                output_file="${md_files[0]}"
            elif [[ ${#md_files[@]} -gt 1 ]]; then
                echo "Warning: Multiple output files found but no synthesis file. Cannot determine correct output." >&2
            fi
        fi
        
        if [[ -n "$output_file" ]]; then
            # Validate output path to prevent path traversal
            if [[ "$TT_CONFIG_OUTPUT_FILE" = /* ]] || [[ "$TT_CONFIG_OUTPUT_FILE" = *..* ]]; then
                echo "Error: Output file must be a relative path without '..' components" >&2
                return 1
            fi
            cp "$output_file" "$TT_CONFIG_OUTPUT_FILE"
            echo "✓ Created $TT_CONFIG_OUTPUT_FILE from $(basename "$output_file")"
            # Don't clean up - user might want to inspect other outputs
            echo "Output directory preserved: $output_dir"
            return 0
        else
            echo "Warning: Could not find output file in $output_dir" >&2
            echo "Directory contents:" >&2
            ls -la "$output_dir" >&2
            return 1
        fi
    else
        echo "Warning: Output directory $output_dir does not exist" >&2
        echo "Current directory contents:" >&2
        ls -d thinktank_* 2>/dev/null || echo "No thinktank directories found" >&2
        return 1
    fi
}

# Get the default git branch (main or master)
tt_get_default_branch() {
    local default_branch
    default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')

    if [[ -n "$default_branch" ]]; then
        echo "$default_branch"
        return
    fi

    if git show-ref --verify --quiet refs/heads/main; then
        if git show-ref --verify --quiet refs/heads/master; then
            echo "master"
        else
            echo "main"
        fi
    elif git show-ref --verify --quiet refs/heads/master; then
        echo "master"
    else
        echo "master"
    fi
}

# Set up a diff-based review with common git operations
# Usage: tt_setup_diff_review "$@"
# This function handles:
# - Argument parsing for base branch and flags
# - Git diff generation with PR awareness
# - Smart base branch detection
# - Context setting with accurate PR details
# - Target files setting
tt_setup_diff_review() {
    # Parse arguments for base branch
    local base_branch=""
    local pr_number=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                tt_show_usage
                exit 0
                ;;
            --dry-run)
                TT_DRY_RUN=true
                shift
                ;;
            --pr)
                pr_number="$2"
                shift 2
                ;;
            *)
                base_branch="$1"
                shift
                ;;
        esac
    done

    # Validate branch name format to prevent command injection
    if [[ -n "$base_branch" ]] && [[ ! "$base_branch" =~ ^[a-zA-Z0-9/_.-]+$ ]]; then
        echo "Error: Invalid branch name format. Only alphanumeric characters, /, _, ., and - are allowed." >&2
        exit 1
    fi

    # Get current branch name
    local current_branch
    current_branch=$(git branch --show-current)

    if [[ -z "$current_branch" ]]; then
        echo "Error: Not on a branch" >&2
        exit 1
    fi

    # Initialize variables for diff content
    local changed_files
    local diff_content
    local file_count
    local comparison_info=""
    local pr_context=""

    # Check if we're in a PR context (either explicit PR number or auto-detect)
    local in_pr_context=false
    local pr_base_branch=""
    
    if command -v gh >/dev/null 2>&1; then
        if [[ -n "$pr_number" ]]; then
            # Explicit PR number provided
            if gh pr view "$pr_number" >/dev/null 2>&1; then
                in_pr_context=true
                pr_info=$(gh pr view "$pr_number" --json baseRefName,headRefName,number,title)
                pr_base_branch=$(echo "$pr_info" | jq -r .baseRefName)
                pr_context="PR #$(echo "$pr_info" | jq -r .number): $(echo "$pr_info" | jq -r .title)"
            else
                echo "Warning: PR #$pr_number not found, falling back to branch comparison" >&2
            fi
        elif gh pr view >/dev/null 2>&1; then
            # Auto-detect current PR
            in_pr_context=true
            pr_info=$(gh pr view --json baseRefName,headRefName,number,title)
            pr_base_branch=$(echo "$pr_info" | jq -r .baseRefName)
            pr_context="PR #$(echo "$pr_info" | jq -r .number): $(echo "$pr_info" | jq -r .title)"
        fi
    fi

    # Determine base branch
    if [[ "$in_pr_context" == true ]] && [[ -n "$pr_base_branch" ]]; then
        base_branch="$pr_base_branch"
        echo "Detected PR context: reviewing against base branch '$base_branch'"
    elif [[ -z "$base_branch" ]]; then
        base_branch=$(tt_get_default_branch)
        echo "No base branch specified, using default: $base_branch"
    fi

    # Fetch latest remote state to ensure accurate comparison
    echo "Fetching latest state of origin/$base_branch..."
    if ! git fetch origin "$base_branch" >/dev/null 2>&1; then
        echo "Warning: Could not fetch origin/$base_branch, using local state" >&2
    fi

    # Use PR diff if available, otherwise use smart git diff
    if [[ "$in_pr_context" == true ]]; then
        echo "Using GitHub PR diff for accurate change detection..."
        
        # Get changed files from PR
        changed_files=$(gh pr diff --name-only 2>/dev/null | while read -r file; do [[ -f "$file" ]] && echo "$file"; done || true)
        
        # Get diff content from PR
        diff_content=$(gh pr diff 2>/dev/null || echo "Failed to get PR diff")
        
        comparison_info="GitHub PR diff (exact PR changes)"
    else
        # Find the merge base for accurate comparison
        local merge_base
        if git rev-parse "origin/$base_branch" >/dev/null 2>&1; then
            merge_base=$(git merge-base "origin/$base_branch" HEAD 2>/dev/null || echo "")
            
            if [[ -n "$merge_base" ]]; then
                echo "Found merge base: ${merge_base:0:8}"
                comparison_info="Merge base ${merge_base:0:8} to HEAD"
                
                # Use three-dot diff to show only changes in current branch
                changed_files=$(git diff --name-only "$merge_base"..HEAD 2>/dev/null | while read -r file; do [[ -f "$file" ]] && echo "$file"; done || true)
                diff_content=$(git diff "$merge_base"..HEAD)
            else
                echo "Warning: Could not find merge base, using direct comparison" >&2
                comparison_info="Direct comparison against origin/$base_branch"
                changed_files=$(git diff --name-only "origin/$base_branch" 2>/dev/null | while read -r file; do [[ -f "$file" ]] && echo "$file"; done || true)
                diff_content=$(git diff "origin/$base_branch")
            fi
        else
            # Fallback to local branch if origin not available
            echo "Warning: origin/$base_branch not found, using local $base_branch" >&2
            comparison_info="Local $base_branch to HEAD"
            changed_files=$(git diff --name-only "$base_branch" 2>/dev/null | while read -r file; do [[ -f "$file" ]] && echo "$file"; done || true)
            diff_content=$(git diff "$base_branch")
        fi
    fi

    if [[ -z "$changed_files" ]]; then
        echo "No changes detected between $current_branch and $base_branch"
        exit 0
    fi

    file_count=$(echo "$changed_files" | wc -l | tr -d ' ')

    echo "Generating review for $file_count files..."
    echo "Comparison: $comparison_info"

    # Set the context with PR details and diff
    local context_header="## Review Context
Current Branch: $current_branch
Base Branch: $base_branch
Comparison: $comparison_info
Files Changed: $file_count"

    if [[ -n "$pr_context" ]]; then
        context_header="$context_header
$pr_context"
    fi

    tt_set_context "$context_header

## Diff
\`\`\`diff
$diff_content
\`\`\`"

    # Set the target files (changed files)
    tt_set_target_files "$(echo "$changed_files" | tr '\n' ' ')"
}

# Main execution function
tt_run() {
    # Validate configuration
    if [[ -z "$TT_CONFIG_TEMPLATE_NAME" || -z "$TT_CONFIG_OUTPUT_FILE" || -z "$TT_CONFIG_DESCRIPTION" ]]; then
        echo "Error: tt_set_config must be called with required parameters" >&2
        exit 1
    fi
    
    if [[ -z "$TT_TEMPLATE_CONTENT" ]]; then
        echo "Error: tt_set_template must be called" >&2
        exit 1
    fi
    
    # Parse arguments
    local remaining_args
    remaining_args=$(tt_parse_args "$@")
    
    # Check requirements
    tt_check_requirements
    
    # Create instruction file
    local instruction_file
    instruction_file=$(tt_create_temp_files)
    
    # Find leyline files
    local leyline_files
    leyline_files=$(tt_find_leyline_files)
    
    # Use target files if set, otherwise use remaining args
    local target_files
    if [[ -n "$TT_TARGET_FILES" ]]; then
        target_files="$TT_TARGET_FILES"
    else
        target_files="$remaining_args"
    fi
    
    # Execute thinktank
    if ! tt_execute_thinktank "$instruction_file" "$target_files" "$leyline_files"; then
        exit 1
    fi
    
    # Handle output (skip for dry run)
    if [[ "$TT_DRY_RUN" != true ]]; then
        if ! tt_handle_output; then
            exit 1
        fi
        
        echo ""
        echo "Analysis complete! See $TT_CONFIG_OUTPUT_FILE"
    fi
}