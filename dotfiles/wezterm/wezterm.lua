-- Beautiful WezTerm Configuration
-- Optimized for macOS stability and aesthetics

local wezterm = require('wezterm')
local config = wezterm.config_builder()
local act = wezterm.action

-- ====================
-- APPEARANCE
-- ====================

-- Rose Pine Moon for softer, more aesthetic colors
config.color_scheme = 'rose-pine-moon'

-- Typography with better spacing and fallbacks
config.font = wezterm.font_with_fallback({
  { family = 'JetBrains Mono', weight = 'Medium' },
  'Symbols Nerd Font Mono',
  'Apple Color Emoji',
})
config.font_size = 14.0
config.line_height = 1.3
config.harfbuzz_features = { 'calt=1', 'clig=1', 'liga=1' }

-- Window aesthetics
config.window_background_opacity = 0.95
config.macos_window_background_blur = 30

-- Dim inactive panes for visual depth
config.inactive_pane_hsb = {
  saturation = 0.24,
  brightness = 0.5,
}

-- ====================
-- PERFORMANCE
-- ====================

-- Conservative settings to avoid input lag
config.front_end = 'WebGpu'
config.max_fps = 30
config.animation_fps = 30
config.scrollback_lines = 10000

-- Smooth cursor
config.default_cursor_style = 'BlinkingBlock'
config.cursor_blink_rate = 800
config.cursor_blink_ease_in = 'EaseIn'
config.cursor_blink_ease_out = 'EaseOut'

-- ====================
-- BEHAVIOR
-- ====================

config.default_prog = { '/bin/zsh', '-l' }
config.audible_bell = 'Disabled'
config.window_close_confirmation = 'NeverPrompt'
config.automatically_reload_config = true

-- CRITICAL: Disable kitty keyboard protocol (causes input doubling on macOS)
config.enable_kitty_keyboard = false

-- ====================
-- TAB BAR & WINDOW
-- ====================

config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = false
config.tab_max_width = 32
config.window_decorations = 'RESIZE'
config.window_padding = { left = 12, right = 12, top = 12, bottom = 12 }

-- Rose Pine Moon colors for tab bar
local rose_pine = {
  bg = '#232136',
  fg = '#e0def4',
  subtle = '#6e6a86',
  muted = '#908caa',
  love = '#eb6f92',
  gold = '#f6c177',
  foam = '#9ccfd8',
  iris = '#c4a7e7',
}

-- Powerline separators (nerd fonts)
local SOLID_LEFT_ARROW = wezterm.nerdfonts.pl_right_hard_divider
local SOLID_RIGHT_ARROW = wezterm.nerdfonts.pl_left_hard_divider

-- Process icons
local process_icons = {
  ['bash'] = wezterm.nerdfonts.cod_terminal_bash,
  ['zsh'] = wezterm.nerdfonts.dev_terminal,
  ['nvim'] = wezterm.nerdfonts.custom_vim,
  ['vim'] = wezterm.nerdfonts.dev_vim,
  ['node'] = wezterm.nerdfonts.mdi_hexagon,
  ['git'] = wezterm.nerdfonts.fa_git,
  ['cargo'] = wezterm.nerdfonts.dev_rust,
  ['go'] = wezterm.nerdfonts.seti_go,
  ['python'] = wezterm.nerdfonts.dev_python,
  ['ruby'] = wezterm.nerdfonts.cod_ruby,
  ['docker'] = wezterm.nerdfonts.linux_docker,
}

-- Format tab title with icon and directory
wezterm.on('format-tab-title', function(tab, tabs, panes, config, hover, max_width)
  local pane = tab.active_pane
  local title = tab.tab_title

  -- Get process name
  local process = pane.foreground_process_name
  local process_name = process and process:match('([^/]+)$') or 'zsh'
  local icon = process_icons[process_name] or wezterm.nerdfonts.cod_terminal

  -- Get directory name
  local cwd = pane.current_working_dir
  local dir = 'home'
  if cwd then
    local cwd_uri = type(cwd) == 'userdata' and cwd.file_path or cwd
    dir = cwd_uri:match('([^/]+)/?$') or 'home'
  end

  -- Use custom title if set, otherwise format as "icon dir/"
  if not title or #title == 0 then
    title = string.format(' %s %s/ ', icon, dir)
  end

  -- Colors
  local bg = rose_pine.bg
  local fg = rose_pine.subtle

  if tab.is_active then
    bg = rose_pine.muted
    fg = rose_pine.bg
  elseif hover then
    bg = '#2a273f'
    fg = rose_pine.fg
  end

  return {
    { Background = { Color = bg } },
    { Foreground = { Color = fg } },
    { Text = title },
  }
end)

