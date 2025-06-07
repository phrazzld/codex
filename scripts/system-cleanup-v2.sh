#!/bin/bash
# Safe System Cleanup Script v2.0
# Cross-platform, configurable, robust maintenance

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# === Configuration ===
DOWNLOADS_AGE_DAYS=""
NODE_MODULES_STALE_DAYS=""
CACHE_RETENTION_DAYS=""
DEV_DIR=""

load_config() {
    DOWNLOADS_AGE_DAYS="$(get_config 'cleanup.downloads_age' '30')"
    NODE_MODULES_STALE_DAYS="$(get_config 'cleanup.node_modules_stale_age' '90')"
    CACHE_RETENTION_DAYS="$(get_config 'cleanup.cache_retention' '7')"
    DEV_DIR="$(expand_path "$(get_config 'user.dev_dir' '$HOME/Development')")"
    
    log_info "Configuration loaded:"
    log_info "  Downloads cleanup age: $DOWNLOADS_AGE_DAYS days"
    log_info "  Node modules stale age: $NODE_MODULES_STALE_DAYS days"
    log_info "  Development directory: $DEV_DIR"
}

# === Cleanup Operations ===
cleanup_downloads() {
    local downloads_dir="$HOME/Downloads"
    
    if [[ ! -d "$downloads_dir" ]]; then
        log_warn "Downloads directory not found: $downloads_dir"
        return 0
    fi
    
    log_info "Scanning Downloads folder for files older than $DOWNLOADS_AGE_DAYS days..."
    
    local old_files
    old_files=$(find "$downloads_dir" -type f -mtime +$DOWNLOADS_AGE_DAYS 2>/dev/null)
    local count=$(echo "$old_files" | grep -c . || echo 0)
    
    if [[ $count -eq 0 ]]; then
        log_info "No old files found in Downloads"
        return 0
    fi
    
    log_info "Found $count files older than $DOWNLOADS_AGE_DAYS days"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would remove $count files:"
        echo "$old_files" | head -10 | while read -r file; do
            log_info "  - $file"
        done
        [[ $count -gt 10 ]] && log_info "  ... and $((count - 10)) more files"
        return 0
    fi
    
    if confirm "Remove $count old files from Downloads?"; then
        local removed=0
        while IFS= read -r file; do
            if [[ -n "$file" && -f "$file" ]]; then
                rm "$file" && ((removed++))
                show_progress $removed $count "Removing old downloads"
            fi
        done <<< "$old_files"
        
        log_info "Successfully removed $removed files from Downloads"
    else
        log_info "Downloads cleanup skipped by user"
    fi
}

cleanup_browser_caches() {
    local os="$(detect_os)"
    local caches_cleaned=0
    
    log_info "Cleaning browser caches..."
    
    # Common browser cache locations by OS
    local cache_dirs=()
    case "$os" in
        macos)
            cache_dirs=(
                "$HOME/Library/Caches/com.brave.Browser"
                "$HOME/Library/Caches/com.google.Chrome"
                "$HOME/Library/Caches/com.apple.Safari"
                "$HOME/Library/Caches/org.mozilla.firefox"
            )
            ;;
        linux)
            cache_dirs=(
                "$HOME/.cache/google-chrome"
                "$HOME/.cache/mozilla/firefox"
                "$HOME/.cache/BraveSoftware/Brave-Browser"
            )
            ;;
        windows)
            cache_dirs=(
                "$HOME/AppData/Local/Google/Chrome/User Data/Default/Cache"
                "$HOME/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Cache"
            )
            ;;
    esac
    
    for cache_dir in "${cache_dirs[@]}"; do
        if [[ -d "$cache_dir" ]]; then
            local size_before=$(du -sm "$cache_dir" 2>/dev/null | cut -f1 || echo 0)
            
            if [[ "$DRY_RUN" == "true" ]]; then
                log_info "[DRY RUN] Would clean cache: $cache_dir (${size_before}MB)"
            else
                log_info "Cleaning cache: $cache_dir (${size_before}MB)"
                rm -rf "$cache_dir"/* 2>/dev/null && ((caches_cleaned++))
            fi
        fi
    done
    
    log_info "Browser cache cleanup complete ($caches_cleaned caches processed)"
}

cleanup_package_manager_caches() {
    local managers=(npm yarn pnpm)
    
    log_info "Cleaning package manager caches..."
    
    for manager in "${managers[@]}"; do
        local enabled="$(get_config "package_managers.${manager}.enabled" 'true')"
        local cache_cmd="$(get_config "package_managers.${manager}.cache_cmd")"
        
        if [[ "$enabled" == "true" ]] && command -v "$manager" >/dev/null 2>&1; then
            log_info "Cleaning $manager cache..."
            
            if [[ "$DRY_RUN" == "true" ]]; then
                log_info "[DRY RUN] Would run: $cache_cmd"
            else
                eval "$cache_cmd" 2>/dev/null || log_warn "Failed to clean $manager cache"
            fi
        fi
    done
}

cleanup_stale_node_modules() {
    if [[ ! -d "$DEV_DIR" ]]; then
        log_warn "Development directory not found: $DEV_DIR"
        return 0
    fi
    
    log_info "Scanning for stale node_modules directories (not modified in $NODE_MODULES_STALE_DAYS days)..."
    
    local stale_dirs=()
    local total_size=0
    
    while IFS= read -r -d '' node_modules_dir; do
        if [[ -d "$node_modules_dir" ]]; then
            local project_dir="$(dirname "$node_modules_dir")"
            local last_modified=$(stat -c %Y "$project_dir" 2>/dev/null || stat -f %m "$project_dir" 2>/dev/null || echo 0)
            local now=$(date +%s)
            local days_old=$(( (now - last_modified) / 86400 ))
            
            if [[ $days_old -gt $NODE_MODULES_STALE_DAYS ]]; then
                local size_mb=$(du -sm "$node_modules_dir" 2>/dev/null | cut -f1 || echo 0)
                stale_dirs+=("$node_modules_dir:$days_old:$size_mb")
                total_size=$((total_size + size_mb))
            fi
        fi
    done < <(find "$DEV_DIR" -name "node_modules" -type d -print0 2>/dev/null)
    
    if [[ ${#stale_dirs[@]} -eq 0 ]]; then
        log_info "No stale node_modules directories found"
        return 0
    fi
    
    log_info "Found ${#stale_dirs[@]} stale node_modules directories (${total_size}MB total)"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would remove:"
        for entry in "${stale_dirs[@]}"; do
            IFS=':' read -r dir days size <<< "$entry"
            log_info "  - $dir ($days days old, ${size}MB)"
        done
        return 0
    fi
    
    if confirm "Remove ${#stale_dirs[@]} stale node_modules directories (${total_size}MB)?"; then
        local removed=0
        for entry in "${stale_dirs[@]}"; do
            IFS=':' read -r dir days size <<< "$entry"
            if safe_remove "$dir" "node_modules-$(basename "$(dirname "$dir")")"; then
                ((removed++))
                show_progress $removed ${#stale_dirs[@]} "Removing stale node_modules"
            fi
        done
        
        log_info "Successfully removed $removed stale node_modules directories"
    else
        log_info "Stale node_modules cleanup skipped by user"
    fi
}

cleanup_system_memory() {
    local os="$(detect_os)"
    local purge_enabled="$(get_config 'system.memory.purge_enabled' 'true')"
    
    if [[ "$purge_enabled" != "true" ]]; then
        log_info "Memory purge disabled in configuration"
        return 0
    fi
    
    log_info "Purging system memory caches..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would purge system memory"
        return 0
    fi
    
    if run_os_command "memory_purge"; then
        log_info "System memory purged successfully"
    else
        log_warn "Failed to purge system memory (may require sudo)"
    fi
}

# === Main Function ===
main() {
    local remaining_args
    remaining_args=$(parse_common_args "$@")
    
    init_common "system-cleanup-v2"
    load_config
    
    # Check dependencies
    check_dependencies "find" "du" "stat"
    
    # Check available disk space (require at least 1GB free)
    check_disk_space 1
    
    log_info "Starting comprehensive system cleanup..."
    log_info "OS: $(detect_os)"
    log_info "Dry run: $DRY_RUN"
    
    # Perform cleanup operations
    cleanup_downloads
    cleanup_browser_caches
    cleanup_package_manager_caches
    cleanup_stale_node_modules
    cleanup_system_memory
    
    # Final summary
    local disk_free_after=$(df -h "$HOME" | awk 'NR==2 {print $4}')
    log_info "=== Cleanup Summary ==="
    log_info "Available disk space: $disk_free_after"
    log_info "Log file: $LOG_FILE"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "This was a DRY RUN - no changes were made"
        log_info "Run without --dry-run to perform actual cleanup"
    fi
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi