# Interaction Design

## The Eight Interactive States

Every interactive element needs these states designed:

| State | When | Visual Treatment |
|-------|------|------------------|
| **Default** | At rest | Base styling |
| **Hover** | Pointer over (not touch) | Subtle lift, color shift |
| **Focus** | Keyboard/programmatic focus | Visible ring |
| **Active** | Being pressed | Pressed in, darker |
| **Disabled** | Not interactive | Reduced opacity, no pointer |
| **Loading** | Processing | Spinner, skeleton |
| **Error** | Invalid state | Red border, icon, message |
| **Success** | Completed | Green check, confirmation |

**The common miss**: Designing hover without focus, or vice versa. Keyboard users never see hover states.

## Focus Rings: Do Them Right

**Never `outline: none` without replacement.** Use `:focus-visible` to show focus only for keyboard users:

```css
button:focus { outline: none; }
button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

Focus ring design: High contrast (3:1 minimum), 2-3px thick, offset from element, consistent across all interactive elements.

## Form Design

**Placeholders aren't labels**--they disappear on input. Always use visible `<label>` elements. **Validate on blur**, not on every keystroke (exception: password strength). Place errors **below** fields with `aria-describedby` connecting them.

## Loading States

**Optimistic updates**: Show success immediately, rollback on failure. Use for low-stakes actions (likes, follows), not payments or destructive actions. **Skeleton screens > spinners**--they preview content shape and feel faster.

## Modals: The Inert Approach

Use the `inert` attribute or native `<dialog>` element:

```javascript
const dialog = document.querySelector('dialog');
dialog.showModal();
```

## The Popover API

For tooltips, dropdowns, and non-modal overlays:

```html
<button popovertarget="menu">Open menu</button>
<div id="menu" popover>
  <button>Option 1</button>
</div>
```

Benefits: Light-dismiss, proper stacking, no z-index wars, accessible by default.

## Dropdown & Overlay Positioning

Dropdowns rendered with `position: absolute` inside `overflow: hidden` will be clipped. Use CSS Anchor Positioning (Chrome 125+), Popover API top layer, portals in frameworks, or `position: fixed` with manual coordinates as fallback.

### Anti-Patterns

- `position: absolute` inside `overflow: hidden`--use `position: fixed` or top layer
- Arbitrary `z-index: 9999`--use a semantic z-index scale
- Inline dropdown markup without an escape hatch from parent stacking context

## Destructive Actions: Undo > Confirm

Undo is better than confirmation dialogs--users click through confirmations mindlessly. Remove from UI immediately, show undo toast, actually delete after toast expires.

## Keyboard Navigation Patterns

### Roving Tabindex

For component groups (tabs, menu items, radio groups), one item is tabbable; arrow keys move within. Tab moves to the next component entirely.

### Skip Links

Provide skip links for keyboard users to jump past navigation. Hide off-screen, show on focus.

## Gesture Discoverability

Swipe-to-delete and similar gestures are invisible. Always provide a visible fallback. Hint at gesture existence through partial reveals or onboarding.

---

**Avoid**: Removing focus indicators without alternatives. Using placeholder text as labels. Touch targets <44x44px. Generic error messages. Custom controls without ARIA/keyboard support.
