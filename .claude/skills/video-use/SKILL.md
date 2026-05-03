---
name: video-use
description: >-
  Edit any video by conversation — transcribe, cut, color grade, generate
  overlay animations, burn subtitles. For talking heads, montages, tutorials,
  travel, interviews. No presets, no menus. Ask → confirm → execute → iterate
  → persist. Production-correctness rules are hard; everything else is
  artistic freedom. Based on browser-use/video-use. Use when the user asks to
  'edit a video', 'cut this video', 'transcribe video', 'color grade', 'add
  subtitles', 'trim video', 'montage edit', 'video editing', 'burn subs',
  'generate EDL', 'render video from EDL', 'filmstrip view', 'batch
  transcribe', 'pack transcripts', 'video timeline', 'talking head edit',
  'interview edit', 'tutorial edit', 'travel video edit', '영상 편집', '비디오 편집',
  '자막 입히기', '컬러 그레이딩', '영상 자르기', '영상 트랜스크립션', '몽타주 편집', 'EDL 생성', '타임라인 보기',
  or any request to edit, cut, grade, subtitle, or render video content via
  conversation. Do NOT use for AI video generation from text prompts (use
  pika-text-to-video). Do NOT use for Remotion programmatic motion graphics
  without source footage (use remotion-motion-forge). Do NOT use for video
  compression only (use video-compress). Do NOT use for video script writing
  without footage (use video-script-generator). Do NOT use for post-production
  editing plans without execution (use video-editing-planner). Do NOT use for
  subtitle formatting from existing transcripts (use
  caption-subtitle-formatter). Do NOT use for YouTube transcript extraction
  only (use defuddle). Do NOT use for NotebookLM video explainers (use
  nlm-video).
disable-model-invocation: true
---

# Video Use

## Principle

1. **LLM reasons from raw transcript + on-demand visuals.** The only derived artifact that earns its keep is a packed phrase-level transcript (`takes_packed.md`). Everything else — filler tagging, retake detection, shot classification, emphasis scoring — you derive at decision time.
2. **Audio is primary, visuals follow.** Cut candidates come from speech boundaries and silence gaps. Drill into visuals only at decision points.
3. **Ask → confirm → execute → iterate → persist.** Never touch the cut until the user has confirmed the strategy in plain English.
4. **Generalize.** Do not assume what kind of video this is. Look at the material, ask the user, then edit.
5. **Artistic freedom is the default.** Every specific value, preset, font, color, duration, pitch structure, and technique in this document is a *worked example* from one proven video — not a mandate. Read them to understand what's possible and why each worked. Then make your own taste calls based on what the material actually is and what the user actually wants. **The only things you MUST do are in the Hard Rules section below.** Everything else is yours.
6. **Invent freely.** If the material calls for a technique not described here — split-screen, picture-in-picture, lower-third identity cards, reaction cuts, speed ramps, freeze frames, crossfades, match cuts, L-cuts, J-cuts, speed ramps over breath, whatever — build it. The helpers are ffmpeg and PIL. They can do anything the format supports. Do not wait for permission.
7. **Verify your own output before showing it to the user.** If you wouldn't ship it, don't present it.

## Hard Rules (production correctness — non-negotiable)

These are the things where deviation produces silent failures or broken output. They are not taste, they are correctness. Memorize them.

1. **Subtitles are applied LAST in the filter chain**, after every overlay. Otherwise overlays hide captions. Silent failure.
2. **Per-segment extract → lossless `-c copy` concat**, not single-pass filtergraph. Otherwise you double-encode every segment when overlays are added.
3. **30ms audio fades at every segment boundary** (`afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03`). Otherwise audible pops at every cut.
4. **Overlays use `setpts=PTS-STARTPTS+T/TB`** to shift the overlay's frame 0 to its window start. Otherwise you see the middle of the animation during the overlay window.
5. **Master SRT uses output-timeline offsets**: `output_time = word.start - segment_start + segment_offset`. Otherwise captions misalign after segment concat.
6. **Never cut inside a word.** Snap every cut edge to a word boundary from the Scribe transcript.
7. **Pad every cut edge.** Working window: 30–200ms. Scribe timestamps drift 50–100ms — padding absorbs the drift. Tighter for fast-paced, looser for cinematic.
8. **Word-level verbatim ASR only.** Never SRT/phrase mode (loses sub-second gap data). Never normalized fillers (loses editorial signal).
9. **Cache transcripts per source.** Never re-transcribe unless the source file itself changed.
10. **Parallel sub-agents for multiple animations.** Never sequential. Spawn N at once via the `Agent` tool; total wall time ≈ slowest one.
11. **Strategy confirmation before execution.** Never touch the cut until the user has approved the plain-English plan.
12. **All session outputs in `<videos_dir>/edit/`.** Never write inside the `video-use/` project directory.

Everything else in this document is a worked example. Deviate whenever the material calls for it.

## Directory layout

### Skill directory (`video-use/`)

```
video-use/
├── SKILL.md                     ← this file
├── pyproject.toml               ← Python package metadata + deps
├── .gitignore
├── helpers/
│   ├── __init__.py
│   ├── transcribe.py            ← single-file ElevenLabs Scribe
│   ├── transcribe_batch.py      ← 4-worker parallel transcription
│   ├── pack_transcripts.py      ← word-level → phrase-level markdown
│   ├── timeline_view.py         ← filmstrip + waveform PNG
│   ├── render.py                ← EDL → final video pipeline
│   ├── grade.py                 ← ffmpeg color grade presets + custom
│   ├── healthcheck.py           ← dependency verification
│   ├── self_eval.py             ← post-render quality evaluation
│   └── pipeline.py              ← full workflow orchestrator
├── examples/
│   └── edl_template.json        ← annotated EDL schema reference
└── skills/
    └── manim-video/
        └── SKILL.md             ← animation overlay sub-skill
```

### User session directory (`<videos_dir>/edit/`)

All session outputs go here. User footage lives wherever they put it.

```
<videos_dir>/
├── <source files, untouched>
└── edit/
    ├── project.md               ← memory; appended every session
    ├── takes_packed.md          ← phrase-level transcripts, the LLM's primary reading view
    ├── edl.json                 ← cut decisions
    ├── transcripts/<name>.json  ← cached raw Scribe JSON
    ├── animations/slot_<id>/    ← per-animation source + render + reasoning
    ├── clips_graded/            ← per-segment extracts with grade + fades
    ├── master.srt               ← output-timeline subtitles
    ├── downloads/               ← yt-dlp outputs
    ├── verify/                  ← debug frames / timeline PNGs
    ├── preview.mp4
    └── final.mp4
```

## First Response Protocol

When this skill activates, follow this sequence before any editing work:

1. **Healthcheck** — run `python helpers/healthcheck.py --strict`. If required deps fail, guide the user through setup before proceeding. Do not silently skip.
2. **Inventory sources** — `ffprobe` every file the user points to. Report: codec, resolution, fps, duration, audio channels. If sources are URLs, download with `yt-dlp` first.
3. **Transcribe** — `python helpers/transcribe_batch.py <dir>` (or single `transcribe.py`) for all source files. Check transcript cache — never re-transcribe cached sources.
4. **Pack** — `python helpers/pack_transcripts.py --edit-dir <edit>` to produce `takes_packed.md`.
5. **First impression** — read `takes_packed.md`, sample 1-2 `timeline_view` frames at interesting moments. Then describe what you see to the user in plain language.
6. **Converse** — ask questions shaped by the material (not a fixed checklist), collect the editing brief.
7. **Propose strategy** — 4-8 sentences. Wait for explicit confirmation before touching any cut.

If `project.md` exists in the edit directory, read it first and summarize the last session in one sentence before asking whether to continue.

## Setup

### Required
- `ffmpeg` + `ffprobe` on PATH (`brew install ffmpeg` on macOS).
- `ELEVENLABS_API_KEY` in `.env` at project root or env var. The agent will ask and write `.env` if missing.
- Python deps: `pip install -e .` from this skill's directory (or `pip install requests pillow numpy`).

### Health check
Run `python helpers/healthcheck.py` to verify all dependencies at once. Use `--strict` to exit non-zero on missing required deps.

### Optional (installed on first use)
- `yt-dlp` — for downloading source videos from URLs (`brew install yt-dlp` or `pip install yt-dlp`).
- `manim` — for mathematical/technical animation overlays (`pip install manim`). Requires LaTeX: `brew install --cask mactex` on macOS, `apt install texlive-full` on Linux.
- Remotion — for React-based motion graphics (see remotion-motion-forge skill).

### Sub-skills
- This skill vendors `skills/manim-video/`. Read its SKILL.md when building a Manim animation slot.

## Helpers

All helper scripts live in `helpers/` within this skill directory.

- **`transcribe.py <video>`** — single-file Scribe call. `--num-speakers N` optional. Cached.
- **`transcribe_batch.py <videos_dir>`** — 4-worker parallel transcription. Use for multi-take. Includes `sys.path` fix for cross-helper imports.
- **`pack_transcripts.py --edit-dir <dir>`** — `transcripts/*.json` → `takes_packed.md` (phrase-level, break on silence ≥ 0.5s). Handles `FileNotFoundError` and malformed JSON gracefully. Optional `-o <path>` to override default output location.
- **`timeline_view.py <video> <start> <end>`** — filmstrip + waveform PNG. On-demand visual drill-down. **Not a scan tool** — use it at decision points, not constantly. `--edl <file>` mode generates a multi-segment composite: each EDL range gets its own filmstrip row with waveform, segment labels, timing info, silence highlights, and color-coded boundary markers — stacked vertically into a single PNG for full-edit overview.
- **`render.py <edl.json> -o <out>`** — per-segment extract → concat → overlays (PTS-shifted) → subtitles LAST. Validates EDL structure before rendering. Flags: `--preview` (1080p, medium preset, CRF 22), `--draft` (720p, ultrafast preset, CRF 28), `--dry-run` (validate EDL + print segment plan without rendering), `--no-loudnorm` (skip 2-pass loudness normalization), `--no-subtitles` (skip subtitles even if EDL references one), `--build-subtitles` (generate master.srt inline).
- **`grade.py <in> -o <out>`** — ffmpeg filter chain grade. Presets + `--filter '<raw>'` for custom. Raises `RuntimeError` with stderr tail on ffmpeg failure. Additional flags: `--analyze <clip>` (print auto-grade filter without writing output), `--list-presets` (list available presets), `--print-preset <name>` (print filter string for a preset).
- **`healthcheck.py`** — verify all external deps (ffmpeg, ffprobe, yt-dlp, manim, API keys, Python packages). Searches for `ELEVENLABS_API_KEY` in skill root `.env`, CWD `.env`, and `~/.env` before reporting failure. `--strict` exits non-zero on failures.
- **`self_eval.py <rendered.mp4>`** — post-render quality gate. Runs `ffprobe` to verify container format, codecs, resolution, framerate; measures integrated loudness (LUFS) and true peak via ffmpeg loudnorm filter; optionally compares actual duration against EDL expected total (`--edl <file>`). Outputs a structured PASS/FAIL report with per-check detail. `--json` for machine-readable output.
- **`pipeline.py <project_dir> --edl <edl.json> -o <out>`** — full workflow orchestrator. Chains `healthcheck → transcribe_batch → pack_transcripts → render → self_eval` in sequence with per-stage timing and PASS/FAIL tracking. Flags: `--stage <name>` (run single stage), `--preview`/`--draft` (quality modes passed to render), `--workers N` (transcription parallelism), `--skip-healthcheck`, `--no-eval`. Exits non-zero if any required stage fails.

