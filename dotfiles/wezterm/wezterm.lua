-- Minimal WezTerm Configuration
-- Optimized for macOS stability and performance

local wezterm = require('wezterm')
local config = wezterm.config_builder()
local act = wezterm.action

-- ====================
-- APPEARANCE
-- ====================

config.color_scheme = 'rose-pine'
config.font = wezterm.font('JetBrains Mono', { weight = 'Medium' })
config.font_size = 14.0
config.window_background_opacity = 0.98
config.macos_window_background_blur = 20

-- ====================
-- PERFORMANCE
-- ====================

-- Conservative settings to avoid input lag
config.front_end = 'WebGpu'
config.max_fps = 30
config.animation_fps = 30
config.scrollback_lines = 10000

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
-- TAB BAR
-- ====================

config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = false
config.window_decorations = 'RESIZE'
config.window_padding = { left = 8, right = 8, top = 8, bottom = 8 }

-- Simple static status (no subprocess calls)
wezterm.on('update-right-status', function(window, pane)
  local workspace = window:active_workspace()
  local time = wezterm.strftime('%H:%M')

  local status = workspace ~= 'default'
    and string.format(' %s | %s ', workspace, time)
    or string.format(' %s ', time)

  window:set_right_status(status)
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

  -- Pane splits
  { key = '"', mods = 'LEADER|SHIFT', action = act.SplitVertical({ domain = 'CurrentPaneDomain' }) },
  { key = '%', mods = 'LEADER|SHIFT', action = act.SplitHorizontal({ domain = 'CurrentPaneDomain' }) },

  -- Pane navigation
  { key = 'h', mods = 'LEADER', action = act.ActivatePaneDirection('Left') },
  { key = 'j', mods = 'LEADER', action = act.ActivatePaneDirection('Down') },
  { key = 'k', mods = 'LEADER', action = act.ActivatePaneDirection('Up') },
  { key = 'l', mods = 'LEADER', action = act.ActivatePaneDirection('Right') },

  -- Pane zoom
  { key = 'z', mods = 'LEADER', action = act.TogglePaneZoomState },

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
