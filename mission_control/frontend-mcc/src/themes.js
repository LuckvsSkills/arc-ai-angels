const mk = (name, mode, bg, bg2, bg3, bdr, bdrH, text, textM, acc, accDim) => ({
  name, mode,
  colors: {
    bg, bgSecondary: bg2, bgTertiary: bg3,
    border: bdr, borderHover: bdrH,
    text, textSecondary: textM, textMuted: textM,
    accent: acc, accentSoft: accDim, accentText: acc,
    accentDim: accDim,
    borderAccent: `${acc}40`,
    success: '#2ecc71', warning: '#f39c12', danger: '#e74c3c', info: '#3498db',
    primary: acc, primaryLight: acc, secondary: acc, secondaryLight: acc,
  }
})

export const THEMES = {

  cosmic_night: mk(
    "Cosmic Night", "dark",
    "#080d1f", "#0d1530", "#131e42",
    "#1a2848", "#243660",
    "#dce8f8", "#7aa0cc",
    "#00d9ff", "rgba(0,217,255,0.09)"
  ),

  neon_city: mk(
    "Neon City", "dark",
    "#06080f", "#0c1020", "#111830",
    "#18233a", "#243350",
    "#e8eeff", "#7890c8",
    "#f020c0", "rgba(240,32,192,0.09)"
  ),

  midnight_blue: mk(
    "Midnight Blue", "dark",
    "#080b10", "#0e131c", "#141d28",
    "#1e2a38", "#2a3a50",
    "#d8eeff", "#7098c8",
    "#4d9fff", "rgba(77,159,255,0.09)"
  ),

  aurora: mk(
    "Aurora", "dark",
    "#080b10", "#0e131c", "#141d28",
    "#1e2a38", "#2a3a50",
    "#d8f0ee", "#70b8a8",
    "#00ffcc", "rgba(0,255,204,0.09)"
  ),

  ember: mk(
    "Ember", "dark",
    "#080b10", "#0e131c", "#141d28",
    "#1e2a38", "#2a3a50",
    "#f0e8d8", "#b09878",
    "#ff8c00", "rgba(255,140,0,0.09)"
  ),

  deep_purple: mk(
    "Deep Purple", "dark",
    "#080612", "#0f0c1e", "#17122c",
    "#22183e", "#302258",
    "#e4dcff", "#9070d0",
    "#a855f7", "rgba(168,85,247,0.09)"
  ),

  slate: mk(
    "Slate", "dark",
    "#080b10", "#0e131c", "#141d28",
    "#1e2a38", "#2a3a50",
    "#d8e4f0", "#7098b8",
    "#ff6b35", "rgba(255,107,53,0.09)"
  ),

  arctic: mk(
    "Arctic", "light",
    "#f0f6ff", "#e4eeff", "#d8e6ff",
    "#b8ccee", "#8aaad8",
    "#08182e", "#3a5878",
    "#0050cc", "rgba(0,80,204,0.08)"
  ),

  warm_paper: mk(
    "Warm Paper", "light",
    "#faf7f2", "#f2ede4", "#e8e0d4",
    "#d4c8b8", "#b8aa98",
    "#1c1410", "#6a5040",
    "#8b2500", "rgba(139,37,0,0.08)"
  ),

  // ── Bestaande extra themes ────────────────────────────────
  imperial: mk(
    "Imperial Gold", "dark",
    "#0c0f18", "#141824", "#1c2436",
    "#243050", "#304070",
    "#f0f4ff", "#6a7a98",
    "#e8b84b", "rgba(232,184,75,0.09)"
  ),
}

export const getCompatTheme = (name) => {
  const t = THEMES[name] || THEMES.cosmic_night
  return { ...t, colors: { ...t.colors } }
}
export const getTheme = (name) => getCompatTheme(name)
