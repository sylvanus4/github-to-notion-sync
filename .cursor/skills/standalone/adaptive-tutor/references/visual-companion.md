# Visual Companion — Browser Mode Reference

The visual companion is an **opt-in** browser-based teaching surface. It pushes rich interactive content (diagrams, quizzes, walkthroughs) to a local browser window. The learner must explicitly request it ("show me in the browser", "open visuals").

**Requirement:** Node.js must be installed. If unavailable, fall back to inline Mermaid diagrams and AskQuestion quizzes.

---

## Lifecycle

### Starting the Server

Use Shell to run the start script. It auto-detects an available port and creates a session directory.

```
Shell: bash .cursor/skills/standalone/adaptive-tutor/scripts/start-server.sh --project-dir "$(pwd)"
```

The script outputs JSON on success:

```json
{
  "port": 3456,
  "url": "http://localhost:3456",
  "screen_dir": "/path/to/session/screens"
}
```

**Save `screen_dir` and `url`** — you need both for the rest of the session.

Tell the learner: "Visual companion started at `<url>`. Open that in your browser."

### Stopping the Server

When the session ends or the learner no longer needs browser visuals:

```
Shell: bash .cursor/skills/standalone/adaptive-tutor/scripts/stop-server.sh <screen_dir>
```

This kills the server process and cleans up the session directory.

---

## Pushing Content

Write HTML fragments to `<screen_dir>/` as `.html` files. The server auto-detects the newest file and serves it. Use sequential naming for clarity: `001-intro.html`, `002-quiz.html`, etc.

```
Write: <screen_dir>/001-concept-diagram.html
```

The fragment is wrapped in `tutor-frame.html` (dark theme, Mermaid support, quiz/walkthrough interactivity) — you only write the inner content.

### Diagram

```html
<div class="diagram">
  <h2>How HTTP Works</h2>
  <pre class="mermaid">
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: GET /index.html
    Server-->>Client: 200 OK + HTML
    Client->>Server: GET /style.css
    Server-->>Client: 200 OK + CSS
  </pre>
</div>
```

Mermaid is loaded from CDN by the frame template. Supported diagram types: `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram-v2`, `mindmap`, `erDiagram`, `gantt`, `pie`.

### Quiz

```html
<div class="quiz" data-answer="b">
  <h3>What does HTTP stand for?</h3>
  <div class="options">
    <button class="option" data-value="a" onclick="checkAnswer(this)">
      Hyper Text Transfer Package
    </button>
    <button class="option" data-value="b" onclick="checkAnswer(this)">
      Hyper Text Transfer Protocol
    </button>
    <button class="option" data-value="c" onclick="checkAnswer(this)">
      High Transfer Text Protocol
    </button>
  </div>
  <div class="feedback"></div>
</div>
```

`data-answer` on `.quiz` sets the correct option. `checkAnswer()` handles feedback display, option locking, and posts a `quiz-answer` event.

### Walkthrough

```html
<div class="walkthrough">
  <h2>Building a REST API — Step by Step</h2>

  <div class="step active" data-step="1">
    <h3>Step 1: Define the Route</h3>
    <pre><code>app.get('/users', (req, res) => {
  res.json(users);
});</code></pre>
    <p>This creates a GET endpoint at <code>/users</code>.</p>
  </div>

  <div class="step" data-step="2">
    <h3>Step 2: Add Error Handling</h3>
    <pre><code>app.get('/users', (req, res) => {
  try {
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});</code></pre>
    <p>Always wrap route handlers in try/catch.</p>
  </div>

  <div class="nav-buttons">
    <button onclick="prevStep()">← Previous</button>
    <button onclick="nextStep()">Next →</button>
  </div>
</div>
```

`prevStep()`/`nextStep()` manage step visibility and post `walkthrough-step` and `walkthrough-complete` events.

---

## Reading Events

The visual companion posts learner interaction events to `<screen_dir>/.events`. Each line is a JSON object.

```
Read: <screen_dir>/.events
```

### Event Types

**Quiz answer:**
```json
{"type": "quiz-answer", "value": "b", "correct": true, "timestamp": "2026-04-05T10:30:00Z"}
```

**Walkthrough step change:**
```json
{"type": "walkthrough-step", "step": 2, "timestamp": "2026-04-05T10:31:00Z"}
```

**Walkthrough completion:**
```json
{"type": "walkthrough-complete", "totalSteps": 5, "timestamp": "2026-04-05T10:35:00Z"}
```

### Using Events in Teaching

- **Quiz wrong answer:** follow up with a targeted Socratic question about the misconception
- **Quiz correct answer:** acknowledge and advance
- **Walkthrough step:** if they spend a long time on a step, proactively ask if they have questions
- **Walkthrough complete:** transition to Active Recall — ask them to explain what they just walked through

---

## Cursor Tool Mapping

| Action | Tool | Details |
|--------|------|---------|
| Start server | Shell | `bash scripts/start-server.sh --project-dir "$(pwd)"` |
| Push content | Write | Write `.html` file to `<screen_dir>/` |
| Read events | Read | Read `<screen_dir>/.events` |
| Stop server | Shell | `bash scripts/stop-server.sh <screen_dir>` |

---

## Design Guidelines

1. **One concept per page** — don't cram multiple diagrams or quizzes into one HTML fragment
2. **Progressive disclosure** — use walkthroughs for complex topics, not one massive diagram
3. **Keep diagrams small** — under 15 nodes. Split large diagrams into multiple pages
4. **Quiz after every major concept** — push a quiz fragment, read the event, adapt
5. **Always have a fallback** — if the server fails to start, switch to inline Mermaid + AskQuestion
