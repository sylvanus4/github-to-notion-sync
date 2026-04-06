# Responsive Design

## Mobile-First: Write It Right

Start with base styles for mobile, use `min-width` queries to layer complexity. Desktop-first (`max-width`) means mobile loads unnecessary styles first.

## Breakpoints: Content-Driven

Don't chase device sizes--let content tell you where to break. Start narrow, stretch until design breaks, add breakpoint there. Three breakpoints usually suffice (640, 768, 1024px). Use `clamp()` for fluid values without breakpoints.

## Detect Input Method, Not Just Screen Size

**Screen size doesn't tell you input method.** Use pointer and hover queries:

```css
@media (pointer: fine) {
  .button { padding: 8px 16px; }
}

@media (pointer: coarse) {
  .button { padding: 12px 20px; }
}

@media (hover: hover) {
  .card:hover { transform: translateY(-2px); }
}

@media (hover: none) {
  .card { /* No hover state - use active instead */ }
}
```

**Critical**: Don't rely on hover for functionality. Touch users can't hover.

## Safe Areas: Handle the Notch

Modern phones have notches, rounded corners, and home indicators:

```css
body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

Enable viewport-fit: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`

## Responsive Images

### srcset with Width Descriptors

```html
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="Hero image"
>
```

### Picture Element for Art Direction

```html
<picture>
  <source media="(min-width: 768px)" srcset="wide.jpg">
  <source media="(max-width: 767px)" srcset="tall.jpg">
  <img src="fallback.jpg" alt="...">
</picture>
```

## Layout Adaptation Patterns

**Navigation**: Three stages--hamburger + drawer on mobile, horizontal compact on tablet, full with labels on desktop. **Tables**: Transform to cards on mobile using `display: block` and `data-label` attributes. **Progressive disclosure**: Use `<details>/<summary>` for content that can collapse on mobile.

## Testing: Don't Trust DevTools Alone

DevTools misses: actual touch interactions, real CPU/memory constraints, network latency patterns, font rendering differences, browser chrome/keyboard appearances.

**Test on at least**: One real iPhone, one real Android, a tablet if relevant.

---

**Avoid**: Desktop-first design. Device detection instead of feature detection. Separate mobile/desktop codebases. Ignoring tablet and landscape. Assuming all mobile devices are powerful.
