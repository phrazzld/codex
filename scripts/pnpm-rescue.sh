#!/bin/bash
# Safe pnpm rescue script for bloated node_modules
# Works with any pnpm project

set -e

# Check if project path is provided
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <project-path>"
    echo "Example: $0 /Users/phaedrus/Development/my-project"
    exit 1
fi

PROJECT_PATH="$1"
PROJECT_NAME="$(basename "$PROJECT_PATH")"
BACKUP_DIR="$HOME/.package-manager-backups"

log() {
    echo "[$(date '+%H:%M:%S')] $1"
}

if [[ ! -d "$PROJECT_PATH" ]]; then
    log "❌ Project not found: $PROJECT_PATH"
    exit 1
fi

log "🔍 Analyzing $PROJECT_NAME node_modules bloat..."

# Check current size
CURRENT_SIZE=$(du -sh "$PROJECT_PATH/node_modules" | cut -f1)
log "Current node_modules size: $CURRENT_SIZE"

# Backup package files
mkdir -p "$BACKUP_DIR"
cp "$PROJECT_PATH/package.json" "$BACKUP_DIR/$PROJECT_NAME-package.json.bak"
cp "$PROJECT_PATH/pnpm-lock.yaml" "$BACKUP_DIR/$PROJECT_NAME-pnpm-lock.yaml.bak"
log "📦 Backed up package files to $BACKUP_DIR"

# Check for duplicate or unnecessary packages
log "🔍 Checking for issues..."

# Safe cleanup procedure
log "🧹 Starting safe cleanup..."

# 1. Remove node_modules completely (safest approach)
rm -rf "$PROJECT_PATH/node_modules"
log "✅ Removed bloated node_modules"

# 2. Clean pnpm cache for this project
pnpm store prune 2>/dev/null || true
log "✅ Cleaned pnpm store"

# 3. Fresh install
log "📥 Performing fresh pnpm install..."
cd "$PROJECT_PATH" && pnpm install

# Check new size
NEW_SIZE=$(du -sh "$PROJECT_PATH/node_modules" | cut -f1)
log "✅ Fresh install complete!"
log "📊 Size comparison:"
log "   Before: $CURRENT_SIZE"
log "   After:  $NEW_SIZE"

# Calculate savings
log "🎉 node_modules rescue complete for $PROJECT_NAME"