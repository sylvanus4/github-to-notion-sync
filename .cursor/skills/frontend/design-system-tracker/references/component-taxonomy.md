# Component Taxonomy

Standard categories for organizing design system components during change tracking.

## Component Categories

| Category | Examples | Change Sensitivity |
|----------|---------|-------------------|
| **Foundation** | Colors, Typography, Spacing, Shadows, Icons | High — affects everything |
| **Layout** | Grid, Container, Stack, Divider | High — affects page structure |
| **Navigation** | Header, Sidebar, Tabs, Breadcrumb, Pagination | Medium — affects UX flow |
| **Input** | Button, TextField, Select, Checkbox, Radio, Toggle | High — affects interaction |
| **Feedback** | Alert, Toast, Modal, Dialog, Tooltip, Progress | Medium — affects UX feedback |
| **Data Display** | Table, Card, List, Badge, Tag, Avatar | Medium — affects content |
| **Utility** | Skeleton, Empty State, Loading Spinner | Low — visual-only |

## Token Categories

| Category | Examples | Change Sensitivity |
|----------|---------|-------------------|
| **Color** | primary, secondary, error, warning, surface | High |
| **Typography** | font-family, font-size, line-height, font-weight | High |
| **Spacing** | spacing-xs through spacing-xxl, padding, margin | Medium |
| **Shadow** | elevation-1 through elevation-5 | Low |
| **Border** | radius, width, color | Low |
| **Breakpoint** | mobile, tablet, desktop | High |

## Change Tracking Hierarchy

```
Design System
├── Foundation Tokens (track all changes)
├── Components
│   ├── Props (track additions, removals, type changes)
│   ├── Variants (track additions, removals)
│   ├── States (track additions, removals)
│   └── Slots/Children (track structure changes)
└── Patterns/Compositions (track when components change)
```
