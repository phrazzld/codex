#!/bin/bash
# Node Modules Rescue Script v2.0
# Safely fixes bloated/corrupted node_modules with rollback capability

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# === Configuration ===
EXPECTED_SIZE_THRESHOLD_MB=1000  # Flag projects with node_modules > 1GB
RESCUE_TIMEOUT_MINUTES=30        # Max time for rescue operation

# === Project Analysis ===
analyze_project() {
    local project_path="$1"
    
    if [[ ! -d "$project_path" ]]; then
        error "Project directory not found: $project_path"
    fi
    
    if [[ ! -f "$project_path/package.json" ]]; then
        error "No package.json found in: $project_path"
    fi
    
    local project_name=$(basename "$project_path")
    local node_modules_path="$project_path/node_modules"
    
    log_info "=== Analyzing Project: $project_name ==="
    log_info "Path: $project_path"
    
    # Detect package manager
    local package_manager="unknown"
    local lock_file=""
    
    if [[ -f "$project_path/pnpm-lock.yaml" ]]; then
        package_manager="pnpm"
        lock_file="pnpm-lock.yaml"
    elif [[ -f "$project_path/yarn.lock" ]]; then
        package_manager="yarn" 
        lock_file="yarn.lock"
    elif [[ -f "$project_path/package-lock.json" ]]; then
        package_manager="npm"
        lock_file="package-lock.json"
    fi
    
    log_info "Package manager: $package_manager"
    log_info "Lock file: $lock_file"
    
    # Check node_modules size
    local size_mb=0
    local dir_count=0
    
    if [[ -d "$node_modules_path" ]]; then
        size_mb=$(du -sm "$node_modules_path" 2>/dev/null | cut -f1 || echo 0)
        dir_count=$(find "$node_modules_path" -type d 2>/dev/null | wc -l | xargs)
        
        log_info "Current node_modules size: ${size_mb}MB"
        log_info "Directory count: $dir_count"
        
        # Flag if unusually large
        if [[ $size_mb -gt $EXPECTED_SIZE_THRESHOLD_MB ]]; then
            log_warn "⚠️  Unusually large node_modules detected (${size_mb}MB > ${EXPECTED_SIZE_THRESHOLD_MB}MB threshold)"
            return 1  # Indicates rescue needed
        else
            log_info "✅ node_modules size appears normal"
            return 0  # No rescue needed
        fi
    else
        log_info "No node_modules directory found"
        return 2  # Missing node_modules
    fi
}

# === Package Manager Detection & Validation ===
validate_package_manager() {
    local project_path="$1"
    local package_manager="$2"
    
    # Check if package manager is available
    if ! command -v "$package_manager" >/dev/null 2>&1; then
        error "Package manager '$package_manager' not found in PATH"
    fi
    
    # Validate lock file integrity
    case "$package_manager" in
        pnpm)
            if ! pnpm install --dry-run --dir "$project_path" >/dev/null 2>&1; then
                log_warn "pnpm lock file may be corrupted"
                return 1
            fi
            ;;
        yarn)
            if ! yarn check --cwd "$project_path" >/dev/null 2>&1; then
                log_warn "yarn lock file may be corrupted"
                return 1
            fi
            ;;
        npm)
            # npm doesn't have a good dry-run check, so we just verify the file exists
            if [[ ! -f "$project_path/package-lock.json" ]]; then
                log_warn "package-lock.json missing"
                return 1
            fi
            ;;
    esac
    
    return 0
}

# === Rescue Operation ===
rescue_node_modules() {
    local project_path="$1"
    local package_manager="$2"
    local project_name="$(basename "$project_path")"
    
    log_info "=== Starting Rescue Operation for $project_name ==="
    
    # Create comprehensive backup
    local backup_dir="$(expand_path "$(get_config 'user.backup_dir')")/node-modules-rescue"
    local timestamp="$(date +%Y%m%d-%H%M%S)"
    local project_backup="$backup_dir/${project_name}-${timestamp}"
    
    mkdir -p "$project_backup"
    
    log_info "Creating project backup..."
    
    # Backup critical files
    local backup_files=("package.json" "package-lock.json" "yarn.lock" "pnpm-lock.yaml" ".nvmrc" ".node-version")
    for file in "${backup_files[@]}"; do
        if [[ -f "$project_path/$file" ]]; then
            cp "$project_path/$file" "$project_backup/"
            log_info "  ✓ Backed up $file"
        fi
    done
    
    # Backup entire node_modules if it exists
    if [[ -d "$project_path/node_modules" ]]; then
        local size_mb=$(du -sm "$project_path/node_modules" | cut -f1)
        log_info "Creating node_modules backup (${size_mb}MB)..."
        
        if [[ "$DRY_RUN" == "true" ]]; then
            log_info "[DRY RUN] Would backup node_modules to: $project_backup/node_modules.tar.gz"
        else
            # Use tar with compression for large directories
            if tar -czf "$project_backup/node_modules.tar.gz" -C "$project_path" node_modules; then
                log_info "  ✓ node_modules backed up successfully"
            else
                error "Failed to backup node_modules"
            fi
        fi
    fi
    
    # Record current state
    cat > "$project_backup/rescue-info.txt" << EOF
Rescue Operation Info
====================
Project: $project_name
Path: $project_path
Package Manager: $package_manager
Timestamp: $(date)
Original Size: ${size_mb:-0}MB
Rescue Reason: Bloated node_modules detected

Backup Contents:
$(ls -la "$project_backup/")
EOF
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Rescue operation planned:"
        log_info "  1. Remove existing node_modules"
        log_info "  2. Clear package manager cache"
        log_info "  3. Fresh install with $package_manager"
        log_info "  4. Verify installation"
        return 0
    fi
    
    # Confirm before proceeding
    if ! confirm "Proceed with rescue operation for $project_name?"; then
        log_info "Rescue operation cancelled by user"
        return 1
    fi
    
    # Step 1: Remove existing node_modules
    log_info "Step 1: Removing corrupted node_modules..."
    rm -rf "$project_path/node_modules"
    
    # Step 2: Clear package manager cache
    log_info "Step 2: Clearing package manager cache..."
    case "$package_manager" in
        pnpm) pnpm store prune ;;
        yarn) yarn cache clean ;;
        npm) npm cache clean --force ;;
    esac
    
    # Step 3: Fresh installation with timeout
    log_info "Step 3: Performing fresh installation..."
    
    local install_cmd=""
    case "$package_manager" in
        pnpm) install_cmd="pnpm install --dir $project_path" ;;
        yarn) install_cmd="yarn install --cwd $project_path" ;;
        npm) install_cmd="npm install --prefix $project_path" ;;
    esac
    
    log_info "Running: $install_cmd"
    
    # Run with timeout to prevent hanging
    if timeout "${RESCUE_TIMEOUT_MINUTES}m" bash -c "$install_cmd"; then
        log_info "  ✓ Fresh installation completed"
    else
        error "Fresh installation failed or timed out after ${RESCUE_TIMEOUT_MINUTES} minutes"
    fi
    
    # Step 4: Verify installation
    log_info "Step 4: Verifying installation..."
    
    if [[ -d "$project_path/node_modules" ]]; then
        local new_size_mb=$(du -sm "$project_path/node_modules" | cut -f1)
        local new_dir_count=$(find "$project_path/node_modules" -type d | wc -l | xargs)
        
        log_info "  ✓ node_modules recreated successfully"
        log_info "  New size: ${new_size_mb}MB (was ${size_mb:-0}MB)"
        log_info "  Directory count: $new_dir_count"
        
        # Calculate savings
        local saved_mb=$((${size_mb:-0} - new_size_mb))
        if [[ $saved_mb -gt 0 ]]; then
            log_info "  🎉 Rescued ${saved_mb}MB of disk space!"
        fi
        
        # Test basic functionality
        case "$package_manager" in
            pnpm) 
                if pnpm list --dir "$project_path" >/dev/null 2>&1; then
                    log_info "  ✓ pnpm dependency tree is valid"
                else
                    log_warn "  ⚠️  pnpm dependency tree validation failed"
                fi
                ;;
            yarn)
                if yarn check --cwd "$project_path" >/dev/null 2>&1; then
                    log_info "  ✓ yarn dependency tree is valid"
                else
                    log_warn "  ⚠️  yarn dependency tree validation failed"
                fi
                ;;
            npm)
                if npm ls --prefix "$project_path" >/dev/null 2>&1; then
                    log_info "  ✓ npm dependency tree is valid"
                else
                    log_warn "  ⚠️  npm dependency tree validation failed"
                fi
                ;;
        esac
    else
        error "node_modules was not created - installation failed"
    fi
    
    log_info "=== Rescue Operation Complete ==="
    log_info "Backup location: $project_backup"
    log_info "To rollback: Use restore_backup function with backup path"
}

# === Rollback Function ===
rollback_rescue() {
    local backup_path="$1"
    local project_path="$2"
    
    if [[ ! -d "$backup_path" ]]; then
        error "Backup directory not found: $backup_path"
    fi
    
    log_info "=== Rolling Back Rescue Operation ==="
    log_info "Backup: $backup_path"
    log_info "Target: $project_path"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would restore from backup"
        return 0
    fi
    
    if ! confirm "Restore project from backup (this will overwrite current state)?"; then
        log_info "Rollback cancelled by user"
        return 1
    fi
    
    # Restore files
    cp "$backup_path"/*.json "$project_path/" 2>/dev/null || true
    cp "$backup_path"/*.yaml "$project_path/" 2>/dev/null || true
    cp "$backup_path"/*.lock "$project_path/" 2>/dev/null || true
    
    # Restore node_modules if backup exists
    if [[ -f "$backup_path/node_modules.tar.gz" ]]; then
        log_info "Restoring node_modules from backup..."
        rm -rf "$project_path/node_modules"
        tar -xzf "$backup_path/node_modules.tar.gz" -C "$project_path"
        log_info "  ✓ node_modules restored"
    fi
    
    log_info "Rollback complete"
}

# === Main Function ===
main() {
    local remaining_args
    remaining_args=$(parse_common_args "$@")
    
    # Parse script-specific arguments
    local project_path=""
    local operation="analyze"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --project)
                project_path="$2"
                shift 2
                ;;
            --rescue)
                operation="rescue"
                shift
                ;;
            --rollback)
                operation="rollback"
                shift
                ;;
            --auto-scan)
                operation="auto-scan"
                shift
                ;;
            *)
                if [[ -z "$project_path" && -d "$1" ]]; then
                    project_path="$1"
                fi
                shift
                ;;
        esac
    done
    
    init_common "node-modules-rescue"
    
    case "$operation" in
        analyze)
            if [[ -z "$project_path" ]]; then
                error "Usage: $0 [--project] <project-path> [--dry-run]"
            fi
            
            analyze_project "$project_path"
            ;;
        rescue)
            if [[ -z "$project_path" ]]; then
                error "Usage: $0 --rescue [--project] <project-path> [--dry-run]"
            fi
            
            # First analyze to determine if rescue is needed
            if analyze_project "$project_path"; then
                log_info "Project appears healthy - no rescue needed"
                exit 0
            fi
            
            # Detect package manager
            local package_manager="unknown"
            if [[ -f "$project_path/pnpm-lock.yaml" ]]; then
                package_manager="pnpm"
            elif [[ -f "$project_path/yarn.lock" ]]; then
                package_manager="yarn"
            elif [[ -f "$project_path/package-lock.json" ]]; then
                package_manager="npm"
            else
                error "No lock file found - cannot determine package manager"
            fi
            
            validate_package_manager "$project_path" "$package_manager"
            rescue_node_modules "$project_path" "$package_manager"
            ;;
        auto-scan)
            local dev_dir="$(expand_path "$(get_config 'user.dev_dir' '$HOME/Development')")"
            log_info "Auto-scanning projects in: $dev_dir"
            
            local projects_needing_rescue=()
            
            # Find all projects with package.json
            while IFS= read -r -d '' project_dir; do
                local project_name="$(basename "$(dirname "$project_dir")")"
                
                if analyze_project "$(dirname "$project_dir")" >/dev/null 2>&1; then
                    # Return code 1 means rescue needed
                    if [[ $? -eq 1 ]]; then
                        projects_needing_rescue+=("$(dirname "$project_dir")")
                    fi
                fi
            done < <(find "$dev_dir" -name "package.json" -print0 2>/dev/null)
            
            if [[ ${#projects_needing_rescue[@]} -eq 0 ]]; then
                log_info "✅ No projects need rescue"
            else
                log_info "Found ${#projects_needing_rescue[@]} projects that may need rescue:"
                for project in "${projects_needing_rescue[@]}"; do
                    log_info "  - $(basename "$project")"
                done
                
                if confirm "Run rescue operation on all flagged projects?"; then
                    for project in "${projects_needing_rescue[@]}"; do
                        log_info "Processing: $(basename "$project")"
                        "$0" --rescue --project "$project" || log_warn "Rescue failed for $(basename "$project")"
                    done
                fi
            fi
            ;;
        *)
            error "Unknown operation: $operation"
            ;;
    esac
}

# Show help
show_rescue_help() {
    cat << EOF
Node Modules Rescue Script v2.0

USAGE:
    $0 [--project] <path>              # Analyze project
    $0 --rescue [--project] <path>     # Rescue bloated node_modules  
    $0 --auto-scan                     # Scan all projects for issues
    $0 --rollback <backup-path> <project-path>  # Rollback rescue

EXAMPLES:
    $0 ~/Development/my-project                    # Analyze project
    $0 --rescue ~/Development/timeismoney-splash  # Rescue specific project
    $0 --auto-scan --dry-run                      # Preview what would be rescued
    
COMMON OPTIONS:
    --dry-run      Show what would be done without doing it
    --no-backup    Skip backup creation (dangerous!)
    --help         Show this help

The script will:
1. Analyze node_modules size and detect bloat
2. Create comprehensive backups before any changes
3. Safely remove and reinstall dependencies
4. Verify the new installation works correctly
5. Provide rollback capability if needed
EOF
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ "$1" == "--help" || "$1" == "-h" ]]; then
        show_rescue_help
        exit 0
    fi
    
    main "$@"
fi