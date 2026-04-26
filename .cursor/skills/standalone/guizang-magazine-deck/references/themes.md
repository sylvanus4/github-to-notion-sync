# Theme Presets (Themes)

5 carefully crafted color palettes that maintain the "electronic magazine × electronic ink" aesthetic. **Custom colors are not allowed — bad color pairing instantly ruins the visual.** Only pick from the presets below.

---

## How to Apply

1. Ask the user which theme to use (or recommend one based on content)
2. Open the `<style>` block in `assets/template.html`
3. Find the `:root{` block at the top
4. **Replace the entire set** of lines marked with theme color comments: `--ink` / `--ink-rgb` / `--paper` / `--paper-rgb` / `--paper-tint` / `--ink-tint`
5. All other CSS uses `var(--...)` — no other changes needed

---

## Ink Classic (Monocle Default)

**Best for**: Universal presentations, business launches, tech products, any scenario — the safe default choice.
**Tonality**: Pure ink black + warm cream white. Maximum magazine feel. Monocle / Apricot / A Book Apart aesthetic.

```css
--ink:#0a0a0b;
--ink-rgb:10,10,11;
--paper:#f1efea;
--paper-rgb:241,239,234;
--paper-tint:#e8e5de;
--ink-tint:#18181a;
```

---

## Indigo Porcelain

**Best for**: Tech/research/data presentations, engineer culture, deep content, technical launches.
**Tonality**: Deep indigo + porcelain white. Calm, rational, substantial — like an academic journal or blue-and-white porcelain.

```css
--ink:#0a1f3d;
--ink-rgb:10,31,61;
--paper:#f1f3f5;
--paper-rgb:241,243,245;
--paper-tint:#e4e8ec;
--ink-tint:#152a4a;
```

---

## Forest Ink

**Best for**: Nature/sustainability/culture/non-fiction content, outdoor brands, environmental themes.
**Tonality**: Deep forest green + ivory. Steady, breathable — like a vintage issue of National Geographic.

```css
--ink:#1a2e1f;
--ink-rgb:26,46,31;
--paper:#f5f1e8;
--paper-rgb:245,241,232;
--paper-tint:#ece7da;
--ink-tint:#253d2c;
```

---

## Kraft Paper

**Best for**: Nostalgia/humanities/reading/history/literary presentations, indie magazines, artisan brands.
**Tonality**: Deep brown + warm cream — like a kraft envelope or vintage notebook. Warm, with a sense of age.

```css
--ink:#2a1e13;
--ink-rgb:42,30,19;
--paper:#eedfc7;
--paper-rgb:238,223,199;
--paper-tint:#e0d0b6;
--ink-tint:#3a2a1d;
```

---

## Dune

**Best for**: Art/design/creative/fashion presentations, gallery handbooks, aesthetics-first private sessions.
**Tonality**: Charcoal + sand. Restrained, premium, neutral — like a desert dusk or architectural monograph.

```css
--ink:#1f1a14;
--ink-rgb:31,26,20;
--paper:#f0e6d2;
--paper-rgb:240,230,210;
--paper-tint:#e3d7bf;
--ink-tint:#2d2620;
```

---

## Selection Guide

| If the content is... | Recommended Theme |
|---------------------|-------------------|
| Unsure / first time using | Ink Classic |
| AI / tech / product launch | Indigo Porcelain |
| Content / industry / culture | Forest Ink |
| Book review / lifestyle / humanities | Kraft Paper |
| Design / art / brand | Dune |

---

## Switching Rules

- **One deck = one theme** — do not switch colors mid-deck
- WebGL shader default colors (titanium dispersion / silver flow) work with all 5 themes (tested)
- `currentColor`-driven borders and icons auto-adapt to each section's text color — no extra adjustment needed
- After choosing a theme, `<title>` text and `chrome` copy can reinforce the theme's semantics (e.g., Kraft Paper pairs with "Vol.03 · Autumn")

## Things NOT to Do

- **No mixing** (e.g., taking ink from Ink Classic and paper from Dune) — creates immediate dissonance
- **No arbitrary hex values** from users — politely decline and show the 5 presets
- **Do not modify colors elsewhere** in template.html — all scattered rgba() calls use var(), changing `:root` is sufficient

After selecting a theme, tell the user: "Using Ink Classic / Indigo Porcelain / ..." and note it in the deck project record for future iteration consistency.
