#!/bin/bash
# Setup Automated Maintenance Script
# Configures cron jobs and validates the maintenance system

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

setup_cron_jobs() {
    log_info "Setting up automated maintenance tasks..."
    
    # Check if cron is available
    if ! command -v crontab >/dev/null 2>&1; then
        log_warn "cron not available - skipping automated scheduling"
        return 1
    fi
    
    # Create temporary crontab file
    local temp_cron=$(mktemp)
    
    # Preserve existing crontab
    crontab -l 2>/dev/null > "$temp_cron" || true
    
    # Remove any existing maintenance entries
    grep -v "system-cleanup-v2.sh\|weekly-reboot.sh" "$temp_cron" > "${temp_cron}.new" || true
    mv "${temp_cron}.new" "$temp_cron"
    
    # Add new maintenance entries
    cat >> "$temp_cron" << EOF

# System Maintenance (added by setup-maintenance.sh)
# Monthly cleanup on 1st of month at 2 AM
0 2 1 * * $SCRIPT_DIR/system-cleanup-v2.sh --no-confirm >> ~/.system-maintenance/logs/cron-cleanup.log 2>&1

# Weekly reboot check on Sundays at 3 AM
0 3 * * 0 $SCRIPT_DIR/weekly-reboot.sh >> ~/.system-maintenance/logs/cron-reboot.log 2>&1

EOF
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would install crontab:"
        cat "$temp_cron"
        rm "$temp_cron"
        return 0
    fi
    
    # Install new crontab
    if crontab "$temp_cron"; then
        log_info "✅ Automated maintenance scheduled:"
        log_info "  - Monthly cleanup: 1st of month at 2:00 AM"
        log_info "  - Weekly reboot check: Sundays at 3:00 AM"
    else
        log_error "Failed to install crontab"
        rm "$temp_cron"
        return 1
    fi
    
    rm "$temp_cron"
}

validate_scripts() {
    log_info "Validating maintenance scripts..."
    
    local scripts=(
        "common.sh"
        "system-cleanup-v2.sh"
        "node-modules-rescue.sh"
        "config.yaml"
    )
    
    local all_valid=true
    
    for script in "${scripts[@]}"; do
        local script_path="$SCRIPT_DIR/$script"
        
        if [[ ! -f "$script_path" ]]; then
            log_error "Missing script: $script_path"
            all_valid=false
            continue
        fi
        
        case "$script" in
            *.sh)
                if ! bash -n "$script_path"; then
                    log_error "Syntax error in: $script"
                    all_valid=false
                else
                    log_info "✓ $script syntax OK"
                fi
                
                if [[ ! -x "$script_path" ]]; then
                    log_warn "Making $script executable..."
                    chmod +x "$script_path"
                fi
                ;;
            config.yaml)
                # Basic YAML validation
                if command -v yq >/dev/null 2>&1; then
                    if yq eval '.' "$script_path" >/dev/null 2>&1; then
                        log_info "✓ $script YAML syntax OK"
                    else
                        log_error "YAML syntax error in: $script"
                        all_valid=false
                    fi
                else
                    log_info "✓ $script exists (install 'yq' for validation)"
                fi
                ;;
        esac
    done
    
    if [[ "$all_valid" == "true" ]]; then
        log_info "✅ All scripts validated successfully"
        return 0
    else
        log_error "❌ Script validation failed"
        return 1
    fi
}

test_dry_runs() {
    log_info "Testing scripts in dry-run mode..."
    
    # Test system cleanup
    log_info "Testing system-cleanup-v2.sh..."
    if "$SCRIPT_DIR/system-cleanup-v2.sh" --dry-run --no-confirm >/dev/null 2>&1; then
        log_info "✓ system-cleanup-v2.sh dry-run OK"
    else
        log_error "✗ system-cleanup-v2.sh dry-run failed"
        return 1
    fi
    
    # Test node modules rescue (if we have a project to test with)
    local dev_dir="$(expand_path "$(get_config 'user.dev_dir' '$HOME/Development')")"
    local test_project=""
    
    # Find a project with package.json for testing
    test_project=$(find "$dev_dir" -name "package.json" -print0 2>/dev/null | head -z -1 | xargs -0 dirname 2>/dev/null || echo "")
    
    if [[ -n "$test_project" && -d "$test_project" ]]; then
        log_info "Testing node-modules-rescue.sh with: $(basename "$test_project")"
        if "$SCRIPT_DIR/node-modules-rescue.sh" --project "$test_project" --dry-run >/dev/null 2>&1; then
            log_info "✓ node-modules-rescue.sh dry-run OK"
        else
            log_error "✗ node-modules-rescue.sh dry-run failed"
            return 1
        fi
    else
        log_info "⚠ No projects found for node-modules-rescue.sh testing"
    fi
    
    log_info "✅ All dry-run tests passed"
}

create_aliases() {
    local aliases_file="$HOME/.maintenance-aliases"
    
    log_info "Creating convenience aliases..."
    
    cat > "$aliases_file" << EOF
# System Maintenance Aliases
# Source this file or add to your shell RC file

alias cleanup='$SCRIPT_DIR/system-cleanup-v2.sh'
alias cleanup-dry='$SCRIPT_DIR/system-cleanup-v2.sh --dry-run'
alias rescue-node='$SCRIPT_DIR/node-modules-rescue.sh --rescue'
alias scan-projects='$SCRIPT_DIR/node-modules-rescue.sh --auto-scan'
alias maintenance-logs='ls -la ~/.system-maintenance/logs/'
alias maintenance-config='cat $SCRIPT_DIR/config.yaml'

# Quick maintenance functions
quick-cleanup() {
    echo "🧹 Running quick system cleanup..."
    $SCRIPT_DIR/system-cleanup-v2.sh --no-confirm
}

fix-bloated-project() {
    if [[ -z "\$1" ]]; then
        echo "Usage: fix-bloated-project <project-path>"
        return 1
    fi
    $SCRIPT_DIR/node-modules-rescue.sh --rescue --project "\$1"
}
EOF
    
    log_info "✅ Aliases created at: $aliases_file"
    log_info "💡 To use them, add this to your shell RC file:"
    log_info "    source $aliases_file"
}

show_setup_summary() {
    cat << EOF

🎉 System Maintenance Setup Complete!

WHAT'S CONFIGURED:
✅ Cross-platform maintenance scripts with safety features
✅ Automated monthly cleanup (1st of month, 2 AM)  
✅ Weekly reboot checks (Sundays, 3 AM)
✅ Dry-run and rollback capabilities
✅ Configurable thresholds and behavior

QUICK COMMANDS:
  cleanup                  # Run system cleanup now
  cleanup-dry             # Preview what would be cleaned
  rescue-node <project>   # Fix bloated node_modules
  scan-projects           # Find projects that need attention

LOGS AND BACKUPS:
  ~/.system-maintenance/logs/     # All operation logs
  ~/.system-maintenance/backups/  # Safety backups
  
CONFIGURATION:
  $SCRIPT_DIR/config.yaml        # Customize behavior

NEXT STEPS:
1. Add aliases to your shell: source ~/.maintenance-aliases
2. Review and customize config.yaml if needed  
3. Test: cleanup-dry
4. Monitor logs after first automated run

EOF
}

main() {
    local remaining_args
    remaining_args=$(parse_common_args "$@")
    
    init_common "setup-maintenance"
    
    log_info "🔧 Setting up system maintenance..."
    
    # Validate all scripts first
    if ! validate_scripts; then
        error "Script validation failed - setup aborted"
    fi
    
    # Test dry runs
    if ! test_dry_runs; then
        error "Dry run tests failed - setup aborted"  
    fi
    
    # Setup cron jobs
    if setup_cron_jobs; then
        log_info "✅ Automated scheduling configured"
    else
        log_warn "⚠ Automated scheduling skipped (you can run scripts manually)"
    fi
    
    # Create aliases
    create_aliases
    
    # Final summary
    show_setup_summary
    
    log_info "🎯 Setup complete! System maintenance is ready."
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi