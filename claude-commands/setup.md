# SETUP

## 1. Verify Environment
- Ensure the `DEVELOPMENT` environment variable is set and points to the root of your project.
- If `DEVELOPMENT` is unset or invalid, exit with an error:
  ```bash
  if [ -z "$DEVELOPMENT" ] || [ ! -d "$DEVELOPMENT" ]; then
    echo "Error: DEVELOPMENT variable not set or not a directory."
    exit 1
  fi
  ```

## 2. Create Symlinks
- Link the central development philosophy:
  ```bash
  ln -sfn "$DEVELOPMENT/codex/docs/DEVELOPMENT_PHILOSOPHY.md" docs/DEVELOPMENT_PHILOSOPHY.md
  ```
- Link the prompts directory:
  ```bash
  ln -sfn "$DEVELOPMENT/codex/docs/prompts" docs/prompts
  ```

## 3. Verify Symlinks
- Confirm both links point to the correct targets:
  ```bash
  ls -l docs/DEVELOPMENT_PHILOSOPHY.md docs/prompts
  ```

## 4. Initialize BACKLOG.md
- Create a BACKLOG.md file if it doesn't exist:
  ```bash
  if [ ! -f "BACKLOG.md" ]; then
    cat > "BACKLOG.md" << EOF
# Project Backlog

## Infrastructure
- [ ] Set up GitHub Actions CI and useful precommit hooks
  * Warn when files are over 500 lines
  * Error when files are over 1000 lines
  * Run tests
  * Run linter
  * Run `glance ./` async on post-commit
EOF
    echo "Created BACKLOG.md with initial tasks"
  fi
  ```