### Examples

- **`examples/edl_template.json`** — annotated EDL template showing the `sources`/`ranges`/`overlays`/`subtitles` schema. Copy and adapt for your project.

For animations, create `<edit>/animations/slot_<id>/` with `Bash` and spawn a sub-agent via the `Agent` tool.

## The process

1. **Inventory.** `ffprobe` every source. `transcribe_batch.py` on the directory. `pack_transcripts.py` to produce `takes_packed.md`. Sample one or two `timeline_view`s for a visual first impression.
2. **Pre-scan for problems.** One pass over `takes_packed.md` to note verbal slips, obvious mis-speaks, or phrasings to avoid. Plain list, feed into the editor brief.
3. **Converse.** Describe what you see in plain English. Ask questions *shaped by the material*. Collect: content type, target length/aspect, aesthetic/brand direction, pacing feel, must-preserve moments, must-cut moments, animation and grade preferences, subtitle needs. Do not use a fixed checklist — the right questions are different every time.
4. **Propose strategy.** 4–8 sentences: shape, take choices, cut direction, animation plan, grade direction, subtitle style, length estimate. **Wait for confirmation.**
5. **Execute.** Produce `edl.json` via the editor sub-agent brief. Drill into `timeline_view` at ambiguous moments. Build animations in parallel sub-agents. Apply grade per-segment. Compose via `render.py`.
6. **Preview.** `render.py --preview` (or `--draft` for fastest iteration).
7. **Self-eval (before showing the user).** Two-layer verification:

   **Layer 1 — Automated** (`self_eval.py`): Run `python helpers/self_eval.py <output.mp4> --edl <edl.json>`. This checks codec, resolution, fps, loudness (LUFS ±2 of -14), true peak (≤ 0 dBTP), and duration drift (< 1s vs EDL). If any check fails, fix the cause and re-render before proceeding.

   **Layer 2 — Visual spot-check** (`timeline_view`): Run `timeline_view` on the **rendered output** (not the sources) at every cut boundary (±1.5s window). Check each image for:
   - Visual discontinuity / flash / jump at the cut
   - Waveform spike at the boundary (audio pop that slipped past the 30ms fade)
   - Subtitle hidden behind an overlay (Rule 1 violation)
   - Overlay misaligned or showing wrong frames (Rule 4 violation)

   Also sample: first 2s, last 2s, and 2–3 mid-points — check grade consistency, subtitle readability, overall coherence.

   If anything fails: fix → re-render → re-eval. **Cap at 3 self-eval passes** — if issues remain after 3, flag them to the user rather than looping forever. Only present the preview once the self-eval passes.
8. **Final render.** On user confirmation, run full-quality render (no `--preview`/`--draft` flags). Run `self_eval.py` once more on the final output.
9. **Iterate + persist.** Natural-language feedback, re-plan, re-render. Never re-transcribe. Append to `project.md`.

### Full pipeline shortcut

For automated or batch workflows, use `pipeline.py` to chain all stages:

```bash
python helpers/pipeline.py <project_dir> --edl <edl.json> -o <output.mp4>
python helpers/pipeline.py <project_dir> --edl <edl.json> -o <output.mp4> --draft
python helpers/pipeline.py <project_dir> --stage transcribe
```

This runs: `healthcheck → transcribe → pack → render → self_eval` with per-stage timing and PASS/FAIL tracking. Use `--skip-healthcheck` or `--no-eval` to skip stages.

## Cut craft (techniques)

- **Audio-first.** Candidate cuts from word boundaries and silence gaps.
- **Preserve peaks.** Laughs, punchlines, emphasis beats. Extend past punchlines to include reactions — the laugh IS the beat.
- **Speaker handoffs** benefit from air between utterances. Common values: 400–600ms. Less for fast-paced, more for cinematic. Taste call.
- **Audio events as signals.** `(laughs)`, `(sighs)`, `(applause)` mark beats. Extend past them.
- **Silence gaps are cut candidates.** Silences ≥400ms are usually the cleanest. 150–400ms phrase boundaries are usable with a visual check. <150ms is unsafe (mid-phrase).
- **Example cut padding** (the launch video shipped with this): 50ms before the first kept word, 80ms after the last. Tighter for montage energy, looser for documentary. Stay in the 30–200ms working window (Hard Rule 7).
- **Never reason audio and video independently.** Every cut must work on both tracks.

## The packed transcript (primary reading view)

`pack_transcripts.py` reads all `transcripts/*.json` and produces one markdown file where each take is a list of phrase-level lines, each prefixed with its `[start-end]` time range. Phrases break on any silence ≥ 0.5s OR speaker change. This is the artifact the editor sub-agent reads to pick cuts — it gives word-boundary precision from text alone at 1/10 the tokens of raw JSON.

Example line:
```
## C0103  (duration: 43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
```

## Editor sub-agent brief (for multi-take selection)

When the task is "pick the best take of each beat across many clips," spawn a dedicated sub-agent with a brief shaped like this. The structure is load-bearing; the pitch-shape example is not.

```
You are editing a <type> video. Pick the best take of each beat and
assemble them chronologically by beat, not by source clip order.

INPUTS:
  - takes_packed.md (time-annotated phrase-level transcripts of all takes)
  - Product/narrative context: <2 sentences from the user>
  - Speaker(s): <name, role, delivery style note>
  - Expected structure: <pick an archetype or invent one>
  - Verbal slips to avoid: <list from the pre-scan pass>
  - Target runtime: <seconds>

Common structural archetypes (pick, adapt, or invent):
  - Tech launch / demo:   HOOK → PROBLEM → SOLUTION → BENEFIT → EXAMPLE → CTA
  - Tutorial:             INTRO → SETUP → STEPS → GOTCHAS → RECAP
  - Interview:            (QUESTION → ANSWER → FOLLOWUP) repeat
  - Travel / event:       ARRIVAL → HIGHLIGHTS → QUIET MOMENTS → DEPARTURE
  - Documentary:          THESIS → EVIDENCE → COUNTERPOINT → CONCLUSION
  - Music / performance:  INTRO → VERSE → CHORUS → BRIDGE → OUTRO
  - Or invent your own.

RULES:
  - Start/end times must fall on word boundaries from the transcript.
  - Pad cut boundaries (working window 30–200ms).
  - Prefer silences ≥ 400ms as cut targets.
  - Unavoidable slips are kept if no better take exists. Note them in "reason".
  - If over budget, revise: drop a beat or trim tails. Report total and self-correct.

OUTPUT (JSON array, no prose):
  [{"source": "C0103", "start": 2.42, "end": 6.85, "beat": "HOOK",
    "quote": "...", "reason": "..."}, ...]

Return the final EDL and a one-line total runtime check.
```

## Color grade (when requested)

Your job is to **reason about the image**, not apply a preset. Look at a frame (via `timeline_view`), decide what's wrong, adjust one thing, look again.

Mental model is ASC CDL. Per channel: `out = (in * slope + offset) ** power`, then global saturation. `slope` → highlights, `offset` → shadows, `power` → midtones.

**Example filter chains** (`grade.py` has `--list-presets`; use them as starting points or mix your own):

- **`warm_cinematic`** — retro/technical, subtle teal/orange split, desaturated. Shipped in a real launch video. Safe for talking heads.
- **`neutral_punch`** — minimal corrective: contrast bump + gentle S-curve. No hue shifts.
- **`none`** — straight copy. Default when the user hasn't asked.

For anything else — portraiture, nature, product, music video, documentary — invent your own chain. `grade.py --filter '<raw ffmpeg>'` accepts any filter string.

Hard rules: apply **per-segment during extraction** (not post-concat, which re-encodes twice). Never go aggressive without testing skin tones.

## Subtitles (when requested)

Subtitles have three dimensions worth reasoning about: **chunking** (1/2/3/sentence per line), **case** (UPPER/Title/Natural), and **placement** (margin from bottom). The right combo depends on content.

**Worked styles** — pick, adapt, or invent:

**`bold-overlay`** — short-form tech launch, fast-paced social. 2-word chunks, UPPERCASE, break on punctuation, Helvetica 18 Bold, white-on-outline, `MarginV=35`. `render.py` ships with this as `SUB_FORCE_STYLE`.

**`natural-sentence`** (if you invent this mode) — narrative, documentary, education. 4–7 word chunks, sentence case, break on natural pauses, `MarginV=60–80`, larger font for readability, slightly wider max-width. No shipped force_style — design one if you need it.

Invent a third style if neither fits. Hard rules: subtitles LAST (Rule 1), output-timeline offsets (Rule 5).

## Animations (when requested)

Animations match the content and the brand. **Get the palette, font, and visual language from the conversation** — never assume a default. If the user hasn't told you, propose a palette in the strategy phase and wait for confirmation before building anything.

**Tool options:**

- **PIL + PNG sequence + ffmpeg** — simple overlay cards: counters, typewriter text, single bar reveals, progressive draws. Fast to iterate, any aesthetic you want.
- **Manim** — formal diagrams, state machines, equation derivations, graph morphs. Read `skills/manim-video/SKILL.md` and its references for depth.
- **Remotion** — typography-heavy, brand-aligned, web-adjacent layouts. React/CSS-based.

None is mandatory. Invent hybrids if useful.

**Duration rules of thumb, context-dependent:**

- **Sync-to-narration explanations.** A viewer needs to parse the content at 1×. Rough floor 3s, typical 5–7s for simple cards, 8–14s for complex diagrams.
- **Beat-synced accents** (music video, fast montage). 0.5–2s is fine — they're visual accents, not information.
- **Hold the final frame ≥ 1s** before the cut (universal).
- **Over voiceover:** total duration ≥ `narration_length + 1s` (universal).
- **Never parallel-reveal independent elements** — the eye can't track two new things at once.

**Animation payoff timing (rule for sync-to-narration):** get the payoff word's timestamp. Start the overlay `reveal_duration` seconds earlier so the landing frame coincides with the spoken payoff word.

**Easing** (universal — never `linear`, it looks robotic):

```python
def ease_out_cubic(t):    return 1 - (1 - t) ** 3
def ease_in_out_cubic(t):
    if t < 0.5: return 4 * t ** 3
    return 1 - (-2 * t + 2) ** 3 / 2
```

**Parallel sub-agent brief** — each animation is one sub-agent spawned via the `Agent` tool. Each prompt is self-contained (sub-agents have no parent context). Include:

