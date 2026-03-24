# Terminology Glossary (Cloud UX)

Approved, prohibited, and replacement terms for cloud service UX copy.
Apply during generation to ensure consistent terminology across all UI surfaces.

---

## How to Use

1. **Before generating copy**, scan the output for any Prohibited terms.
2. **Replace** prohibited terms with their Approved alternative.
3. **When a term is not listed**, use the cloud provider's most common
   convention (AWS/GCP/Azure consensus).
4. **Flag new terms** that need glossary inclusion in the output's Usage Notes.

---

## Core Cloud Terms

| Approved Term | Prohibited / Avoid | Notes |
|--------------|-------------------|-------|
| instance | server, machine, box, VM (unless product-specific) | Generic compute unit. Use product-specific term if the product defines one. |
| resource | object, thing, item, entity | Generic term for any cloud-managed unit. |
| region | location, area, zone (unless AZ-specific) | Geographic deployment area. Use "availability zone" for AZ. |
| availability zone | AZ (in user-facing copy) | Spell out in UI text; abbreviation OK in developer docs. |
| deploy | push, ship, roll out | Standard term for making code/config live. |
| provision | spin up, fire up, stand up | Create and configure a new resource. |
| terminate | kill, destroy, nuke | Permanently end a resource. Use for irreversible compute shutdown. |
| delete | remove, erase, wipe | Permanently remove data or configuration. |
| stop | pause, freeze, suspend | Reversible halt of a running resource. |
| start | boot, launch, resume | Begin or resume a stopped resource. |
| scale | grow, shrink, resize | Adjust capacity. Specify direction: "scale up/down/out/in". |
| configure | set up, tweak, adjust | Change settings or parameters. |
| credentials | creds, secrets, login info | Authentication materials. |
| API key | token (unless specifically an OAuth token) | Identifier for API access. Distinguish from auth tokens. |
| endpoint | URL, link, address | The network address for an API or service. |
| quota | limit, cap, ceiling | Maximum allowed usage of a resource type. |
| billing | charges, fees, costs | Financial aspects. Use "billing" as the category. |
| dashboard | home page, landing page, main screen | Primary monitoring/overview interface. |

---

## Action Terms

| Approved | Prohibited / Avoid | Notes |
|----------|-------------------|-------|
| create | add, new, make | Primary action for provisioning. "Create instance", not "Add instance". |
| edit | modify, change, alter | Update existing configuration. |
| save | apply, commit, store | Persist changes. "Save" for settings; "apply" only for staged config changes. |
| cancel | abort, exit, quit, back out | Abandon an in-progress action. |
| enable | turn on, activate, switch on | Activate a feature or setting. |
| disable | turn off, deactivate, switch off | Deactivate a feature or setting. |
| select | choose, pick, check | Make a selection from options. |
| upload | send, push, transfer | Move a file from local to cloud. |
| download | pull, fetch, get | Move a file from cloud to local. |
| connect | link, attach, hook up | Establish a connection between services. |
| disconnect | unlink, detach, unhook | Remove a connection. |
| retry | try again, redo, re-run | Attempt a failed action again. |
| refresh | reload, update, sync | Reload current data from the server. |

---

## Status Terms

| Approved | Prohibited / Avoid | Notes |
|----------|-------------------|-------|
| running | active, alive, up, live | Resource is operational. |
| stopped | paused, suspended, halted, down | Resource exists but is not running. |
| terminated | killed, dead, destroyed | Resource permanently ended. |
| pending | initializing, waiting, queued | Action in progress, not yet complete. |
| failed | broken, errored, crashed, error state | Action did not complete successfully. |
| healthy | good, OK, normal | Resource is functioning within expected parameters. |
| degraded | unhealthy, impaired, struggling | Resource is functional but underperforming. |
| unavailable | offline, unreachable, inaccessible | Resource cannot be reached. |

---

## Prohibited Patterns

These patterns should never appear in cloud service UI copy:

| Pattern | Why | Replace With |
|---------|-----|-------------|
| "Please note that..." | Filler; adds nothing | State the information directly |
| "In order to..." | Verbose for "To..." | "To..." |
| "It should be noted..." | Passive filler | State the fact directly |
| "Successfully" (in success toasts) | Redundant — the success state implies it | "Instance created." not "Instance created successfully." |
| "Are you sure?" | Vague; doesn't state consequences | State what will happen specifically |
| "Click here" | Accessibility anti-pattern | Use descriptive link text |
| "Please try again later" | Vague timeline; unhelpful | State when to try or give alternatives |
| "Oops", "Whoops", "Uh oh" | Unprofessional for enterprise cloud | State the error directly |
| "An error has occurred" | Vague | Describe the specific error |
| "Something went wrong" | Vague | Describe what specifically failed |
| "Invalid input" | Vague | State what's invalid and the expected format |
| "Contact administrator" (alone) | Unhelpful without context | Include what the admin should do or check |

---

## Capitalization Rules

| Element | Rule | Example |
|---------|------|---------|
| Page titles | Title Case | "Instance Settings" |
| Button labels | Title Case | "Create Instance" |
| Tab labels | Title Case | "Network Configuration" |
| Menu items | Title Case | "Access Management" |
| Form field labels | Sentence case | "Instance name" |
| Tooltips | Sentence case | "Choose a region close to your users." |
| Error messages | Sentence case | "The instance couldn't be created." |
| Status messages | Sentence case | "Instance created." |
| Descriptions | Sentence case | "Auto-scaling adjusts instance count..." |
| Column headers | Sentence case | "Last modified" |

---

## Pluralization

| Scenario | Pattern | Example |
|----------|---------|---------|
| Zero items | "No {resources}" | "No instances" |
| One item | "1 {resource}" | "1 instance" |
| Multiple items | "{N} {resources}" | "3 instances" |
| Unknown count | "{resources}" (plural) | "Instances" (as a page title) |

Never use "(s)" for optional plurals. Use the appropriate singular or plural
form based on the actual count.
