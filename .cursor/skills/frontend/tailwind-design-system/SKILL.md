---
name: tailwind-design-system
description: >-
  Build scalable design systems with Tailwind CSS v4, including CSS-first
  configuration, OKLCH design tokens, CVA-based component variants, compound
  components, form patterns, responsive grids, dark mode, and native CSS
  animations. Use when the user asks to "create a component library",
  "implement design tokens", "build a design system", "standardize UI patterns",
  "set up Tailwind v4 theming", "create responsive components",
  "tailwind-design-system", "Tailwind v4 setup", "CVA component",
  "design system with Tailwind", or wants to build a systematic UI foundation.
  Do NOT use for building specific UIs from scratch (use anthropic-frontend-design).
  Do NOT use for polishing existing work (use polish).
  Do NOT use for Figma-to-code workflows (use figma-dev-pipeline).
  Do NOT use for TDS (@thakicloud/shared) component usage (follow 03-tds-essentials.mdc).
  Do NOT use for mobile app design via Sleek (use sleek-design-mobile-apps).
  Korean triggers: "디자인 시스템", "Tailwind v4", "컴포넌트 라이브러리",
  "디자인 토큰", "CVA 컴포넌트", "다크 모드 설정", "반응형 그리드".
metadata:
  author: "wshobson/agents"
  version: "1.0.0"
  license: "MIT"
  category: "frontend"
---

# Tailwind Design System (v4)

Build production-ready design systems with Tailwind CSS v4, including CSS-first configuration, design tokens, component variants, responsive patterns, and accessibility.

