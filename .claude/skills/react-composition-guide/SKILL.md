---
name: react-composition-guide
description: >-
  Scalable React composition patterns for React + Radix UI + Tailwind CSS v4
  stacks. Covers component architecture (avoid boolean props, compound
  components), state management (decouple state from UI, generic context, lift
  state), implementation patterns (explicit variants, children over render
  props), and React 19 API changes. Adapted from Vercel's composition-patterns
  skill.
---

# React Composition Guide

**4 categories · 9 patterns · React + Radix UI + Tailwind CSS v4 stack**

Composition patterns for building flexible, maintainable React components.
Avoid boolean prop proliferation by using compound components, lifting
state, and composing internals.

---

## 1. Component Architecture — **HIGH**

### 1.1 Avoid Boolean Prop Proliferation — CRITICAL

Don't add boolean props like `isThread`, `isEditing`, `isDMThread` to
customize behavior. Each boolean doubles possible states, creating
unmaintainable conditional logic. Use composition instead.

**Bad: boolean props create exponential complexity**

```tsx
function Composer({
  onSubmit,
  isThread,
  channelId,
  isDMThread,
  isEditing,
  isForwarding,
}: Props) {
  return (
    <form>
      <Header />
      <Input />
      {isDMThread ? (
        <AlsoSendToDMField />
      ) : isThread ? (
        <AlsoSendToChannelField id={channelId} />
      ) : null}
      {isEditing ? <EditActions /> : isForwarding ? <ForwardActions /> : <DefaultActions />}
      <Footer onSubmit={onSubmit} />
    </form>
  )
}
```

**Good: composition eliminates conditionals**

```tsx
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Attachments />
        <Composer.Formatting />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <AlsoSendToChannelField id={channelId} />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

function EditComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer>
        <Composer.CancelEdit />
        <Composer.SaveEdit />
      </Composer.Footer>
    </Composer.Frame>
  )
}
```

Each variant is explicit. Internals are shared without a monolithic parent.

### 1.2 Use Compound Components — HIGH

Share implicit state between related components via React Context.

```tsx
import * as React from 'react'

type AccordionContextType = {
  openItem: string | null
  toggle: (id: string) => void
}

const AccordionContext = React.createContext<AccordionContextType | null>(null)

function useAccordion() {
  const ctx = React.useContext(AccordionContext)
  if (!ctx) throw new Error('useAccordion must be used within Accordion')
  return ctx
}

function Accordion({ children }: { children: React.ReactNode }) {
  const [openItem, setOpenItem] = React.useState<string | null>(null)
  const toggle = (id: string) => setOpenItem((prev) => (prev === id ? null : id))
  return (
    <AccordionContext.Provider value={{ openItem, toggle }}>
      <div className="divide-y divide-border">{children}</div>
    </AccordionContext.Provider>
  )
}

function AccordionItem({ id, title, children }: {
  id: string; title: string; children: React.ReactNode
}) {
  const { openItem, toggle } = useAccordion()
  const isOpen = openItem === id
  return (
    <div>
      <button
        className="flex w-full items-center justify-between py-3 text-sm font-medium"
        onClick={() => toggle(id)}
        aria-expanded={isOpen}
      >
        {title}
        <ChevronIcon className={isOpen ? 'rotate-180' : ''} />
      </button>
      {isOpen && <div className="pb-3 text-sm text-muted-foreground">{children}</div>}
    </div>
  )
}

Accordion.Item = AccordionItem
```

**With Radix UI** — Radix already provides compound component APIs.
Compose around them instead of reinventing:

```tsx
import * as AccordionPrimitive from '@radix-ui/react-accordion'

function Accordion({ children }: { children: React.ReactNode }) {
  return (
    <AccordionPrimitive.Root type="single" collapsible className="divide-y divide-border">
      {children}
    </AccordionPrimitive.Root>
  )
}

function AccordionItem({ value, title, children }: {
  value: string; title: string; children: React.ReactNode
}) {
  return (
    <AccordionPrimitive.Item value={value}>
      <AccordionPrimitive.Header>
        <AccordionPrimitive.Trigger className="flex w-full items-center justify-between py-3 text-sm font-medium">
          {title}
        </AccordionPrimitive.Trigger>
      </AccordionPrimitive.Header>
      <AccordionPrimitive.Content className="pb-3 text-sm text-muted-foreground">
        {children}
      </AccordionPrimitive.Content>
    </AccordionPrimitive.Item>
  )
}
```

