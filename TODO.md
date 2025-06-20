# Claude Usage Window Trigger Implementation

## Setup and Preparation Tasks

- [x] Verify Claude Code CLI is installed globally by running `claude --version` in terminal
- [x] Test Claude Code CLI works with basic command `claude -p "hello"` to confirm authentication and connectivity
- [ ] Check if `~/bin/` directory exists, create it if missing with `mkdir -p ~/bin`
- [ ] Verify `~/bin/` is in PATH by running `echo $PATH | grep "$HOME/bin"` or add to shell profile if needed

## Script Creation Tasks

- [ ] Create the main trigger script file at `~/bin/claude-trigger.sh`
- [ ] Write shell script content with shebang `#!/bin/bash` at the top
- [ ] Add timestamp logging line: `echo "$(date): Triggering Claude usage window" | logger -t claude-trigger`
- [ ] Add main Claude command: `claude -p "hello" >> /tmp/claude-trigger.log 2>&1`
- [ ] Capture exit code with: `exit_code=$?`
- [ ] Add success logging: `if [ $exit_code -eq 0 ]; then echo "$(date): Success" | logger -t claude-trigger`
- [ ] Add failure logging: `else echo "$(date): Failed with exit code $exit_code" | logger -t claude-trigger; fi`
- [ ] Make script executable with `chmod +x ~/bin/claude-trigger.sh`

## Testing Tasks

- [ ] Run manual test of script: `~/bin/claude-trigger.sh`
- [ ] Verify script creates log file at `/tmp/claude-trigger.log`
- [ ] Check system logs for claude-trigger entries: `log show --predicate 'senderImagePath contains "logger"' --info | grep claude-trigger`
- [ ] Confirm Claude actually responds in the log file by checking `/tmp/claude-trigger.log` contents
- [ ] Test script behavior when Claude CLI fails (temporarily break authentication) to verify error handling

## Cron Job Configuration Tasks

- [ ] Open crontab editor with `crontab -e`
- [ ] Add comment line: `# Claude usage window triggers`
- [ ] Add 6:00 AM trigger: `0 6 * * * /bin/bash ~/bin/claude-trigger.sh`
- [ ] Add 11:05 AM trigger: `5 11 * * * /bin/bash ~/bin/claude-trigger.sh`
- [ ] Add 4:05 PM trigger: `5 16 * * * /bin/bash ~/bin/claude-trigger.sh`
- [ ] Add 9:05 PM trigger: `5 21 * * * /bin/bash ~/bin/claude-trigger.sh`
- [ ] Save and exit crontab editor
- [ ] Verify crontab entries with `crontab -l`

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

## Verification and Cleanup Tasks

- [ ] After one week of successful operation, confirm usage windows are consistently aligned as expected
- [ ] Clean up any test files or temporary logs created during setup process
- [ ] Document any issues encountered and solutions for future maintenance
- [ ] Verify the solution doesn't interfere with normal Claude Code usage during development work