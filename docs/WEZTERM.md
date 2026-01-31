# WezTerm Configuration Guide

Modern terminal emulator with native multiplexing, replacing tmux with WezTerm's built-in features.

## Configuration Files

```
dotfiles/wezterm/
├── wezterm.lua       # Main configuration
├── rose-pine.lua     # Rose Pine theme (main/moon/dawn)
├── keybindings.lua   # Tmux-style keybindings
└── status.lua        # Smart status bar with git
```

**Location:** `~/.config/wezterm/` → `dotfiles/wezterm/`

## Features

- **Rose Pine Theme** - All natural pine, faux fur and soho vibes
- **Native Multiplexing** - Tabs, panes, workspaces (no tmux needed)
- **Smart Status Bar** - Git branch, battery, time, workspace
- **Vim Copy Mode** - Full vim keybindings for scrollback
- **GPU Rendering** - WebGPU acceleration via Metal
- **Ligature Support** - JetBrains Mono with programming ligatures

## Leader Key

**Leader:** `Ctrl+b` (same as tmux)

Press `Ctrl+b` then release, then press the command key.

## Keybindings Reference

### Tab/Window Management

| Keybinding | Action |
|------------|--------|
| `Ctrl+b c` | Create new tab |
| `Ctrl+b &` | Close tab (with confirmation) |
| `Ctrl+b n` | Next tab |
| `Ctrl+b p` | Previous tab |
| `Ctrl+b 1-9` | Jump to tab number |
| `Ctrl+b ,` | Rename current tab |
| `Ctrl+b w` | List/choose tabs (fuzzy finder) |

### Pane Management

| Keybinding | Action |
|------------|--------|
| `Ctrl+b "` | Split pane down (horizontal) |
| `Ctrl+b %` | Split pane right (vertical) |
| `Ctrl+b x` | Close pane (with confirmation) |
| `Ctrl+b h` | Navigate to left pane |
| `Ctrl+b j` | Navigate to pane below |
| `Ctrl+b k` | Navigate to pane above |
| `Ctrl+b l` | Navigate to right pane |
| `Ctrl+b H` | Resize pane left |
| `Ctrl+b J` | Resize pane down |
| `Ctrl+b K` | Resize pane up |
| `Ctrl+b L` | Resize pane right |
| `Ctrl+b z` | Toggle pane zoom (fullscreen) |
| `Ctrl+b o` | Rotate panes clockwise |

### Workspace Management

Workspaces are like tmux sessions - organize windows by project.

| Keybinding | Action |
|------------|--------|
| `Ctrl+b s` | List/switch workspaces (fuzzy) |
| `Ctrl+b $` | Rename current workspace |
| `Ctrl+b d` | Detach/hide window (minimize) |

### Copy Mode & Search

| Keybinding | Action |
|------------|--------|
| `Ctrl+b [` | Enter copy mode (vim bindings) |
| `Ctrl+b f` | Search scrollback |
| `Ctrl+b ]` | Paste from clipboard |

#### Vim Bindings in Copy Mode

**Movement:**
- `h/j/k/l` - Left/Down/Up/Right
- `w/b/e` - Forward word / Back word / End word
- `0/$` - Start/End of line
- `^` - First non-blank character
- `H/M/L` - Top/Middle/Bottom of viewport
- `g/G` - Top/Bottom of scrollback
- `Ctrl+f/b` - Page down/up
- `Ctrl+d/u` - Half page down/up

**Selection:**
- `v` - Character selection
- `V` - Line selection
- `Ctrl+v` - Block selection

**Copy & Exit:**
- `y` - Yank (copy) selection and exit
- `/` - Search
- `n/N` - Next/Previous match
- `Escape` or `q` - Exit copy mode

### Launcher & Palette

| Keybinding | Action |
|------------|--------|
| `Ctrl+b P` | Show launcher (tabs/workspaces) |
| `Ctrl+b :` | Command palette |

### Direct Shortcuts (no leader)

| Keybinding | Action |
|------------|--------|
| `Cmd+=` | Increase font size |
| `Cmd+-` | Decrease font size |
| `Cmd+0` | Reset font size |
| `Cmd+K` | Clear scrollback |
| `Cmd+C` | Copy to clipboard |
| `Cmd+V` | Paste from clipboard |
| `Cmd+N` | New window |
| `Cmd+W` | Close window/pane |
| `Cmd+Enter` | Toggle fullscreen |
| `Cmd+Shift+R` | Reload configuration |
| `Cmd+Shift+L` | Debug overlay |

### Mouse Bindings

- **Left Click** - Select text
- **Right Click** - Paste from clipboard
- **Cmd+Click** - Open hyperlink
- **Middle Click** - Paste primary selection

## Status Bar

**Right Side:** Workspace • Battery • Time • Hostname

**Left Side:** Active key table indicator (e.g., `[RESIZE_PANE]`)

**Tab Title Format:** `<number>: <directory> <git-branch> [🔍]`
- Shows git branch if in repo
- Shows 🔍 if pane is zoomed

## Themes

Rose Pine has three variants:

```lua
-- In wezterm.lua, change:
local theme = rose_pine.main  -- Default dark theme
local theme = rose_pine.moon  -- Alternative dark theme
local theme = rose_pine.dawn  -- Light theme
```

**Colors:**
- **Main** - Deep purple background (#191724)
- **Moon** - Slightly lighter purple (#232136)
- **Dawn** - Light beige background (#faf4ed)

## Workspaces

Create project-based workspaces:

1. `Ctrl+b s` - Open workspace switcher
2. Type new workspace name
3. Each workspace has independent tabs/panes
4. Switch between workspaces with fuzzy finder

**Example workflow:**
```
Ctrl+b s → "codex" → Create workspace for codex project
Ctrl+b s → "docs" → Create workspace for documentation
Ctrl+b s → Switch back to previous workspace
```

## Advanced Features

### GPU Acceleration
- **Backend:** WebGPU (Metal on macOS)
- **FPS:** 60 frames per second
- **Performance:** High-performance GPU preference

### Font Configuration
- **Font:** JetBrains Mono Medium
- **Size:** 14pt
- **Ligatures:** Enabled (programming ligatures)
- **Line Height:** 1.2

### Window Behavior
- **Opacity:** 98% with 20pt blur
- **Decorations:** Resize only (no title bar)
- **Padding:** 8px all sides
- **Startup:** Maximized window

## Tips & Tricks

### Quick Pane Layouts

**Split right then split down:**
```
Ctrl+b %     # Split right
Ctrl+b j     # Move to right pane
Ctrl+b "     # Split down
```

**Three-column layout:**
```
Ctrl+b %     # Split right (now 2 columns)
Ctrl+b %     # Split right again (now 3 columns)
```

### Rename Tab to Match Project
```
Ctrl+b ,     # Opens rename prompt
Type: "my-project"
```

### Search Scrollback
```
Ctrl+b f     # Opens search
Type: "error"
Enter        # Searches through scrollback
```

### Quick Workspace Switch
```
Ctrl+b s     # Opens workspace fuzzy finder
Type: first few letters
Enter        # Switches to workspace
```

## Troubleshooting

### Config Not Loading
```bash
# Check config validity
wezterm show-config

# Reload config
Cmd+Shift+R
```

### See All Keybindings
```bash
# Show all configured keys
wezterm show-keys --lua
```

### Debug Issues
```bash
# Open debug overlay
Cmd+Shift+L

# Check logs
tail -f ~/.local/share/wezterm/wezterm.log
```

### Reset to Defaults
```bash
# Temporarily disable config
mv ~/.config/wezterm ~/.config/wezterm.bak
```

## Comparison to Tmux

| Feature | Tmux | WezTerm |
|---------|------|---------|
| Sessions | Yes | Workspaces |
| Tabs/Windows | Yes | Yes (native) |
| Panes | Yes | Yes (native) |
| Leader Key | Ctrl+b | Ctrl+b (compatible) |
| Copy Mode | Vi/Emacs | Vi (native) |
| Detach | Yes | Hide window |
| Remote | Yes | SSH domains |
| Performance | Terminal-based | GPU-accelerated |
| Ligatures | No | Yes |
| Images | Limited | Full support |
| Escape Time | ~500ms lag | No lag |

## Migration from Tmux

WezTerm keybindings are designed to match tmux:

- Same leader key (Ctrl+b)
- Same split bindings (% and ")
- Same navigation (h/j/k/l)
- Same copy mode ([ and ])
- Workspaces replace sessions

**For remote servers:** Keep using tmux over SSH. Use WezTerm SSH domains for seamless integration.

## Resources

- **Official Docs:** https://wezfurlong.org/wezterm/
- **Color Schemes:** https://wezfurlong.org/wezterm/colorschemes/
- **Rose Pine:** https://rosepinetheme.com/
- **Config Location:** `~/.config/wezterm/wezterm.lua`
- **This Config:** `~/Development/codex/dotfiles/wezterm/`

## Quick Start

1. Install WezTerm: `brew install --cask wezterm`
2. Config already symlinked: `~/.config/wezterm → dotfiles/wezterm`
3. Launch WezTerm
4. Press `Ctrl+b ?` to see this guide
5. Start with `Ctrl+b c` (new tab) and `Ctrl+b %` (split right)

---

*Last updated: 2025-01-21*
