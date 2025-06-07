#!/bin/bash
# Common utilities for system maintenance scripts
# Provides cross-platform, safe, robust functionality

set -euo pipefail

# === Global Variables ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.yaml"
LOCK_FILE="${HOME}/.system-maintenance/maintenance.lock"
LOG_FILE=""
DRY_RUN=false
VERBOSE=false

# === Initialization ===
init_common() {
    local script_name="$1"
    
    # Create required directories
    mkdir -p "${HOME}/.system-maintenance/"{logs,backups,state}
    
    # Set up logging
    LOG_FILE="${HOME}/.system-maintenance/logs/${script_name}-$(date +%Y%m%d-%H%M%S).log"
    
    # Check for lock file
    if [[ -f "$LOCK_FILE" ]]; then
        local lock_pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "unknown")
        if kill -0 "$lock_pid" 2>/dev/null; then
            error "Another maintenance operation is running (PID: $lock_pid)"
            exit 1
        else
            log_warn "Stale lock file found, removing..."
            rm -f "$LOCK_FILE"
        fi
    fi
    
    # Create lock file
    echo $$ > "$LOCK_FILE"
    
    # Set up cleanup trap
    trap cleanup_on_exit EXIT INT TERM
    
    log_info "=== $script_name started ==="
    log_info "PID: $$, Log: $LOG_FILE"
}

cleanup_on_exit() {
    rm -f "$LOCK_FILE"
    if [[ -n "${LOG_FILE:-}" ]]; then
        log_info "=== Script completed ==="
    fi
}

# === OS Detection ===
detect_os() {
    case "$(uname -s)" in
        Darwin*) echo "macos" ;;
        Linux*)  echo "linux" ;;
        MINGW*|CYGWIN*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}

# === Configuration ===
get_config() {
    local key="$1"
    local default="${2:-}"
    
    if command -v yq >/dev/null 2>&1; then
        yq eval ".$key" "$CONFIG_FILE" 2>/dev/null || echo "$default"
    else
        # Fallback for simple config reading without yq
        grep -A 10 "^${key%.*}:" "$CONFIG_FILE" | grep "  ${key##*.}:" | cut -d':' -f2- | xargs || echo "$default"
    fi
}

expand_path() {
    local path="$1"
    echo "${path/\$\{HOME\}/$HOME}"
}

# === Logging ===
log() {
    local level="$1"
    local message="$2"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    local log_line="[$timestamp] [$level] $message"
    
    echo "$log_line" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$1"; }
log_warn() { log "WARN" "$1"; }
log_error() { log "ERROR" "$1"; }

error() {
    log_error "$1"
    exit 1
}

# === Safety Checks ===
check_dependencies() {
    local deps=("$@")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            missing+=("$dep")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing dependencies: ${missing[*]}"
    fi
}

check_disk_space() {
    local required_gb="$1"
    local available_kb=$(df "$HOME" | awk 'NR==2 {print $4}')
    local available_gb=$((available_kb / 1024 / 1024))
    
    if [[ $available_gb -lt $required_gb ]]; then
        error "Insufficient disk space. Required: ${required_gb}GB, Available: ${available_gb}GB"
    fi
}

is_file_in_use() {
    local file="$1"
    local os="$(detect_os)"
    
    case "$os" in
        macos) lsof "$file" >/dev/null 2>&1 ;;
        linux) fuser "$file" >/dev/null 2>&1 ;;
        *) return 1 ;;  # Assume not in use if can't check
    esac
}

# === Backup Functions ===
create_backup() {
    local source="$1"
    local name="${2:-$(basename "$source")}"
    local backup_dir="$(expand_path "$(get_config 'user.backup_dir')")"
    local timestamp="$(date +%Y%m%d-%H%M%S)"
    local backup_path="$backup_dir/${name}-${timestamp}.tar.gz"
    
    if [[ ! -e "$source" ]]; then
        log_warn "Source does not exist: $source"
        return 1
    fi
    
    log_info "Creating backup: $source -> $backup_path"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would create backup: $backup_path"
        return 0
    fi
    
    mkdir -p "$backup_dir"
    if tar -czf "$backup_path" -C "$(dirname "$source")" "$(basename "$source")"; then
        log_info "Backup created successfully: $backup_path"
        echo "$backup_path"  # Return backup path
    else
        error "Failed to create backup: $backup_path"
    fi
}

