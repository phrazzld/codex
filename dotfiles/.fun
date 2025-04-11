#!/bin/bash

# Detect the current host
HOSTNAME="$(hostname)"

# Universal functions

function timezsh() {
  shell=${1-$SHELL}
  for i in $(seq 1 10); do /usr/bin/time $shell -i -c exit; done
}

function vrg() {
  nvim $(rg -l "$1")
}

function vrgi() {
  nvim $(rg -il "$1")
}

function clear_port() {
  if [ -z "$1" ]; then
    echo "Please specify a port number."
    return 1
  fi

  local PORT=$1
  local PID=$(lsof -i :$PORT | grep LISTEN | awk '{print $2}' | uniq)

  if [ -z "$PID" ]; then
    echo "No process found running on port $PORT."
    return 1
  fi

  echo "Killing process $PID on port $PORT."
  kill -9 $PID
  if [ $? -eq 0 ]; then
    echo "Process on port $PORT killed successfully."
  else
    echo "Failed to kill process on port $PORT."
  fi
}

function conventional_commit() {
  # check if we are inside a git repo
  git rev-parse --is-inside-work-tree > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "fatal: not a git repository (or any of the parent directories): .git."
    return 1
  fi

  # check if we have any changes to commit
  git diff-index --quiet --cached HEAD
  if [ $? -eq 0 ]; then
    echo "fatal: no changes added to commit."
    return 1
  fi

  TYPE=$(gum choose "fix" "feat" "docs" "style" "refactor" "test" "chore" "revert" "ops")
  SCOPE=$(gum input --placeholder "scope")

  # since the scope is optional, wrap it in parentheses if it has a value
  test -n "$SCOPE" && SCOPE="($SCOPE)"

  # pre-populate the input with the type(scope): so that the user may change it
  SUMMARY=$(gum input --value "$TYPE$SCOPE: " --placeholder "summary of this change")
  DESCRIPTION=$(gum write --placeholder "details of this change (CTRL+D to finish)")

  # commit these changes
  echo "\ncommit preview:"
  echo "-----------------"
  echo "$SUMMARY"
  echo "$DESCRIPTION"
  echo "-----------------"
  gum confirm "commit changes?" && git commit -m "$SUMMARY" -m "$DESCRIPTION"
}

# open all modified files in the current working tree
function modified() {
  git status --porcelain | awk '{print $2}' | xargs $EDITOR
}

# Machine-specific functions

# LastPass functions
function pullpasses() {
  if [ -n "$1" ]; then
    lpass show $(lpass ls | grep -i "$1" | awk '{ print $3 }' | sed 's/.$//')
  else
    echo "Error: missing search term"
  fi
}

function pullpass() {
  if [ -n "$1" ]; then
    pullpasses "$1" | grep -i "Password:" | awk '{ print $2 }' | head -1 | pbcopy
  else
    echo "Error: missing search term"
  fi
}

# Encryption functions
function lock() {
  TARFILE=$1
  TARGET_DIR=$2
  tar czf $TARFILE $TARGET_DIR
  gpg -c $TARFILE
  echo "Remember: remove $TARFILE and $TARGET_DIR"
}

function unlock() {
  TARFILE=$1
  GPGFILE=$2
  gpg --output $TARFILE $GPGFILE
  tar xzf $TARFILE
}

# PR review function
function review-pr() {
  # check if we have enough arguments
  if [ $# -lt 3 ]; then
    echo "Usage: review-pr <user> <repo> <pr-number>"
    return 1
  fi

  local user=$1
  local repo=$2
  local pr_number=$3

  $HOME/development/code-review-assistant/code-review-assistant $user/$repo $pr_number --github-token $GITHUB_PERSONAL_ACCESS_TOKEN --openai-key $OPENAI_API_KEY
}