> **Note**: This skill targets Tailwind CSS v4 (2024+). For v3 projects, refer to the [upgrade guide](https://tailwindcss.com/docs/upgrade-guide).

## When to Use

- Creating a component library with Tailwind v4
- Implementing design tokens and theming with CSS-first configuration
- Building responsive and accessible components
- Standardizing UI patterns across a codebase
- Migrating from Tailwind v3 to v4
- Setting up dark mode with native CSS features

## Key v4 Changes

| v3 Pattern | v4 Pattern |
|---|---|
| `tailwind.config.ts` | `@theme` in CSS |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| `darkMode: "class"` | `@custom-variant dark (&:where(.dark, .dark *))` |
| `theme.extend.colors` | `@theme { --color-*: value }` |
| `require("tailwindcss-animate")` | CSS `@keyframes` in `@theme` + `@starting-style` for entry animations |

## Quick Start

```css
/* app.css - Tailwind v4 CSS-first configuration */
@import "tailwindcss";

@theme {
  /* Semantic color tokens using OKLCH */
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);

  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);

  --color-secondary: oklch(96% 0.01 264);
  --color-secondary-foreground: oklch(14.5% 0.025 264);

  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);

  --color-accent: oklch(96% 0.01 264);
  --color-accent-foreground: oklch(14.5% 0.025 264);

  --color-destructive: oklch(53% 0.22 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);

  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);

  --color-ring-offset: oklch(100% 0 0);

  /* Radius tokens */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;

  /* Animation tokens */
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-fade-out: fade-out 0.2s ease-in;
  --animate-slide-in: slide-in 0.3s ease-out;
  --animate-slide-out: slide-out 0.3s ease-in;

  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes fade-out {
    from { opacity: 1; }
    to { opacity: 0; }
  }

  @keyframes slide-in {
    from { transform: translateY(-0.5rem); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  @keyframes slide-out {
    from { transform: translateY(0); opacity: 1; }
    to { transform: translateY(-0.5rem); opacity: 0; }
  }
}

/* Dark mode variant */
@custom-variant dark (&:where(.dark, .dark *));

.dark {
  --color-background: oklch(14.5% 0.025 264);
  --color-foreground: oklch(98% 0.01 264);

  --color-primary: oklch(98% 0.01 264);
  --color-primary-foreground: oklch(14.5% 0.025 264);

  --color-secondary: oklch(22% 0.02 264);
  --color-secondary-foreground: oklch(98% 0.01 264);

  --color-muted: oklch(22% 0.02 264);
  --color-muted-foreground: oklch(65% 0.02 264);

  --color-accent: oklch(22% 0.02 264);
  --color-accent-foreground: oklch(98% 0.01 264);

  --color-destructive: oklch(42% 0.15 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(22% 0.02 264);
  --color-ring: oklch(83% 0.02 264);

  --color-card: oklch(14.5% 0.025 264);
  --color-card-foreground: oklch(98% 0.01 264);

  --color-ring-offset: oklch(14.5% 0.025 264);
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground antialiased;
  }
}
```

## Core Concepts

### 1. Design Token Hierarchy

```
Brand Tokens (abstract)
    -> Semantic Tokens (purpose)
        -> Component Tokens (specific)

Example:
    oklch(45% 0.2 260) -> --color-primary -> bg-primary
```

### 2. Component Architecture

```
Base styles -> Variants -> Sizes -> States -> Overrides
```

## Patterns

### Pattern 1: CVA (Class Variance Authority) Components

```typescript
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-border bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'size-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

export function Button({
  className, variant, size, asChild = false, ref, ...props
}: ButtonProps & { ref?: React.Ref<HTMLButtonElement> }) {
  const Comp = asChild ? Slot : 'button'
  return (
    <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
  )
}
```

### Pattern 2: Compound Components (React 19)

```typescript
import { cn } from '@/lib/utils'

export function Card({
  className, ref, ...props
}: React.HTMLAttributes<HTMLDivElement> & { ref?: React.Ref<HTMLDivElement> }) {
  return (
    <div ref={ref}
      className={cn('rounded-lg border border-border bg-card text-card-foreground shadow-sm', className)}
      {...props}
    />
  )
}

export function CardHeader({ className, ref, ...props }: React.HTMLAttributes<HTMLDivElement> & { ref?: React.Ref<HTMLDivElement> }) {
  return <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
}

export function CardTitle({ className, ref, ...props }: React.HTMLAttributes<HTMLHeadingElement> & { ref?: React.Ref<HTMLHeadingElement> }) {
  return <h3 ref={ref} className={cn('text-2xl font-semibold leading-none tracking-tight', className)} {...props} />
}

export function CardDescription({ className, ref, ...props }: React.HTMLAttributes<HTMLParagraphElement> & { ref?: React.Ref<HTMLParagraphElement> }) {
  return <p ref={ref} className={cn('text-sm text-muted-foreground', className)} {...props} />
}

export function CardContent({ className, ref, ...props }: React.HTMLAttributes<HTMLDivElement> & { ref?: React.Ref<HTMLDivElement> }) {
  return <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
}

export function CardFooter({ className, ref, ...props }: React.HTMLAttributes<HTMLDivElement> & { ref?: React.Ref<HTMLDivElement> }) {
  return <div ref={ref} className={cn('flex items-center p-6 pt-0', className)} {...props} />
}
```

### Pattern 3: Form Components

```typescript
import { cn } from '@/lib/utils'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string
  ref?: React.Ref<HTMLInputElement>
}

export function Input({ className, type, error, ref, ...props }: InputProps) {
  return (
    <div className="relative">
      <input
        type={type}
        className={cn(
          'flex h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
          error && 'border-destructive focus-visible:ring-destructive',
          className
        )}
        ref={ref}
        aria-invalid={!!error}
        aria-describedby={error ? `${props.id}-error` : undefined}
        {...props}
      />
      {error && (
        <p id={`${props.id}-error`} className="mt-1 text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
    </div>
  )
}
```

### Pattern 4: Responsive Grid System

```typescript
import { cn } from '@/lib/utils'
import { cva, type VariantProps } from 'class-variance-authority'

const gridVariants = cva('grid', {
  variants: {
    cols: {
      1: 'grid-cols-1',
      2: 'grid-cols-1 sm:grid-cols-2',
      3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3',
      4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
    },
    gap: {
      none: 'gap-0', sm: 'gap-2', md: 'gap-4', lg: 'gap-6', xl: 'gap-8',
    },
  },
  defaultVariants: { cols: 3, gap: 'md' },
})

interface GridProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof gridVariants> {}

export function Grid({ className, cols, gap, ...props }: GridProps) {
  return <div className={cn(gridVariants({ cols, gap, className }))} {...props} />
}

const containerVariants = cva('mx-auto w-full px-4 sm:px-6 lg:px-8', {
  variants: {
    size: {
      sm: 'max-w-screen-sm', md: 'max-w-screen-md', lg: 'max-w-screen-lg',
      xl: 'max-w-screen-xl', '2xl': 'max-w-screen-2xl', full: 'max-w-full',
    },
  },
  defaultVariants: { size: 'xl' },
})

interface ContainerProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof containerVariants> {}

export function Container({ className, size, ...props }: ContainerProps) {
  return <div className={cn(containerVariants({ size, className }))} {...props} />
}
```

For advanced animation, dark mode, custom utilities, and migration patterns, see [references/advanced-patterns.md](references/advanced-patterns.md).

## Utility Functions

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const focusRing = cn(
  "focus-visible:outline-none focus-visible:ring-2",
  "focus-visible:ring-ring focus-visible:ring-offset-2",
);

export const disabled = "disabled:pointer-events-none disabled:opacity-50";
```

## Best Practices

### Do

- Use `@theme` blocks for CSS-first configuration
- Use OKLCH colors for better perceptual uniformity
- Compose with CVA for type-safe variants
- Use semantic tokens (`bg-primary` not `bg-blue-500`)
- Use `size-*` shorthand for `w-* h-*`
- Add accessibility (ARIA attributes, focus states)

### Don't

- Use `tailwind.config.ts` (use CSS `@theme`)
- Use `@tailwind` directives (use `@import "tailwindcss"`)
- Use `forwardRef` (React 19 passes ref as prop)
- Use arbitrary values (extend `@theme` instead)
- Hardcode colors (use semantic tokens)
- Forget dark mode testing