restore_backup() {
    local backup_path="$1"
    local restore_location="$2"
    
    if [[ ! -f "$backup_path" ]]; then
        error "Backup file not found: $backup_path"
    fi
    
    log_info "Restoring backup: $backup_path -> $restore_location"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would restore backup to: $restore_location"
        return 0
    fi
    
    mkdir -p "$(dirname "$restore_location")"
    if tar -xzf "$backup_path" -C "$(dirname "$restore_location")"; then
        log_info "Backup restored successfully"
    else
        error "Failed to restore backup: $backup_path"
    fi
}

# === Safe File Operations ===
safe_remove() {
    local target="$1"
    local backup_name="${2:-}"
    local always_backup="$(get_config 'safety.always_backup' 'true')"
    
    if [[ ! -e "$target" ]]; then
        log_warn "Target does not exist: $target"
        return 0
    fi
    
    # Check if file is in use
    if is_file_in_use "$target"; then
        error "Cannot remove file in use: $target"
    fi
    
    # Get size and check limits
    local size_gb=0
    if [[ -d "$target" ]]; then
        size_gb=$(du -sg "$target" 2>/dev/null | cut -f1 || echo 0)
    else
        size_gb=$(du -sg "$target" 2>/dev/null | cut -f1 || echo 0)
    fi
    
    local max_single_delete="$(get_config 'safety.max_single_delete_gb' '10')"
    if [[ $size_gb -gt $max_single_delete ]]; then
        log_warn "Large deletion detected: ${size_gb}GB"
        if ! confirm "Delete large amount of data (${size_gb}GB)?"; then
            log_info "Deletion cancelled by user"
            return 1
        fi
    fi
    
    # Create backup if enabled
    local backup_path=""
    if [[ "$always_backup" == "true" ]]; then
        backup_path=$(create_backup "$target" "$backup_name")
    fi
    
    # Perform deletion
    log_info "Removing: $target (${size_gb}GB)"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would remove: $target"
        return 0
    fi
    
    if rm -rf "$target"; then
        log_info "Successfully removed: $target"
        if [[ -n "$backup_path" ]]; then
            log_info "Backup available at: $backup_path"
        fi
    else
        error "Failed to remove: $target"
    fi
}

# === User Interaction ===
confirm() {
    local message="$1"
    local require_confirmation="$(get_config 'safety.require_confirmation' 'true')"
    
    if [[ "$require_confirmation" != "true" ]]; then
        return 0
    fi
    
    echo -n "$message [y/N]: "
    read -r response
    [[ "$response" =~ ^[Yy]$ ]]
}

# === Progress Reporting ===
show_progress() {
    local current="$1"
    local total="$2"
    local operation="$3"
    
    local percent=$((current * 100 / total))
    log_info "Progress: [$current/$total] ($percent%) - $operation"
}

# === Command Execution ===
run_os_command() {
    local command_key="$1"
    shift
    local args=("$@")
    
    local os="$(detect_os)"
    local command="$(get_config "commands.${os}.${command_key}")"
    
    if [[ -z "$command" ]]; then
        log_warn "No command defined for $command_key on $os"
        return 1
    fi
    
    # Replace placeholders in command
    for arg in "${args[@]}"; do
        command="${command/\{$1\}/$arg}"
        shift
    done
    
    log_info "Executing: $command"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would execute: $command"
        return 0
    fi
    
    eval "$command"
}

# === Help Functions ===
show_help() {
    cat << EOF
Common options for all maintenance scripts:

    --dry-run         Show what would be done without doing it
    --verbose         Enable verbose logging
    --no-backup       Skip backup creation (dangerous!)
    --no-confirm      Skip interactive confirmations
    --config FILE     Use custom config file
    --help           Show this help

Configuration file: $CONFIG_FILE
EOF
}

# === Argument Parsing ===
parse_common_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                log_info "DRY RUN mode enabled"
                ;;
            --verbose)
                VERBOSE=true
                set -x
                ;;
            --no-backup)
                # Override config to disable backups
                log_warn "Backup creation disabled!"
                ;;
            --no-confirm)
                # Override config to skip confirmations
                log_warn "Interactive confirmations disabled!"
                ;;
            --config)
                CONFIG_FILE="$2"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                # Unknown option, return to caller
                break
                ;;
        esac
        shift
    done
    
    # Return remaining arguments
    echo "$@"
}

# === Notification System ===
notify_user() {
    local title="$1"
    local message="$2"
    local method="${3:-$(get_config 'notification_methods.default' 'desktop')}"
    
    case "$method" in
        desktop)
            notify_desktop "$title" "$message"
            ;;
        terminal)
            notify_terminal "$title" "$message"
            ;;
        both)
            notify_desktop "$title" "$message"
            notify_terminal "$title" "$message"
            ;;
        *)
            log_warn "Unknown notification method: $method, using terminal"
            notify_terminal "$title" "$message"
            ;;
    esac
}

notify_desktop() {
    local title="$1"
    local message="$2"
    local os="$(detect_os)"
    
    case "$os" in
        macos)
            osascript -e "display notification \"$message\" with title \"$title\""
            ;;
        linux)
            if command -v notify-send >/dev/null 2>&1; then
                notify-send "$title" "$message"
            else
                log_warn "notify-send not available, falling back to terminal"
                notify_terminal "$title" "$message"
            fi
            ;;
        windows)
            powershell "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('$message', '$title')"
            ;;
        *)
            log_warn "Desktop notifications not supported on $os, using terminal"
            notify_terminal "$title" "$message"
            ;;
    esac
}

notify_terminal() {
    local title="$1"
    local message="$2"
    
    echo ""
    echo "🔔 $title"
    echo "   $message"
    echo ""
}

