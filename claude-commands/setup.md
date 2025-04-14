# SETUP

## GOAL
Initialize a new project directory with standard files, documentation, and git repository.

```bash
# Create basic files
echo "# $(basename $(pwd))\n\nAdd project description here." > README.md
echo "# Backlog\n\n- Initial project setup" > BACKLOG.md

# Create directory structure and copy documentation
mkdir -p docs/philosophy docs/prompts
cp "$DEVELOPMENT/codex/docs/DEVELOPMENT_PHILOSOPHY.md" docs/
cp -r "$DEVELOPMENT/codex/docs/philosophy/"* docs/philosophy/
cp -r "$DEVELOPMENT/codex/docs/prompts/"* docs/prompts/

# Initialize git repository
git init

# Create .gitignore with Claude Code specific entries
cat > .gitignore << EOL
# OS specific files
.DS_Store
Thumbs.db

# Editor specific files
.vscode/
.idea/
*.swp
*~

# Claude Code specific files
TODO.md
PLAN.md
*-TASK.md
*-PLAN.md
architect_output/
EOL

echo "✅ Project setup complete. Ready to run Claude Code's /init command."
```