---

## 2. State Management — **MEDIUM**

### 2.1 Decouple State Management from UI — MEDIUM

Separate what the component *does* from what it *looks like*. Use custom
hooks to encapsulate business logic.

```tsx
function useComposer() {
  const [content, setContent] = React.useState('')
  const [attachments, setAttachments] = React.useState<File[]>([])

  const submit = async () => {
    await api.send({ content, attachments })
    setContent('')
    setAttachments([])
  }

  const addAttachment = (file: File) => setAttachments((prev) => [...prev, file])

  return { content, setContent, attachments, addAttachment, submit }
}

function ChannelComposer() {
  const composer = useComposer()
  return (
    <Composer.Frame>
      <Composer.Input value={composer.content} onChange={composer.setContent} />
      <Composer.AttachmentList files={composer.attachments} />
      <Composer.Footer>
        <Composer.AttachButton onAttach={composer.addAttachment} />
        <Composer.SubmitButton onSubmit={composer.submit} />
      </Composer.Footer>
    </Composer.Frame>
  )
}
```

### 2.2 Define Generic Context Interfaces for Dependency Injection — MEDIUM

Define context shapes as interfaces, not concrete implementations, so
different providers can supply different backends.

```tsx
interface DataSource<T> {
  items: T[]
  isLoading: boolean
  error: Error | null
  refetch: () => void
}

const DataContext = React.createContext<DataSource<unknown> | null>(null)

function useDataSource<T>() {
  const ctx = React.useContext(DataContext) as DataSource<T> | null
  if (!ctx) throw new Error('useDataSource must be used within a DataProvider')
  return ctx
}

function SWRDataProvider<T>({ url, children }: { url: string; children: React.ReactNode }) {
  const { data, error, isLoading, mutate } = useSWR<T[]>(url, fetcher)
  return (
    <DataContext.Provider value={{ items: data ?? [], isLoading, error, refetch: mutate }}>
      {children}
    </DataContext.Provider>
  )
}

function StaticDataProvider<T>({ data, children }: { data: T[]; children: React.ReactNode }) {
  return (
    <DataContext.Provider value={{ items: data, isLoading: false, error: null, refetch: () => {} }}>
      {children}
    </DataContext.Provider>
  )
}
```

### 2.3 Lift State into Provider Components — MEDIUM

When multiple sibling components need the same state, lift it into a
shared provider rather than prop-drilling.

```tsx
type FilterContextType = {
  filters: Record<string, string>
  setFilter: (key: string, value: string) => void
  clearFilters: () => void
}

const FilterContext = React.createContext<FilterContextType | null>(null)

function FilterProvider({ children }: { children: React.ReactNode }) {
  const [filters, setFilters] = React.useState<Record<string, string>>({})

  const setFilter = (key: string, value: string) =>
    setFilters((prev) => ({ ...prev, [key]: value }))

  const clearFilters = () => setFilters({})

  return (
    <FilterContext.Provider value={{ filters, setFilter, clearFilters }}>
      {children}
    </FilterContext.Provider>
  )
}

function FilterBar() {
  const { filters, setFilter, clearFilters } = React.useContext(FilterContext)!
  return (
    <div className="flex items-center gap-2">
      <SelectFilter value={filters.status} onChange={(v) => setFilter('status', v)} />
      <button onClick={clearFilters} className="text-sm text-muted-foreground">Clear</button>
    </div>
  )
}

function DataTable() {
  const { filters } = React.useContext(FilterContext)!
  const filteredData = useFilteredData(filters)
  return <Table data={filteredData} />
}

function Page() {
  return (
    <FilterProvider>
      <FilterBar />
      <DataTable />
    </FilterProvider>
  )
}
```

---

## 3. Implementation Patterns — **MEDIUM**

### 3.1 Create Explicit Component Variants — MEDIUM

Instead of boolean flags, export named variant components that each
compose shared internals.

```tsx
function AlertBase({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn('rounded-lg border p-4 text-sm', className)}>
      {children}
    </div>
  )
}

function InfoAlert({ children }: { children: React.ReactNode }) {
  return (
    <AlertBase className="border-blue-200 bg-blue-50 text-blue-800 dark:border-blue-800 dark:bg-blue-950 dark:text-blue-200">
      <InfoIcon className="mr-2 inline-block h-4 w-4" />
      {children}
    </AlertBase>
  )
}

function ErrorAlert({ children }: { children: React.ReactNode }) {
  return (
    <AlertBase className="border-red-200 bg-red-50 text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-200">
      <AlertCircleIcon className="mr-2 inline-block h-4 w-4" />
      {children}
    </AlertBase>
  )
}
```

