#!/bin/bash
# Weekly reboot monitor for macOS
# Checks system uptime and provides interactive reboot options

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# === Main Function ===
main() {
    local remaining_args
    remaining_args=$(parse_common_args "$@")
    
    init_common "weekly-reboot"
    
    # Get configuration
    local max_uptime_days="$(get_config 'system.reboot.max_uptime_days' '7')"
    local notification_timeout="$(get_config 'notification_methods.timeout_seconds' '30')"
    local notification_method="$(get_config 'notification_methods.reboot_prompt' 'both')"
    
    # Check uptime
    local uptime_days=$(uptime | sed 's/.*up \([0-9]*\) day.*/\1/' || echo 0)
    
    log_info "=== Weekly Reboot Check ==="
    log_info "Current uptime: $(uptime | awk '{print $3, $4}')"
    log_info "Maximum recommended uptime: $max_uptime_days days"
    
    # Check if reboot is recommended
    if [[ $uptime_days -gt $max_uptime_days ]]; then
        log_info "System has been up for $uptime_days days - reboot recommended"
        
        local message="System uptime is $uptime_days days (exceeds $max_uptime_days day limit). 
        
Reboot recommended for optimal performance and security updates.

What would you like to do?"
        
        if [[ "$DRY_RUN" == "true" ]]; then
            log_info "[DRY RUN] Would prompt user for reboot action"
            notify_user "Weekly Maintenance" "DRY RUN: Would prompt for reboot decision" "$notification_method"
            return 0
        fi
        
        # Interactive prompt for user choice
        local choice
        choice=$(prompt_user_choice "Weekly Maintenance - Reboot Recommended" "$message" "Reboot Now,Postpone 4 Hours,Postpone 24 Hours,Cancel" "2" "$notification_timeout")
        
        log_info "User choice: $choice"
        
        case "$choice" in
            "Reboot Now")
                log_info "User chose to reboot immediately"
                notify_user "Weekly Maintenance" "Reboot initiated by user request" "terminal"
                log_info "Executing: sudo shutdown -r +1"
                sudo shutdown -r +1 "Weekly maintenance reboot - user requested"
                ;;
            "Postpone 4 Hours")
                log_info "User chose to postpone reboot for 4 hours"
                notify_user "Weekly Maintenance" "Reboot postponed for 4 hours" "desktop"
                # Schedule reboot in 4 hours
                echo "$0" | at now + 4 hours 2>/dev/null || \
                    log_warn "Could not schedule postponed reboot (at command not available)"
                ;;
            "Postpone 24 Hours")
                log_info "User chose to postpone reboot for 24 hours"
                notify_user "Weekly Maintenance" "Reboot postponed for 24 hours" "desktop"
                # Schedule reboot in 24 hours
                echo "$0" | at now + 24 hours 2>/dev/null || \
                    log_warn "Could not schedule postponed reboot (at command not available)"
                ;;
            "Cancel")
                log_info "User cancelled reboot recommendation"
                notify_user "Weekly Maintenance" "Reboot cancelled - remember to reboot manually when convenient" "desktop"
                ;;
            *)
                log_warn "Unknown choice: $choice, treating as cancel"
                notify_user "Weekly Maintenance" "No valid choice made - reboot cancelled" "desktop"
                ;;
        esac
    else
        log_info "System uptime ($uptime_days days) is acceptable - no reboot needed"
        
        # Optional notification for good status
        if [[ "$(get_config 'notification_methods.notify_on_good_status' 'false')" == "true" ]]; then
            notify_user "Weekly Maintenance" "System uptime is healthy ($uptime_days days)" "desktop"
        fi
    fi
    
    log_info "Weekly reboot check completed"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi