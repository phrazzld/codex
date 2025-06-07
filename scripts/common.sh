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