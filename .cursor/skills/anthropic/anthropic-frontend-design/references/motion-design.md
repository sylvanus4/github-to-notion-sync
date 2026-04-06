# Motion Design

## Duration: The 100/300/500 Rule

| Duration | Use Case | Examples |
|----------|----------|----------|
| **100-150ms** | Instant feedback | Button press, toggle, color change |
| **200-300ms** | State changes | Menu open, tooltip, hover states |
| **300-500ms** | Layout changes | Accordion, modal, drawer |
| **500-800ms** | Entrance animations | Page load, hero reveals |

**Exit animations are faster than entrances**--use ~75% of enter duration.

## Easing: Pick the Right Curve

**Don't use `ease`.** It's a compromise that's rarely optimal.

| Curve | Use For | CSS |
|-------|---------|-----|
| **ease-out** | Elements entering | `cubic-bezier(0.16, 1, 0.3, 1)` |
| **ease-in** | Elements leaving | `cubic-bezier(0.7, 0, 0.84, 0)` |
| **ease-in-out** | State toggles | `cubic-bezier(0.65, 0, 0.35, 1)` |

**For micro-interactions, use exponential curves**:

```css
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
--ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
```

**Avoid bounce and elastic curves.** They feel dated and tacky. Real objects decelerate smoothly.

## The Only Two Properties You Should Animate

**transform** and **opacity** only--everything else causes layout recalculation. For height animations (accordions), use `grid-template-rows: 0fr -> 1fr` instead of animating `height` directly.

## Staggered Animations

Use CSS custom properties for cleaner stagger: `animation-delay: calc(var(--i, 0) * 50ms)` with `style="--i: 0"` on each item. **Cap total stagger time**--10 items at 50ms = 500ms total.

## Reduced Motion

This is not optional. Vestibular disorders affect ~35% of adults over 40.

```css
@media (prefers-reduced-motion: reduce) {
  .card {
    animation: fade-in 200ms ease-out;
  }
}
```

**Preserve**: Functional animations like progress bars, loading spinners (slowed down), and focus indicators--just without spatial movement.

## Perceived Performance

**The 80ms threshold**: Our brains buffer sensory input for ~80ms. Anything under 80ms feels instant. This is your target for micro-interactions.

Strategies:
- **Preemptive start**: Begin transitions immediately while loading
- **Early completion**: Show content progressively
- **Optimistic UI**: Update the interface immediately, handle failures gracefully

**Caution**: Too-fast responses can decrease perceived value. Sometimes a brief delay signals "real work" is happening.

## Performance

Don't use `will-change` preemptively--only when animation is imminent. For scroll-triggered animations, use Intersection Observer instead of scroll events; unobserve after animating once.

---

**Avoid**: Animating everything (animation fatigue is real). Using >500ms for UI feedback. Ignoring `prefers-reduced-motion`. Using animation to hide slow loading.