# Interactive user prompt with choices
prompt_user_choice() {
    local title="$1"
    local message="$2"
    local choices="$3"  # e.g., "Yes,No,Postpone"
    local default="${4:-1}"  # Default choice index (1-based)
    local timeout="${5:-0}"  # Timeout in seconds (0 = no timeout)
    
    # Parse choices into array
    IFS=',' read -ra choice_array <<< "$choices"
    local num_choices=${#choice_array[@]}
    
    # Try desktop dialog first
    local response=""
    local os="$(detect_os)"
    
    if [[ "$os" == "macos" ]]; then
        # Build AppleScript buttons
        local buttons=""
        for i in "${!choice_array[@]}"; do
            if [[ $i -eq 0 ]]; then
                buttons="\"${choice_array[$i]}\""
            else
                buttons="$buttons, \"${choice_array[$i]}\""
            fi
        done
        
        local default_button="${choice_array[$((default-1))]}"
        local timeout_clause=""
        if [[ $timeout -gt 0 ]]; then
            timeout_clause=" giving up after $timeout"
        fi
        
        # Use osascript for interactive dialog
        response=$(osascript -e "display dialog \"$message\" with title \"$title\" buttons {$buttons} default button \"$default_button\"$timeout_clause" 2>/dev/null | sed 's/button returned://')
        
        if [[ -n "$response" ]]; then
            echo "$response"
            return 0
        fi
    fi
    
    # Fallback to terminal prompt
    echo ""
    echo "🔔 $title"
    echo "   $message"
    echo ""
    
    for i in "${!choice_array[@]}"; do
        local marker=""
        if [[ $((i+1)) -eq $default ]]; then
            marker=" (default)"
        fi
        echo "   $((i+1))) ${choice_array[$i]}$marker"
    done
    
    echo ""
    if [[ $timeout -gt 0 ]]; then
        echo -n "Choose [1-$num_choices] (timeout in ${timeout}s): "
        if read -t "$timeout" -r choice; then
            echo
        else
            echo
            echo "Timeout reached, using default choice: ${choice_array[$((default-1))]}"
            choice="$default"
        fi
    else
        echo -n "Choose [1-$num_choices]: "
        read -r choice
    fi
    
    # Validate and return choice
    if [[ "$choice" =~ ^[0-9]+$ ]] && [[ $choice -ge 1 ]] && [[ $choice -le $num_choices ]]; then
        echo "${choice_array[$((choice-1))]}"
    else
        echo "${choice_array[$((default-1))]}"
    fi
}

# Confirm with automatic fallback to default after timeout
confirm_with_timeout() {
    local message="$1"
    local timeout="${2:-30}"
    local default="${3:-false}"
    
    local choice
    choice=$(prompt_user_choice "Confirmation Required" "$message" "Yes,No" "$(if [[ "$default" == "true" ]]; then echo 1; else echo 2; fi)" "$timeout")
    
    [[ "$choice" == "Yes" ]]
}

# === Process Detection Functions ===
# Check for running critical processes that might indicate active work

# Get all critical processes from configuration as a flat array
get_critical_processes() {
    local category="${1:-all}"  # all, databases, development, containers, editors, network, custom
    local processes=()
    
    # Helper function to extract array from config using yq
    extract_config_array() {
        local config_key="$1"
        if command -v yq >/dev/null 2>&1; then
            yq eval ".${config_key}[]" "$CONFIG_FILE" 2>/dev/null
        else
            # Fallback: extract using grep (basic YAML parsing)
            local section_key=$(echo "$config_key" | cut -d'.' -f1)
            local array_key=$(echo "$config_key" | cut -d'.' -f2)
            
            # Find the section and extract the array items
            awk "
                /^${section_key}:/ { in_section=1; next }
                /^[a-zA-Z]/ && in_section { in_section=0 }
                in_section && /^  ${array_key}:/ { in_array=1; next }
                in_section && /^  [a-zA-Z]/ && in_array { in_array=0 }
                in_array && /^    - \".*\"/ { 
                    gsub(/^    - \"/, \"\"); 
                    gsub(/\"$/, \"\"); 
                    print 
                }
                in_array && /^    - .*/ { 
                    gsub(/^    - /, \"\"); 
                    print 
                }
            " "$CONFIG_FILE" 2>/dev/null || echo ""
        fi
    }
    
    if [[ "$category" == "all" || "$category" == "databases" ]]; then
        while IFS= read -r process; do
            [[ -n "$process" ]] && processes+=("$process")
        done < <(extract_config_array "critical_processes.databases")
    fi
    
    if [[ "$category" == "all" || "$category" == "development" ]]; then
        while IFS= read -r process; do
            [[ -n "$process" ]] && processes+=("$process")
        done < <(extract_config_array "critical_processes.development")
    fi
    
    if [[ "$category" == "all" || "$category" == "containers" ]]; then
        while IFS= read -r process; do
            [[ -n "$process" ]] && processes+=("$process")
        done < <(extract_config_array "critical_processes.containers")
    fi
    
    if [[ "$category" == "all" || "$category" == "editors" ]]; then
        while IFS= read -r process; do
            [[ -n "$process" ]] && processes+=("$process")
        done < <(extract_config_array "critical_processes.editors")
    fi
    
    if [[ "$category" == "all" || "$category" == "network" ]]; then
        while IFS= read -r process; do
            [[ -n "$process" ]] && processes+=("$process")
        done < <(extract_config_array "critical_processes.network")
    fi
    
    if [[ "$category" == "all" || "$category" == "custom" ]]; then
        while IFS= read -r process; do
            [[ -n "$process" ]] && processes+=("$process")
        done < <(extract_config_array "critical_processes.custom")
    fi
    
    printf '%s\n' "${processes[@]}"
}

# Check if any critical processes are running
check_critical_processes() {
    local category="${1:-all}"
    local running_processes=()
    
    # Get list of critical processes for category  
    local critical_processes=()
    while IFS= read -r process; do
        [[ -n "$process" ]] && critical_processes+=("$process")
    done < <(get_critical_processes "$category")
    
    if [[ ${#critical_processes[@]} -eq 0 ]]; then
        log_warn "No critical processes defined for category: $category"
        return 0
    fi
    
    # Check each critical process
    for process in "${critical_processes[@]}"; do
        if pgrep -f "$process" >/dev/null 2>&1; then
            running_processes+=("$process")
        fi
    done
    
    # Report results
    if [[ ${#running_processes[@]} -gt 0 ]]; then
        log_warn "Found ${#running_processes[@]} critical $category processes running:"
        for process in "${running_processes[@]}"; do
            local pids
            pids=$(pgrep -f "$process" | head -5 | xargs)
            log_warn "  - $process (PIDs: $pids)"
        done
        return 1  # Critical processes found
    else
        log_info "No critical $category processes detected"
        return 0  # No critical processes
    fi
}

# Advanced IDE/editor detection with unsaved file checking
check_critical_editors() {
    local editors_running=()
    local unsaved_work_detected=false
    
    log_info "Checking for running editors and unsaved work..."
    
    # Get editor processes from configuration
    local editor_processes=()
    while IFS= read -r process; do
        [[ -n "$process" ]] && editor_processes+=("$process")
    done < <(get_critical_processes "editors")
    
    # Check each editor
    for editor in "${editor_processes[@]}"; do
        if pgrep -f "$editor" >/dev/null 2>&1; then
            editors_running+=("$editor")
            log_info "Detected running editor: $editor"
            
            # Check for unsaved work based on editor type
            case "$editor" in
                "code"|"cursor")
                    # VS Code / Cursor: Check for backup files or workspace state
                    if check_vscode_unsaved_work; then
                        unsaved_work_detected=true
                        log_warn "  - VS Code/Cursor may have unsaved work"
                    fi
                    ;;
                "vim"|"nvim")
                    # Vim: Check for swap files
                    if check_vim_unsaved_work; then
                        unsaved_work_detected=true
                        log_warn "  - Vim/Neovim may have unsaved work"
                    fi
                    ;;
                "emacs")
                    # Emacs: Check for backup/auto-save files
                    if check_emacs_unsaved_work; then
                        unsaved_work_detected=true
                        log_warn "  - Emacs may have unsaved work"
                    fi
                    ;;
                *)
                    # Generic editor: Just warn about running process
                    log_warn "  - $editor is running (cannot detect unsaved work)"
                    ;;
            esac
        fi
    done
    
    # Summary
    if [[ ${#editors_running[@]} -gt 0 ]]; then
        log_warn "Found ${#editors_running[@]} editor(s) running: ${editors_running[*]}"
        if [[ "$unsaved_work_detected" == "true" ]]; then
            log_warn "⚠️  Potential unsaved work detected - proceed with caution"
            return 2  # Editors with potential unsaved work
        else
            log_info "No unsaved work detected, but editors are running"
            return 1  # Editors running but no unsaved work detected
        fi
    else
        log_info "No critical editors detected"
        return 0  # No editors running
    fi
}

# VS Code unsaved work detection
check_vscode_unsaved_work() {
    # Check for VS Code backup/workspace files that might indicate unsaved work
    local vscode_dirs=(
        "$HOME/Library/Application Support/Code/User/workspaceStorage"
        "$HOME/Library/Application Support/Cursor/User/workspaceStorage"
        "$HOME/.vscode"
        "$HOME/.cursor"
    )
    
    for dir in "${vscode_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            # Look for recent backup files (modified in last 60 minutes)
            if find "$dir" -name "*.json" -o -name "*.backup" -mmin -60 2>/dev/null | head -1 | grep -q .; then
                return 0  # Found potential unsaved work
            fi
        fi
    done
    
    return 1  # No unsaved work detected
}

# Vim unsaved work detection
check_vim_unsaved_work() {
    # Check for vim swap files in common locations
    local swap_patterns=(
        "*.swp"
        "*.swo" 
        "*.swn"
        ".*.swp"
        ".*.swo"
        ".*.swn"
    )
    
    local search_dirs=(
        "$HOME"
        "$HOME/.vim"
        "$HOME/.config/nvim"
        "$(get_config 'user.dev_dir' '$HOME/Development')"
        "/tmp"
    )
    
    for dir in "${search_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            for pattern in "${swap_patterns[@]}"; do
                if find "$dir" -name "$pattern" -mmin -60 2>/dev/null | head -1 | grep -q .; then
                    return 0  # Found swap files
                fi
            done
        fi
    done
    
    return 1  # No swap files found
}

# Emacs unsaved work detection  
check_emacs_unsaved_work() {
    # Check for emacs backup and auto-save files
    local backup_patterns=(
        "*~"     # Backup files
        "#*#"    # Auto-save files
        ".#*"    # Lock files
    )
    
    local search_dirs=(
        "$HOME"
        "$(get_config 'user.dev_dir' '$HOME/Development')"
    )
    
    for dir in "${search_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            for pattern in "${backup_patterns[@]}"; do
                if find "$dir" -name "$pattern" -mmin -60 2>/dev/null | head -1 | grep -q .; then
                    return 0  # Found backup/auto-save files
                fi
            done
        fi
    done
    
    return 1  # No backup files found
}

# === User Presence Detection Functions ===
# Detect if user is actively using the system before disruptive operations

# Main user presence detection function
check_user_presence() {
    local enabled="$(get_config 'user_presence.enabled' 'true')"
    
    if [[ "$enabled" != "true" ]]; then
        log_info "User presence detection disabled"
        return 0  # Assume present when disabled
    fi
    
    log_info "Checking user presence..."
    
    local presence_indicators=()
    local absence_indicators=()
    local uncertain_indicators=()
    
    # Check each detection method
    if [[ "$(get_config 'user_presence.methods.idle_time' 'true')" == "true" ]]; then
        case $(check_system_idle_time) in
            0) presence_indicators+=("system active (low idle time)") ;;
            1) absence_indicators+=("system idle for extended period") ;;
            2) uncertain_indicators+=("unable to determine idle time") ;;
        esac
    fi
    
    if [[ "$(get_config 'user_presence.methods.active_sessions' 'true')" == "true" ]]; then
        case $(check_active_sessions) in
            0) presence_indicators+=("active terminal/SSH sessions") ;;
            1) absence_indicators+=("no active sessions found") ;;
            2) uncertain_indicators+=("session detection inconclusive") ;;
        esac
    fi
    
    if [[ "$(get_config 'user_presence.methods.recent_files' 'true')" == "true" ]]; then
        case $(check_recent_file_activity) in
            0) presence_indicators+=("recent file modifications detected") ;;
            1) absence_indicators+=("no recent file activity") ;;
            2) uncertain_indicators+=("file activity detection uncertain") ;;
        esac
    fi
    
    if [[ "$(get_config 'user_presence.methods.running_processes' 'true')" == "true" ]]; then
        case $(check_interactive_processes) in
            0) presence_indicators+=("interactive processes running") ;;
            1) absence_indicators+=("no recent interactive processes") ;;
            2) uncertain_indicators+=("process detection uncertain") ;;
        esac
    fi
    
    # Analyze results
    local total_indicators=$((${#presence_indicators[@]} + ${#absence_indicators[@]}))
    local presence_score=${#presence_indicators[@]}
    
    # Log findings
    if [[ ${#presence_indicators[@]} -gt 0 ]]; then
        log_info "User presence indicators found:"
        for indicator in "${presence_indicators[@]}"; do
            log_info "  ✓ $indicator"
        done
    fi
    
    if [[ ${#absence_indicators[@]} -gt 0 ]]; then
        log_info "User absence indicators found:"
        for indicator in "${absence_indicators[@]}"; do
            log_info "  ✗ $indicator"
        done
    fi
    
    if [[ ${#uncertain_indicators[@]} -gt 0 ]]; then
        log_warn "Uncertain presence indicators:"
        for indicator in "${uncertain_indicators[@]}"; do
            log_warn "  ? $indicator"
        done
    fi
    
    # Determine presence
    local assume_present_on_error="$(get_config 'user_presence.fallback.assume_present_on_error' 'true')"
    local prompt_on_uncertainty="$(get_config 'user_presence.fallback.prompt_on_uncertainty' 'true')"
    
    if [[ $total_indicators -eq 0 ]]; then
        log_warn "No presence detection methods available"
        if [[ "$assume_present_on_error" == "true" ]]; then
            log_info "Assuming user is present (safer default)"
            return 0
        else
            return 1
        fi
    fi
    
    # Calculate presence confidence
    local presence_percentage=$((presence_score * 100 / total_indicators))
    log_info "User presence confidence: ${presence_percentage}% ($presence_score/$total_indicators indicators)"
    
    # Decision logic
    if [[ $presence_percentage -ge 75 ]]; then
        log_info "High confidence: User is present"
        return 0  # User present
    elif [[ $presence_percentage -le 25 ]]; then
        log_info "High confidence: User is away"
        return 1  # User absent
    else
        log_warn "Uncertain user presence (${presence_percentage}% confidence)"
        if [[ "$prompt_on_uncertainty" == "true" ]]; then
            log_info "Will prompt user due to uncertain presence"
            return 2  # Uncertain - should prompt
        elif [[ "$assume_present_on_error" == "true" ]]; then
            log_info "Assuming user is present due to uncertainty"
            return 0  # Assume present
        else
            log_info "Assuming user is absent due to uncertainty"
            return 1  # Assume absent
        fi
    fi
}

# Check system idle time
check_system_idle_time() {
    local max_idle_minutes="$(get_config 'user_presence.thresholds.max_idle_minutes' '15')"
    local os="$(detect_os)"
    local idle_seconds=0
    
    case "$os" in
        macos)
            # Use ioreg to get idle time on macOS
            idle_seconds=$(ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print int($NF/1000000000); exit}' 2>/dev/null || echo 0)
            ;;
        linux)
            # Use various methods to detect idle time on Linux
            if command -v xprintidle >/dev/null 2>&1; then
                idle_seconds=$(($(xprintidle) / 1000))
            elif [[ -n "$DISPLAY" ]] && command -v xset >/dev/null 2>&1; then
                idle_seconds=$(xset q | grep timeout | awk '{print $2}' || echo 0)
            else
                log_warn "Cannot determine idle time on Linux (no xprintidle or xset)"
                return 2
            fi
            ;;
        *)
            log_warn "Idle time detection not supported on $os"
            return 2
            ;;
    esac
    
    # Ensure idle_seconds is a valid integer
    if ! [[ "$idle_seconds" =~ ^[0-9]+$ ]]; then
        log_warn "Invalid idle time value: $idle_seconds"
        return 2
    fi
    
    local idle_minutes=$((idle_seconds / 60))
    log_info "System idle time: ${idle_minutes} minutes"
    
    if [[ $idle_minutes -gt $max_idle_minutes ]]; then
        log_info "System idle for $idle_minutes minutes (> $max_idle_minutes minute threshold)"
        return 1  # User appears absent
    else
        log_info "System active (idle for only $idle_minutes minutes)"
        return 0  # User appears present
    fi
}

# Check for active terminal/SSH sessions
check_active_sessions() {
    local active_sessions=()
    
    # Check for active SSH sessions
    local current_tty=$(tty 2>/dev/null | sed 's|/dev/||' || echo "unknown")
    local ssh_sessions=$(who | grep -E 'pts|tty' | grep -v "$current_tty" | wc -l | xargs)
    if [[ "$ssh_sessions" =~ ^[0-9]+$ ]] && [[ $ssh_sessions -gt 0 ]]; then
        active_sessions+=("$ssh_sessions SSH/terminal sessions")
    fi
    
    # Check for screen/tmux sessions
    local screen_sessions=$(screen -ls 2>/dev/null | grep -c "Attached\|Detached" || echo 0)
    if [[ "$screen_sessions" =~ ^[0-9]+$ ]] && [[ $screen_sessions -gt 0 ]]; then
        active_sessions+=("$screen_sessions screen sessions")
    fi
    
    local tmux_sessions=$(tmux list-sessions 2>/dev/null | wc -l | xargs || echo 0)
    if [[ "$tmux_sessions" =~ ^[0-9]+$ ]] && [[ $tmux_sessions -gt 0 ]]; then
        active_sessions+=("$tmux_sessions tmux sessions")
    fi
    
    if [[ ${#active_sessions[@]} -gt 0 ]]; then
        log_info "Active sessions detected: ${active_sessions[*]}"
        return 0  # User present
    else
        log_info "No active sessions detected"
        return 1  # User absent
    fi
}

# Check for recent file activity in development directories
check_recent_file_activity() {
    local recent_minutes="$(get_config 'user_presence.thresholds.recent_file_minutes' '30')"
    local dev_dir="$(expand_path "$(get_config 'user.dev_dir' '$HOME/Development')")"
    local home_dir="$(expand_path "$(get_config 'user.home_dir' '$HOME')")"
    
    local search_dirs=("$dev_dir" "$home_dir/Documents" "$home_dir/Desktop")
    local recent_files=0
    
    for dir in "${search_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            local count
            count=$(find "$dir" -type f -mmin -"$recent_minutes" 2>/dev/null | head -10 | wc -l)
            recent_files=$((recent_files + count))
        fi
    done
    
    if [[ $recent_files -gt 0 ]]; then
        log_info "Found $recent_files files modified in last $recent_minutes minutes"
        return 0  # User present
    else
        log_info "No files modified in last $recent_minutes minutes"
        return 1  # User absent
    fi
}

# Check for interactive user processes
check_interactive_processes() {
    local process_minutes="$(get_config 'user_presence.thresholds.process_check_minutes' '5')"
    local interactive_processes=()
    
    # Look for recently started interactive processes
    local current_time=$(date +%s)
    local threshold_time=$((current_time - process_minutes * 60))
    
    # Check for shell processes, editors, browsers started recently
    local interactive_patterns=("bash" "zsh" "fish" "vim" "emacs" "code" "chrome" "firefox" "safari")
    
    for pattern in "${interactive_patterns[@]}"; do
        # Get processes with start time (macOS specific for now)
        local os="$(detect_os)"
        if [[ "$os" == "macos" ]]; then
            local recent_pids
            recent_pids=$(ps -eo pid,lstart,comm | grep "$pattern" | while read -r pid lstart comm; do
                # Convert lstart to epoch time (simplified)
                local start_epoch
                start_epoch=$(date -j -f "%a %b %d %H:%M:%S %Y" "$lstart" "+%s" 2>/dev/null || echo 0)
                if [[ $start_epoch -gt $threshold_time ]]; then
                    echo "$pid"
                fi
            done)
            
            if [[ -n "$recent_pids" ]]; then
                local count
                count=$(echo "$recent_pids" | wc -l)
                interactive_processes+=("$count recent $pattern processes")
            fi
        else
            # Fallback: just check if processes are running
            if pgrep "$pattern" >/dev/null 2>&1; then
                interactive_processes+=("$pattern processes running")
            fi
        fi
    done
    
    if [[ ${#interactive_processes[@]} -gt 0 ]]; then
        log_info "Interactive processes detected: ${interactive_processes[*]}"
        return 0  # User present
    else
        log_info "No recent interactive processes detected"
        return 1  # User absent
    fi
}