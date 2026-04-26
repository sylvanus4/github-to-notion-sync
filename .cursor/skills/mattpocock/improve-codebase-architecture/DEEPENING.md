# Deepening Modules

Techniques for making existing modules deeper — absorbing complexity into their implementation while simplifying their interface.

## When to Deepen

A module is a candidate for deepening when:

- Callers frequently combine multiple calls to the module in the same pattern
- Callers pass information through the module that only the module's internals use
- Error handling is duplicated across callers
- Configuration is copy-pasted between call sites
- The module's tests are simpler than its callers' tests (the complexity leaked upward)

## Technique 1: Absorb Adjacent Logic

Look at what callers do **immediately before and after** calling your module. If most callers perform the same setup or cleanup, that logic belongs inside the module.

**Before:**
```typescript
const config = loadSmtpConfig();
const template = loadTemplate("welcome");
const html = renderTemplate(template, { name: user.name });
await emailService.send(config, user.email, html);
await retryQueue.enqueue(emailId);
```

**After:**
```typescript
await emailService.sendWelcome(user);
```

The module absorbs config loading, template selection, rendering, and retry logic.

## Technique 2: Replace Configuration with Conventions

When a module requires configuration that follows a pattern, replace explicit config with conventions.

**Before:**
```typescript
const db = new Database({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});
```

**After:**
```typescript
const db = Database.fromEnvironment();
```

The module knows the convention for environment variable names and handles parsing.

## Technique 3: Internalize Error Recovery

If callers all handle errors the same way, the module should handle them internally.

**Before:**
```typescript
try {
  await api.fetchData(url);
} catch (e) {
  if (e instanceof TimeoutError) {
    await sleep(1000);
    await api.fetchData(url); // retry once
  } else {
    throw e;
  }
}
```

**After:**
```typescript
await api.fetchData(url); // retries internally
```

The module owns the retry policy. Callers who need custom retry behavior can use a separate, explicit method.

## Technique 4: Merge Shallow Modules

Two shallow modules that are always used together should become one deep module. The combination hides the interaction pattern.

**Signs two modules should merge:**
- They share most of their dependencies
- Changes to one always require changes to the other
- Callers always import both
- They reference each other's internal types

**Caution:** Only merge if the result is deeper than either part. If two modules are genuinely independent (changes to one don't affect the other), keep them separate even if they're both shallow.

## Technique 5: Layer Reduction

Unnecessary layers add interfaces without hiding anything. Each layer is a potential pass-through.

**Detection:** Walk through a common operation from top to bottom. If you pass through layers that just forward the call, those layers are candidates for removal.

**Fix:** Remove the layer and have the caller talk directly to the module underneath. Or, give the layer genuine responsibility that justifies its existence.

## Measuring Depth

A module's depth can be roughly estimated by the ratio:

```
Depth ≈ (implementation complexity) / (interface complexity)
```

Where:
- **Interface complexity** = number of public methods × average parameter count + number of public types
- **Implementation complexity** = the amount of non-trivial logic, decisions, and state management hidden inside

A deep module has high implementation complexity and low interface complexity. The exact numbers don't matter — what matters is the trend. When you change a module, ask: "Did I make the interface simpler or more complex? Did I hide more or expose more?"