### 3.2 Prefer Composing Children Over Render Props — MEDIUM

Children composition is simpler and more readable than render props for
most cases.

```tsx
// ❌ Render prop — harder to read
<DataLoader
  url="/api/users"
  render={(data) => <UserList users={data} />}
/>

// ✅ Children composition
<DataProvider url="/api/users">
  <UserList />
</DataProvider>

// UserList reads from context
function UserList() {
  const { items } = useDataSource<User>()
  return (
    <ul>
      {items.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

Use render props only when the child truly needs dynamic data that can't
be provided via context (e.g., virtualized list item renderers).

---

## 4. React 19 API Changes — **MEDIUM**

### 4.1 use() Replaces useContext() — MEDIUM

In React 19, `use()` can read context (and promises) conditionally:

```tsx
import { use } from 'react'

function ThemeButton() {
  const theme = use(ThemeContext) // can be called conditionally
  return <button className={theme === 'dark' ? 'bg-gray-800' : 'bg-white'}>Click</button>
}
```

### 4.2 ref as Regular Prop — LOW

React 19 eliminates the need for `forwardRef`:

```tsx
// React 19+ — ref is just a prop
function Input({ ref, className, ...props }: React.ComponentProps<'input'>) {
  return <input ref={ref} className={cn('border rounded px-3 py-2', className)} {...props} />
}
```

### 4.3 useActionState for Form Actions — MEDIUM

```tsx
import { useActionState } from 'react'

async function createItem(_prev: State, formData: FormData) {
  const result = await api.create(Object.fromEntries(formData))
  return result.error ? { error: result.error } : { success: true }
}

function CreateForm() {
  const [state, action, isPending] = useActionState(createItem, { error: null })
  return (
    <form action={action}>
      <input name="title" required />
      {state.error && <p className="text-sm text-destructive">{state.error}</p>}
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating…' : 'Create'}
      </button>
    </form>
  )
}
```

### 4.4 useOptimistic for Instant Feedback — MEDIUM

```tsx
import { useOptimistic } from 'react'

function TodoList({ items }: { items: Todo[] }) {
  const [optimisticItems, addOptimistic] = useOptimistic(
    items,
    (state, newItem: Todo) => [...state, { ...newItem, pending: true }],
  )

  async function handleAdd(formData: FormData) {
    const newTodo = { id: crypto.randomUUID(), title: formData.get('title') as string }
    addOptimistic(newTodo)
    await api.createTodo(newTodo)
  }

  return (
    <div>
      <form action={handleAdd}>
        <input name="title" />
        <button type="submit">Add</button>
      </form>
      <ul>
        {optimisticItems.map((item) => (
          <li key={item.id} className={item.pending ? 'opacity-50' : ''}>
            {item.title}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

---

## Quick Reference: When to Apply

| Situation | Pattern |
|---|---|
| Component has 3+ boolean props | 1.1 Avoid Boolean Proliferation |
| Related components share state | 1.2 Compound Components |
| Business logic mixed with JSX | 2.1 Decouple State from UI |
| Multiple data sources for same UI | 2.2 Generic Context Interface |
| Siblings need shared state | 2.3 Lift State into Provider |
| Visual variants of same base | 3.1 Explicit Variants |
| Passing render functions as props | 3.2 Children over Render Props |
| Using `useContext()` | 4.1 Migrate to `use()` |
| Using `forwardRef` | 4.2 Use `ref` as prop |
| Form submission with state | 4.3 `useActionState` |
| Instant UI feedback for mutations | 4.4 `useOptimistic` |

---

## Radix UI Integration Notes

When using Radix UI primitives in this project:

1. **Don't reinvent compound components** that Radix already provides
   (Dialog, Accordion, DropdownMenu, Select, etc.)
2. **Compose around Radix primitives** — wrap them with project-specific
   styling and behavior rather than building from scratch
3. **Use Radix's built-in accessibility** — don't add redundant ARIA attributes
   that Radix already manages
4. **Style with Tailwind CSS v4** — use `className` on Radix primitives,
   leveraging `data-[state=*]` selectors for state-based styling:

```tsx
<AccordionPrimitive.Trigger
  className="data-[state=open]:text-foreground data-[state=closed]:text-muted-foreground"
>
```
