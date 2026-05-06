# AI Portrait Prompt Builder

Build structured AI portrait prompts using a 9-module photography direction framework.
Transforms photographic intent (lens language, lighting design, depth of field, color grading)
into precise, production-ready prompts for any image generation model (Flux, SDXL, Midjourney, etc.).

---

## Triggers

Use when the user asks to:
- "인물 사진 프롬프트 만들어줘", "portrait prompt", "AI 인물 생성"
- "ai-portrait-prompt", "촬영 방안", "인물 프롬프트"
- "프로필 사진 만들어줘", "매거진 인물", "시네마틱 인물"
- "portrait shot plan", "character photo prompt"
- "인물 이미지 생성", "AI 초상화", "프롬프트 설계"
- Any request to generate a portrait/character image with specific photographic intent

Do NOT use for:
- Landscape or product photography prompts (handle directly or use muapi-cinema for video)
- Logo or graphic design (use canvas-design)
- Video generation prompts (use pika-text-to-video or muapi-cinema)
- General image generation without portrait/character focus (use muapi-image-studio)

---

## Core Principle

> 효과적인 인물 프롬프트의 핵심은 스타일 단어의 수가 아니라, **촬영 판단이 명확한지 여부**에 있다.

A portrait prompt is a simplified shooting plan. It must communicate:
- What this photo is FOR (purpose)
- WHO the subject is and what FEELING they convey
- Camera distance and perspective (lens language)
- Where light comes from and its quality
- How much background information to retain
- Color direction
- Where realism details should concentrate

---

## Workflow

### Step 1: Determine Purpose (Module 1)

Ask or infer the image's intended use. This anchors ALL subsequent decisions.

| Purpose | Key Requirements |
|---------|-----------------|
| Social media profile | Face clear, gaze stable, clean background |
| Professional headshot | Trust, naturalness, professionalism, approachability |
| Magazine editorial | Composition, negative space, atmosphere, overall mood |
| Commercial advertising | Clean lighting, stable skin, strong visual control |
| Lifestyle portrait | Natural, relaxed, feels shot in a real scene |
| B&W documentary | Emotion, texture, subject state, presence |
| Cinematic night | Color, shadows, atmosphere, mood |

### Step 2: Define Subject & Mood (Module 2)

Never write just "a woman." Answer two questions:
1. **Who is this person?** (identity/role)
2. **What feeling do they give?** (mood/atmosphere)

Then specify: expression, skin texture preference, and any identity-preserving details.

### Step 3: Choose Lens Language (Module 3)

| Focal Length | Feel |
|---|---|
| 24mm | Environmental, strong perspective distortion |
| 35mm | Street/documentary distance, story feel |
| 50mm | Natural, balanced, everyday portraits |
| 85mm | Classic portrait, stable face proportions, clean BG |
| 105mm | Beauty/commercial close-up, stronger compression |
| 135mm | Restrained, detached, pronounced BG compression |

Write as: `85mm portrait lens look, natural facial proportions, clean background separation`

### Step 4: Set Composition & Angle (Module 4)

Composition options: face close-up, bust-up, half-body, three-quarter body, full-body, cover composition

Angle options: eye level, slightly high angle, slightly low angle, frontal gaze, 45-degree side, candid offset

### Step 5: Set Depth of Field (Module 5)

| Aperture | Effect |
|---|---|
| f/1.4 | Dreamy, emotional, strong bokeh (risks looking fake) |
| f/1.8 | Strong atmosphere, good for night/emotional portraits |
| f/2 | Subject stands out, works for lifestyle and style |
| f/2.8 | Stable portrait, face sharp, background moderately soft |
| f/4 | More environmental info retained (clothing, props, scene) |
| Deep DOF | Documentary, environmental, street scenes |

### Step 6: Design Lighting (Module 6)

| Lighting | Best For |
|---|---|
| Soft window light | Natural, everyday, comfortable skin |
| Large diffused window | Softbox feel, headshots |
| Overcast soft light | Urban, low contrast, stable |
| Golden hour backlight | Warm, soft, outdoor mood |
| Clamshell lighting | Beauty, commercial, clear catchlights |
| Hard direct light | Fashion, dramatic, intense |
| Neon + tungsten mixed | Night, cinematic, urban |
| Available light | Documentary, presence, minimal control |

Always specify: direction, quality, and effect on face.

### Step 7: Choose Color/Style Anchor (Module 7)

Pick ONE per prompt:

| Anchor | Direction |
|---|---|
| Kodak Portra 400 | Soft skin tones, lifestyle, natural film feel |
| Kodak Gold 200 | Warm, sunny, light retro |
| Fujifilm Classic Chrome | Low saturation, urban, restrained, editorial |
| Fujifilm Eterna | Soft, narrative, cinematic |
| CineStill 800T | Night, neon, tungsten, subtle halation |
| Ilford HP5 | B&W documentary, grain, subject state |
| Neutral editorial tone | Clean, neutral, professional |
| Clean commercial tone | Advertising, beauty, clean skin tones |

### Step 8: Specify Realism Details (Module 8)

Target specific areas — never just write "realistic":

- Skin: `natural skin texture, subtle pores`
- Eyes: `realistic catchlights, focused gaze`
- Hair: `natural flyaway hairs`
- Fabric: `real fabric texture`
- Background: `optical bokeh, not artificial blur`
- Highlights: `natural highlight roll-off`
- Face: `slight facial asymmetry, realistic facial detail`
- Retouching: `not over-retouched, no plastic skin`

### Step 9: Add Negative Constraints (Module 9)

Standard negative set (always include):
```
no AI fake face, no plastic skin, no over-retouched skin, no westernized facial features,
no influencer look, no excessive bokeh, no unnatural catchlights, no distorted hands
```

Context-specific additions:
- Night scenes: `restrained neon glow, no excessive halation`
- Commercial: `natural expression, not stiff, not overly posed`

---

## Assembly Formula

```
A [purpose] portrait of [subject], with [mood], framed as [composition] from [camera angle],
using a [lens look] and [aperture feel], lit by [lighting setup], in [environment],
wearing [wardrobe], with [tone/style anchor], emphasizing [realism details],
avoiding [negative constraints].
```

Order: Purpose → Subject → How to shoot → Lighting & Color → Realism & Constraints

---

## Style Presets (Quick Select)

| # | Style | Recipe |
|---|-------|--------|
| 1 | B&W Documentary | 35/50mm, available light, Ilford HP5, natural texture, grain |
| 2 | Film Lifestyle | 50mm, f/2, window light, Portra 400, half-body, relaxed |
| 3 | Low-Sat Urban | 85mm, f/2, overcast, Classic Chrome, bust-up, quiet editorial |
| 4 | Professional Headshot | 85mm, f/2.8, soft window light, neutral editorial, half-body |
| 5 | Commercial Beauty | 105mm, f/2.8, clamshell, face close-up, clean commercial |
| 6 | Cinematic Night | 85mm, f/1.8, neon+tungsten, CineStill 800T, subtle halation |
| 7 | Japanese Soft | 50mm, f/2.8, soft daylight, warm tone, clean BG, gentle |
| 8 | High-Contrast Fashion | 35/85mm, hard light, strong shadow, fashion editorial |
| 9 | Founder Portrait | 85mm, f/2.8, window light, minimal workspace, professional |
| 10 | Outdoor Golden Hour | 50/85mm, golden hour backlight, warm, soft flare |

---

## Output Modes

### Mode A: Full Prompt (Default)
Generate a complete English prompt following the assembly formula. Include all 9 modules.

### Mode B: Fill-in-the-Blank (Interactive)
Ask the user to choose from each module sequentially, then assemble the final prompt.

### Mode C: Style Preset + Customization
User picks a preset number (1-10), then specifies customizations (subject, environment, wardrobe).

### Mode D: Korean Brief → English Prompt
User describes intent in Korean ("카페에서 자연스러운 분위기의 반신 인물 사진"), skill translates to structured English prompt.

---

## References

Read `references/portrait-modules.md` for:
- Full module option lists with Korean/English mappings
- Extended style presets with example prompts
- Common mistakes and fixes
- Model-specific tips (Flux vs SDXL vs Midjourney)

---

## Quality Checklist

Before outputting any prompt, verify:
- [ ] Purpose is explicit (not just "portrait")
- [ ] Subject has identity AND mood (not just "a woman")
- [ ] Exactly ONE lens focal length specified
- [ ] Aperture feel matches the intended DOF
- [ ] Lighting has direction + quality (not just "good lighting")
- [ ] Only ONE color/style anchor (no mixing film stocks)
- [ ] At least 2 realism detail targets specified
- [ ] Negative constraints included
- [ ] Total prompt length: 50-150 words (sweet spot for most models)
