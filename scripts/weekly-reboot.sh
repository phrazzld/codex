#!/bin/bash
# Weekly reboot monitor for macOS
# Checks system uptime and notifies user when reboot is recommended

LOG_DIR="$HOME/.system-maintenance"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/reboot-$(date +%Y%m%d-%H%M%S).log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check uptime
UPTIME_DAYS=$(uptime | sed 's/.*up \([0-9]*\) day.*/\1/')

log "=== Weekly Reboot Check ==="
log "Current uptime: $(uptime | awk '{print $3, $4}')"

# Check if reboot is recommended (uptime > 7 days)
if [[ $UPTIME_DAYS -gt 7 ]]; then
    log "System has been up for $UPTIME_DAYS days - reboot recommended"
    
    # Show informational notification (no forced action)
    osascript -e 'display notification "System uptime is '$UPTIME_DAYS' days. Consider rebooting for optimal performance." with title "Weekly Maintenance Reminder"'
    
    log "Notification sent - user can choose when to reboot"
    log "To reboot manually: sudo shutdown -r now"
else
    log "System uptime ($UPTIME_DAYS days) is acceptable - no reboot needed"
fi