-- Gradient powerline status bar
wezterm.on('update-right-status', function(window, pane)
  local workspace = window:active_workspace()
  local time = wezterm.strftime('%H:%M')
  local hostname = wezterm.hostname():match('([^.]+)')

  -- Build segments
  local segments = {}

  if workspace ~= 'default' then
    table.insert(segments, { text = ' ' .. workspace, color = rose_pine.iris })
  end

  table.insert(segments, { text = ' ' .. wezterm.nerdfonts.md_clock .. ' ' .. time, color = rose_pine.foam })
  table.insert(segments, { text = ' ' .. wezterm.nerdfonts.md_laptop .. ' ' .. hostname, color = rose_pine.gold })

  -- Format with powerline arrows
  local elements = {}
  for i, seg in ipairs(segments) do
    table.insert(elements, { Foreground = { Color = seg.color } })
    table.insert(elements, { Text = SOLID_LEFT_ARROW })
    table.insert(elements, { Background = { Color = seg.color } })
    table.insert(elements, { Foreground = { Color = rose_pine.bg } })
    table.insert(elements, { Text = seg.text .. ' ' })
  end

  window:set_right_status(wezterm.format(elements))
end)

-- ====================
-- TMUX-STYLE KEYBINDINGS
-- ====================

config.leader = { key = 'b', mods = 'CTRL', timeout_milliseconds = 1000 }

config.keys = {
  -- Tab management
  { key = 'c', mods = 'LEADER', action = act.SpawnTab('CurrentPaneDomain') },
  { key = 'n', mods = 'LEADER', action = act.ActivateTabRelative(1) },
  { key = 'p', mods = 'LEADER', action = act.ActivateTabRelative(-1) },
  { key = 'x', mods = 'LEADER', action = act.CloseCurrentPane({ confirm = true }) },
  { key = 'w', mods = 'LEADER', action = act.ShowTabNavigator },

  -- Pane splits (visual mnemonics: | = vertical divider, - = horizontal divider)
  { key = '|', mods = 'LEADER|SHIFT', action = act.SplitHorizontal({ domain = 'CurrentPaneDomain' }) },
  { key = '-', mods = 'LEADER', action = act.SplitVertical({ domain = 'CurrentPaneDomain' }) },

  -- Pane navigation
  { key = 'h', mods = 'LEADER', action = act.ActivatePaneDirection('Left') },
  { key = 'j', mods = 'LEADER', action = act.ActivatePaneDirection('Down') },
  { key = 'k', mods = 'LEADER', action = act.ActivatePaneDirection('Up') },
  { key = 'l', mods = 'LEADER', action = act.ActivatePaneDirection('Right') },

  -- Pane zoom
  { key = 'z', mods = 'LEADER', action = act.TogglePaneZoomState },

  -- Fullscreen
  { key = 'Enter', mods = 'LEADER', action = act.ToggleFullScreen },

  -- Copy mode
  { key = '[', mods = 'LEADER', action = act.ActivateCopyMode },

  -- macOS standard bindings
  { key = '=', mods = 'CMD', action = act.IncreaseFontSize },
  { key = '-', mods = 'CMD', action = act.DecreaseFontSize },
  { key = '0', mods = 'CMD', action = act.ResetFontSize },
  { key = 'K', mods = 'CMD', action = act.ClearScrollback('ScrollbackAndViewport') },
  { key = 'c', mods = 'CMD', action = act.CopyTo('Clipboard') },
  { key = 'v', mods = 'CMD', action = act.PasteFrom('Clipboard') },
  { key = 'n', mods = 'CMD', action = act.SpawnWindow },
  { key = 'w', mods = 'CMD', action = act.CloseCurrentPane({ confirm = true }) },
  { key = 'r', mods = 'CMD|SHIFT', action = act.ReloadConfiguration },
}

-- Tab switching with leader + number
for i = 1, 9 do
  table.insert(config.keys, {
    key = tostring(i),
    mods = 'LEADER',
    action = act.ActivateTab(i - 1),
  })
end

return config