1. One-sentence goal: *"Build ONE animation: [spec]. Nothing else."*
2. Absolute output path (`<edit>/animations/slot_<id>/render.mp4`)
3. Exact technical spec: resolution, fps, codec, pix_fmt, CRF, duration
4. Style palette as concrete values (RGB tuples, hex, or reference to a design system)
5. Font path with index
6. Frame-by-frame timeline (what happens when, with easing)
7. Anti-list ("no chrome, no extras, no titles unless specified")
8. Code pattern reference (copy helpers inline, don't import across slots)
9. Deliverable checklist (script, render, verify duration via ffprobe, report)
10. **"Do not ask questions. If anything is ambiguous, pick the most obvious interpretation and proceed."**

## Output spec

Match the source unless the user asked for something specific. Common targets: `1920×1080@24` cinematic, `1920×1080@30` screen content, `1080×1920@30` vertical social, `3840×2160@24` 4K cinema, `1080×1080@30` square. `render.py` defaults the scale to 1080p from any source.

## EDL format

```json
{
  "version": 1,
  "sources": {"C0103": "/abs/path/C0103.MP4", "C0108": "/abs/path/C0108.MP4"},
  "ranges": [
    {"source": "C0103", "start": 2.42, "end": 6.85,
     "beat": "HOOK", "quote": "...", "reason": "Cleanest delivery, stops before slip at 38.46."},
    {"source": "C0108", "start": 14.30, "end": 28.90,
     "beat": "SOLUTION", "quote": "...", "reason": "Only take without the false start."}
  ],
  "grade": "warm_cinematic",
  "overlays": [
    {"file": "edit/animations/slot_1/render.mp4", "start_in_output": 0.0, "duration": 5.0}
  ],
  "subtitles": "edit/master.srt",
  "total_duration_s": 87.4
}
```

## Memory — `project.md`

Append one section per session at `<edit>/project.md`:

```markdown
## Session N — YYYY-MM-DD

**Strategy:** one paragraph describing the approach
**Decisions:** take choices, cuts, grades, animations + why
**Reasoning log:** one-line rationale for non-obvious decisions
**Outstanding:** deferred items
```

On startup, read `project.md` if it exists and summarize the last session in one sentence before asking whether to continue.

## Failure Modes and Prevention

These are the ways the skill actually breaks in practice. Each has a concrete prevention step.

| Failure | Symptom | Prevention |
|---------|---------|------------|
| **Stale transcript cache** | Cuts don't match audio | Compare source file mtime vs transcript mtime. Re-transcribe if source is newer. |
| **EDL source path mismatch** | `render.py` exits with "file not found" | Always use absolute paths in `sources`. Run `render.py --dry-run` before full render. |
| **Word boundary violation** | Audible word fragment at cut | Snap every `start`/`end` to the nearest word boundary from Scribe JSON. |
| **Missing 30ms audio fade** | Pop/click at segment join | `render.py` applies fades automatically; verify via `self_eval.py` loudness check. |
| **Subtitle under overlay** | Captions invisible during overlay window | Hard Rule 1. `render.py` applies subtitles LAST. Verify with `timeline_view` spot-check. |
| **Animation PTS not shifted** | Overlay shows wrong frames | Hard Rule 4. `render.py` applies `setpts=PTS-STARTPTS+T/TB`. |
| **Self-eval infinite loop** | Agent loops without progress | Cap at 3 passes. After 3, flag remaining issues to user. |
| **Context window exhaustion** | Long transcript overwhelms agent context | Use `pack_transcripts.py` output (10x token reduction). Never feed raw Scribe JSON to the LLM. |
| **ffmpeg silent failure** | Render completes but output is corrupt | Always run `self_eval.py` on output. Check for zero-duration or missing streams. |
| **Parallel animation race** | Slots overwrite each other | Each animation gets its own `slot_<id>/` directory. Never share output paths between sub-agents. |

## Acceptance Criteria (Definition of Done)

A video edit session is complete when ALL of the following are true:

1. `self_eval.py` reports ALL PASS on the final render (codec, resolution, loudness, duration match)
2. Visual spot-check at cut boundaries shows no discontinuities, pops, or hidden subtitles
3. Total duration is within 2% of the EDL's `total_duration_s` (or user-specified target)
4. `project.md` has been updated with the session's strategy, decisions, and reasoning
5. User has explicitly confirmed the output

## Anti-patterns

Things that consistently fail regardless of style:

- **Hierarchical pre-computed codec formats** with USABILITY / tone tags / shot layers. Over-engineering. Derive from the transcript at decision time.
- **Hand-tuned moment-scoring functions.** The LLM picks better than any heuristic you'll write.
- **Whisper SRT / phrase-level output.** Loses sub-second gap data. Always word-level verbatim.
- **Running Whisper locally on CPU.** Slow and it normalizes fillers. Use hosted Scribe.
- **Burning subtitles into base before compositing overlays.** Overlays hide them. (Hard Rule 1.)
- **Single-pass filtergraph when you have overlays.** Double re-encodes. Use per-segment extract → concat.
- **Linear animation easing.** Looks robotic. Always cubic.
- **Hard audio cuts at segment boundaries.** Audible pops. (Hard Rule 3.)
- **Typing text centered on the partial string.** Text slides left as it grows.
- **Sequential sub-agents for multiple animations.** Always parallel.
- **Editing before confirming the strategy.** Never.
- **Re-transcribing cached sources.** Immutable outputs of immutable inputs.
- **Assuming what kind of video it is.** Look first, ask second, edit last.

---

## Changelog

### 1.5.0 — 2026-04-23

- **render.py**: new `ffrun` helper wrapping all FFmpeg subprocess calls — captures and surfaces the last 30 lines of `stderr` on failure for immediate diagnostics; replaced all 5 `subprocess.run` invocations. Added output-file existence guard that aborts with a clear message when the final render is missing or empty.
- **grade.py**: `_sample_frame_stats` no longer discards FFmpeg `stderr` — captures output via `subprocess.PIPE` and prints the last 20 lines on failure for debuggability.
- **pipeline.py**: `--build-subtitles` / `--no-subtitles` refactored into a `mutually_exclusive_group` to prevent conflicting flags. Added `--raw-dir` passthrough. Silent stage-skip messages upgraded to `sys.stderr` warnings.
- **self_eval.py**: zero-byte file pre-check before `ffprobe`; robust `try-except` parsing for `duration` and `size` fields; explicit fail on non-positive `actual_duration`.
- **transcribe.py**: API key loading order corrected — `os.environ` checked before `.env` file fallback for consistent behavior in CI/container environments.
- **timeline_view.py**: `time_to_x` closure lifted out of the inner `silences` loop to avoid per-iteration redefinition overhead.
- **Full suite**: all 9 helper scripts pass `py_compile` syntax verification.

### 1.4.0 — 2026-04-23

- **NEW `self_eval.py`**: post-render quality gate — ffprobe verification (codec, resolution, fps), loudness measurement (LUFS + true peak), EDL duration comparison, structured PASS/FAIL report with `--json` output.
- **NEW `pipeline.py`**: full workflow orchestrator — chains healthcheck → transcribe → pack → render → self_eval with per-stage timing, `--stage` single-stage mode, `--skip-healthcheck`, `--no-eval`, and quality mode passthrough.
- **timeline_view.py**: fully implemented `--edl` mode — multi-segment composite with per-range filmstrip, waveform, silence highlights, segment labels, timing info, and color-coded boundary markers.
- **healthcheck.py**: improved `.env` search — now checks skill root directory, CWD, and `~/.env` before reporting ELEVENLABS_API_KEY failure.
- **SKILL.md**: version 1.4.0; documented `self_eval.py`, `pipeline.py`, updated `timeline_view.py` `--edl` and `healthcheck.py` descriptions.

### 1.3.0 — 2026-04-23

- **render.py**: EDL validation (`validate_edl`), `--dry-run` segment plan preview, defensive empty-segment guard, `--no-subtitles` flag, correct `preview`/`draft` quality propagation to `build_final_composite` and `apply_loudnorm_two_pass`.
- **grade.py**: `--analyze`, `--list-presets`, `--print-preset` flags; `RuntimeError` on ffmpeg failure.
- **pack_transcripts.py**: `FileNotFoundError` / malformed JSON handling; `-o` output path override.
- **timeline_view.py**: `--edl` mode prints clear "not implemented" guidance; duplicate `import wave` removed.
- **transcribe_batch.py**: `sys.path` fix for cross-helper imports.
- **pyproject.toml**: removed unused `librosa`/`matplotlib`; version synced to 1.3.0.
- **SKILL.md**: documentation aligned with all helper flag changes above.

### 1.2.0

- Initial public skill structure with helpers, EDL pipeline, and examples.
