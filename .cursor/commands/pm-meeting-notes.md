---
description: Summarize meeting transcripts into structured notes with decisions and action items
argument-hint: "<meeting transcript or notes>"
---

# PM Meeting Notes

Summarize meeting transcripts or rough notes into structured meeting notes. Extract attendees, topics, decisions, action items (with owners), open questions, and key quotes. Uses pm-execution skill, summarize-meeting sub-skill.

## Usage
```
/pm-meeting-notes Summarize this transcript
/pm-meeting-notes 이 회의록 요약해줘
/pm-meeting-notes Extract action items from these notes
/pm-meeting-notes 회의 내용에서 액션 아이템 추출해줘
```

## Workflow

### Step 1: Ingest Transcript or Notes
- Accept raw transcript, bullet notes, or voice-to-text output
- If multiple sources, merge in chronological order

### Step 2: Extract Core Elements
- **Attendees**: List participants; note who spoke most / was silent
- **Topics**: Main themes discussed, in order
- **Decisions**: Explicit decisions made (with rationale if stated)
- **Action items**: Task + owner + due date (infer if not stated)
- **Open questions**: Unresolved items for follow-up
- **Key quotes**: Memorable or decision-critical quotes

### Step 3: Structure Output
- Use clear headings and bullet lists
- Action items in table or checklist format: `[ ] Task — Owner — Due`
- Call out blockers or dependencies explicitly

### Step 4: Add Metadata
- Meeting title, date, duration (if inferrable)
- Suggested next meeting topic or agenda items

## Notes
- For long transcripts, summarize by section first, then synthesize
- If owner unclear, mark as "TBD" and suggest logical owner based on context
- Avoid editorializing — stick to what was said, not interpretation unless tagged as "Inference"
