# Project Organization Guide

Your new project management system for tracking ideas, active work, and shipped projects.

## Quick Start

### View Projects

```bash
# Interactive fuzzy search (requires fzf)
projects

# List all projects
projects list

# Show only active projects
projects active

# Show ideas only
projects ideas

# Show statistics
projects stats
```

### Maintain the Registry

1. **Edit directly in nvim:**
   ```bash
   nvim ~/Development/codex/docs/projects.md
   ```

2. **Check for sync issues:**
   ```bash
   projects sync
   ```
   This will show repos not in the registry and registry entries without local repos.

3. **Find available names:**
   ```bash
   projects name my-new-project
   ```

### Add a New Project

1. Open `docs/projects.md` in your editor
2. Add row to appropriate section (Ideas, Active, etc.)
3. Format: `| name | description | status | repo | tags |`
4. If needed, create detailed project file: `docs/projects/name.md`

### Flesh Out an Idea

When ready to develop an idea:

1. Create detailed project file:
   ```bash
   nvim ~/Development/codex/docs/projects/project-name.md
   ```

2. Use the template from `docs/projects/README.md`:
   - Overview
   - Names Under Consideration
   - Architecture
   - Features (Core + Future)
   - Notes
   - Todo

3. Update status in `docs/projects.md` from 💡 → 🔨

### Change Project Status

Status indicators:
- `💡` idea - Unstarted concept
- `🔨` active - Currently working on it
- `⏸️` paused - Started but on hold
- `✅` shipped - Deployed and live
- `📦` archived - No longer maintained

Just edit the emoji in the Status column of `docs/projects.md`.

## File Structure

```
docs/
├── projects.md              # Single source of truth - master registry
├── project-names.md         # Available/assigned project names
├── project-backlog.md.archive  # Old backlog (reference only)
└── projects/
    ├── README.md            # Template for detailed project files
    └── <project-name>.md    # Optional detailed project documentation
```

## Workflow Examples

### Brainstorming a New Idea

```bash
# 1. Add to ideas section in projects.md
nvim ~/Development/codex/docs/projects.md

# 2. Pick a name
projects name my-idea

# 3. Update project-names.md if you assign a name
nvim ~/Development/codex/docs/project-names.md
```

### Starting Development

```bash
# 1. Create detailed project file
nvim ~/Development/codex/docs/projects/my-project.md

# 2. Change status from 💡 to 🔨 in projects.md

# 3. Create repo and start coding
mkdir ~/Development/my-project
cd ~/Development/my-project
git init
```

### Reviewing Active Work

```bash
# See all active projects
projects active

# Check if any repos are missing from registry
projects sync

# View statistics
projects stats
```

## Tips

- **Keep registry clean:** Run `projects sync` periodically to catch orphaned repos
- **Archive liberally:** Don't be afraid to move stale projects to archived
- **Use tags:** Add relevant tags (cli, web, mobile, ai, etc.) for easy filtering
- **Detail selectively:** Only create detailed project files for active work
- **Name thoughtfully:** Check available names with `projects name <project>`

## Migration Notes

- Old `project-backlog.md` → archived as `project-backlog.md.archive`
- All projects from backlog + GitHub repos + ~/Development merged into `projects.md`
- Project statuses inferred from git activity:
  - Last commit < 2 weeks = active (🔨)
  - Last commit 2 weeks - 6 months = paused (⏸️)
  - Last commit > 6 months = archived (📦)
  - No commits = idea (💡)

---

**Last Updated:** 2025-11-01
