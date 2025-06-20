# Claude Usage Window Trigger Implementation

## Setup and Preparation Tasks

- [x] Verify Claude Code CLI is installed globally by running `claude --version` in terminal
- [x] Test Claude Code CLI works with basic command `claude -p "hello"` to confirm authentication and connectivity
- [x] Check if `~/bin/` directory exists, create it if missing with `mkdir -p ~/bin`
- [x] Verify `~/bin/` is in PATH by running `echo $PATH | grep "$HOME/bin"` or add to shell profile if needed

## Script Creation Tasks

- [x] Create the main trigger script file at `~/bin/claude-trigger.sh`
- [x] Write shell script content with shebang `#!/bin/bash` at the top
- [x] Add timestamp logging line: `echo "$(date): Triggering Claude usage window" | logger -t claude-trigger`
- [x] Add main Claude command: `claude -p "hello" >> /tmp/claude-trigger.log 2>&1`
- [x] Capture exit code with: `exit_code=$?`
- [x] Add success logging: `if [ $exit_code -eq 0 ]; then echo "$(date): Success" | logger -t claude-trigger`
- [x] Add failure logging: `else echo "$(date): Failed with exit code $exit_code" | logger -t claude-trigger; fi`
- [x] Make script executable with `chmod +x ~/bin/claude-trigger.sh`

## Testing Tasks

- [x] Run manual test of script: `~/bin/claude-trigger.sh`
- [x] Verify script creates log file at `/tmp/claude-trigger.log`
- [x] Check system logs for claude-trigger entries: `log show --predicate 'senderImagePath contains "logger"' --info | grep claude-trigger` (NOTE: log command has syntax issues but logger functionality works)
- [x] Confirm Claude actually responds in the log file by checking `/tmp/claude-trigger.log` contents
- [x] Test script behavior when Claude CLI fails (temporarily break authentication) to verify error handling

## Cron Job Configuration Tasks

- [x] Open crontab editor with `crontab -e`
- [x] Add comment line: `# Claude usage window triggers`
- [x] Add 6:00 AM trigger: `0 6 * * * /bin/bash ~/bin/claude-trigger.sh`
- [x] Add 11:05 AM trigger: `5 11 * * * /bin/bash ~/bin/claude-trigger.sh`
- [x] Add 4:05 PM trigger: `5 16 * * * /bin/bash ~/bin/claude-trigger.sh`
- [x] Add 9:05 PM trigger: `5 21 * * * /bin/bash ~/bin/claude-trigger.sh` (REMOVED per user request)
- [x] Save and exit crontab editor
- [x] Verify crontab entries with `crontab -l`

## Monitoring and Validation Tasks

- [ ] Wait for next scheduled run time and verify execution in system logs
- [ ] Check `/tmp/claude-trigger.log` for actual Claude responses after first automated run
- [ ] Verify usage window timing by making a manual Claude request shortly after trigger time
- [ ] Monitor system logs for any cron errors: `log show --predicate 'subsystem == "com.vix.cron"' --info`
- [ ] Test that usage windows are properly triggered at 6am, 11:05am, 4:05pm, and 9:05pm over several days

## Optional Enhancement Tasks

- [ ] Add log rotation for `/tmp/claude-trigger.log` to prevent it from growing too large
- [ ] Create more descriptive success/failure messages in system logs with actual Claude response status
- [ ] Add environment variable checks in script to ensure proper PATH and authentication
- [ ] Consider adding email notifications for persistent failures (if desired)
- [ ] Document the solution in project CLAUDE.md or README for future reference

## CRITICAL: Migration to launchd (Wake-from-Sleep Support)

**ISSUE IDENTIFIED**: Cron jobs don't run when laptop is closed/sleeping. Need launchd for system wake capability.

### launchd Agent Creation Tasks

- [x] Remove existing cron jobs with `crontab -r` to avoid conflicts
- [x] Create launchd agent directory: `mkdir -p ~/Library/LaunchAgents`
- [x] Create morning trigger plist: `~/Library/LaunchAgents/com.user.claude.morning.plist` (6:00 AM with wake)
- [x] Create midday trigger plist: `~/Library/LaunchAgents/com.user.claude.midday.plist` (11:05 AM with wake)  
- [ ] Create afternoon trigger plist: `~/Library/LaunchAgents/com.user.claude.afternoon.plist` (4:05 PM with wake)
- [ ] Configure each plist with proper wake settings:
  - `StartCalendarInterval` for precise timing
  - `ThrottleInterval` to prevent rapid re-runs
  - `StandardOutPath` and `StandardErrorPath` for logging
  - Proper `ProgramArguments` pointing to our trigger script

### launchd Configuration Details

- [ ] Add wake capability using `RequiresWakeFromSleep` key in each plist
- [ ] Set `RunAtLoad` to false (only run on schedule, not at login)
- [ ] Configure proper logging paths under `/tmp/` for each agent
- [ ] Set appropriate `ProcessType` for background execution

### launchd Deployment and Testing

- [ ] Load morning agent: `launchctl load ~/Library/LaunchAgents/com.user.claude.morning.plist`
- [ ] Load midday agent: `launchctl load ~/Library/LaunchAgents/com.user.claude.midday.plist`
- [ ] Load afternoon agent: `launchctl load ~/Library/LaunchAgents/com.user.claude.afternoon.plist`
- [ ] Verify agents are loaded: `launchctl list | grep claude`
- [ ] Check agent status and next run time: `launchctl print gui/501/com.user.claude.morning`

### Wake-from-Sleep Validation

- [ ] Test manual system sleep and verify agents wake system at scheduled times
- [ ] Close laptop before 6 AM trigger and verify system wakes and executes
- [ ] Monitor system logs for wake events: `log show --predicate 'subsystem == "com.apple.powerd"' --info`
- [ ] Verify Claude usage windows activate even when laptop was closed
- [ ] Test power management settings don't interfere with wake behavior

### System Integration and Permissions

- [ ] Grant necessary permissions for system wake in System Preferences > Security & Privacy
- [ ] Verify Energy Saver settings allow "Wake for network access" if needed
- [ ] Test interaction with Do Not Disturb and Sleep Focus modes
- [ ] Ensure agents respect system sleep schedule and user preferences

## Verification and Cleanup Tasks

- [ ] After one week of successful operation with launchd, confirm usage windows are consistently aligned as expected
- [ ] Verify wake-from-sleep behavior works reliably across different scenarios (closed laptop, external monitor, etc.)
- [ ] Clean up any test files or temporary logs created during setup process
- [ ] Document any issues encountered and solutions for future maintenance
- [ ] Verify the solution doesn't interfere with normal Claude Code usage during development work
- [ ] Create rollback plan in case launchd agents cause issues