#!/bin/bash
# tt-common.sh - Robust shared library for all tt-* scripts
# Eliminates code duplication and provides bulletproof cross-platform functionality

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
    local script_name=$(basename "$0")
    echo "Usage: $script_name [options]"
    echo "  $TT_CONFIG_DESCRIPTION"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  --dry-run      Show what would be executed without running"
    echo ""
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
    
    # Add target files if specified
    if [[ -n "$target_files" ]]; then
        read -ra target_array <<< "$target_files"
        cmd_args+=("${target_array[@]}")
    else
        cmd_args+=("$TT_CONFIG_TARGET_DIRECTORY")
    fi
    
    # Add leyline files if found
    if [[ -n "$leyline_files" ]]; then
        read -ra leyline_array <<< "$leyline_files"
        cmd_args+=("${leyline_array[@]}")
    fi
    
    if [[ "$TT_DRY_RUN" == true ]]; then
        echo "DRY RUN - Would execute:"
        echo "thinktank ${cmd_args[*]}"
        echo ""
        if [[ -n "$leyline_files" ]]; then
            echo "Leyline files found: $(echo $leyline_files | wc -w | tr -d ' ') files"
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
    
    # Execute thinktank
    echo "Running thinktank analysis..."
    thinktank "${cmd_args[@]}"
}

# Handle thinktank output robustly
tt_handle_output() {
    # Find the most recent output directory created by thinktank
    local latest_output_dir
    latest_output_dir=$(find . -maxdepth 1 -name "thinktank-*" -type d -newermt '1 minute ago' 2>/dev/null | sort -r | head -1)
    
    if [[ -n "$latest_output_dir" ]]; then
        # Look for the main output file in the directory
        local output_file
        output_file=$(find "$latest_output_dir" -name "*.md" -type f | head -1)
        
        if [[ -n "$output_file" ]]; then
            cp "$output_file" "$TT_CONFIG_OUTPUT_FILE"
            echo "✓ Created $TT_CONFIG_OUTPUT_FILE"
            return 0
        else
            echo "Warning: Could not find output file in $latest_output_dir" >&2
            return 1
        fi
    else
        echo "Warning: Could not find thinktank output directory" >&2
        echo "Make sure thinktank executed successfully" >&2
        return 1
    fi
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