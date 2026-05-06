# AI Portrait Prompt — 9-Module Reference

Complete option lists, style recipes, and example prompts for the ai-portrait-prompt skill.

---

## Module 1: Purpose (이미지 용도)

| Code | EN | KO | Key Visual Requirements |
|------|----|----|------------------------|
| P01 | Social media profile | 소셜 미디어 프로필 | Face clear, gaze stable, clean background |
| P02 | Professional headshot | 프로필 촬영 | Trust, naturalness, professionalism |
| P03 | Magazine editorial | 매거진 인물 | Composition, negative space, mood |
| P04 | Commercial advertising | 상업 광고 | Clean lighting, stable skin, control |
| P05 | Lifestyle portrait | 라이프스타일 인물 | Natural, relaxed, real-scene feel |
| P06 | B&W documentary | 흑백 다큐멘터리 | Emotion, texture, state, presence |
| P07 | Cinematic night | 야경 시네마틱 | Color, shadow, atmosphere |
| P08 | Fashion editorial | 패션 에디토리얼 | Styling, posing, bold choices |
| P09 | Album/book cover | 앨범/책 표지 | Negative space for text, strong focal |
| P10 | Dating profile | 소개팅/데이팅 프로필 | Approachable, attractive, authentic |

---

## Module 2: Subject & Mood (피사체와 분위기)

### Identity Options
young woman, young man, middle-aged professional, elderly person, teenager, child,
creative director, startup founder, designer, fitness creator, office worker,
street passerby, musician, academic, doctor, chef, artist

### Mood Keywords
| EN | KO |
|----|----|
| natural and relaxed | 자연스럽고 편안한 |
| restrained and calm | 절제되고 차분한 |
| neat and professional | 단정하고 전문적인 |
| friendly and soft | 친근하고 부드러운 |
| elegant and detached | 고급스럽고 초연한 |
| steady and mature | 침착하고 성숙한 |
| confident and warm | 자신감 있고 따뜻한 |
| mysterious and intense | 신비롭고 강렬한 |
| playful and youthful | 활기차고 젊은 |

### Expression Options
peaceful direct gaze, slight smile, focused concentration, thoughtful introspection,
relaxed ease, determined resolve, gentle amusement, quiet confidence,
subtle melancholy, candid mid-action

### Skin Texture Direction
| Level | EN Prompt | Use Case |
|-------|-----------|----------|
| Natural | natural skin texture, visible pores | Documentary, lifestyle |
| Light retouch | lightly retouched, natural-looking | Headshots, social media |
| Commercial clean | smooth even skin, commercial beauty | Advertising, beauty |
| Documentary raw | raw skin detail, imperfections visible | Documentary, art |

---

## Module 3: Lens Language (렌즈 언어)

| Focal | Prompt Fragment | Best For |
|-------|----------------|----------|
| 24mm | 24mm wide-angle lens look, visible perspective distortion, environmental context | Environmental portraits, creative distortion |
| 35mm | 35mm lens look, natural documentary distance, scene included | Street, documentary, storytelling |
| 50mm | 50mm lens look, natural perspective, balanced framing | Everyday, lifestyle, natural portraits |
| 85mm | 85mm portrait lens look, natural facial proportions, clean background separation | Classic portraits, headshots |
| 105mm | 105mm lens look, tight framing, pronounced background compression | Beauty, commercial close-ups |
| 135mm | 135mm telephoto look, strong background compression, detached feel | Fashion, editorial, compressed BG |

---

## Module 4: Composition & Angle (구도와 앵글)

### Composition
| EN | KO | Info Level |
|----|----|-----------|
| extreme close-up (eyes/lips only) | 극단적 클로즈업 | Minimal — detail focus |
| face close-up | 얼굴 클로즈업 | Low — beauty, emotion |
| bust-up (shoulders up) | 가슴까지 | Medium-low — profile, style |
| half-body (waist up) | 반신 | Medium — most versatile |
| three-quarter body | 3/4 전신 | Medium-high — fashion, lookbook |
| full-body | 전신 | High — styling, environment |
| cover composition (with text space) | 표지 구도 | Design-aware — text placement |

### Angle
| EN | KO | Effect |
|----|----|--------|
| eye level | 아이 레벨 | Neutral, equal, stable |
| slightly high angle | 약간 하이 앵글 | Softer, approachable |
| slightly low angle | 약간 로우 앵글 | Powerful, fashionable |
| frontal gaze | 정면 직시 | Direct connection |
| 45-degree side | 45도 측면 | Classic portrait angle |
| candid offset angle | 캔디드 오프셋 | Documentary, spontaneous |
| over-shoulder | 어깨 너머 | Intimate, narrative |

---

## Module 5: Depth of Field (피사계 심도)

| Aperture | Prompt | Character | Risk |
|----------|--------|-----------|------|
| f/1.4 feel | f/1.4 feel, dreamy shallow depth of field, extreme bokeh | Dreamy, emotional | Can look fake |
| f/1.8 feel | f/1.8 feel, strong atmosphere, gentle subject isolation | Atmospheric, night | Slightly unnatural |
| f/2 feel | f/2 feel, moderate shallow depth of field, subject stands out | Versatile, balanced | Low risk |
| f/2.8 feel | f/2.8 feel, face sharp, background moderately soft | Most stable | Very safe |
| f/4 feel | f/4 feel, environment visible, moderate separation | More context | Less isolation |
| deep DOF | deep depth of field, everything in focus | Documentary, environmental | No isolation |

**Default recommendation**: `f/2.8 feel, moderate shallow depth of field, background still recognizable`

---

## Module 6: Lighting Design (조명 디자인)

| Type | EN Prompt | Direction Example |
|------|-----------|-------------------|
| Soft window | soft natural window light from the left side, gentle shadow falloff | Specify side |
| Large diffused | large diffused window light, even illumination, minimal shadows | Front or side |
| Overcast | overcast soft ambient light, low contrast, even skin tones | Omnidirectional |
| Golden hour | golden hour warm backlight, soft rim lighting, gentle flare | Behind subject |
| Clamshell | clamshell lighting, beauty dish above with fill below, clear catchlights | Above + below |
| Hard direct | hard direct sunlight, defined shadows, high contrast | Specify angle |
| Neon + tungsten | mixed neon and tungsten practical lights, color contrast on skin | Environmental |
| Available | available ambient light only, uncontrolled natural illumination | As-is |
| Rembrandt | Rembrandt lighting, triangle shadow on cheek, dramatic but natural | 45° above + side |
| Split | split lighting, half face illuminated, dramatic division | Direct side |

### Lighting Modifier Keywords
- Shadow quality: gentle shadow falloff / harsh shadow edges / minimal shadows
- Catchlights: natural catchlights in the eyes / clear round catchlights / subtle catchlights
- Wrap: light wrapping around face / directional with clear falloff
- Contrast: low contrast even illumination / high contrast dramatic / medium natural contrast

---

## Module 7: Color & Style Anchors (색조와 스타일 앵커)

| Anchor | Prompt Fragment | Character |
|--------|----------------|-----------|
| Kodak Portra 400 | Kodak Portra 400 inspired color palette, soft warm skin tones | Soft, natural, film lifestyle |
| Kodak Gold 200 | Kodak Gold 200 warm tone, slight golden cast | Sunny, warm, nostalgic |
| Fujifilm Classic Chrome | Fujifilm Classic Chrome inspired muted palette, desaturated | Urban, editorial, restrained |
| Fujifilm Eterna | Fujifilm Eterna inspired soft cinematic tone | Narrative, soft, cinematic |
| CineStill 800T | CineStill 800T inspired night tone, warm tungsten shift | Night, neon, cinematic |
| Ilford HP5 | Ilford HP5 inspired monochrome, subtle grain | B&W documentary, textural |
| Neutral editorial | neutral editorial color tone, clean balanced grading | Professional, magazine |
| Clean commercial | clean commercial color grading, perfect skin tones | Advertising, beauty |
| Kodachrome 64 | Kodachrome 64 inspired saturated colors, strong contrast | Vivid, punchy, retro |
| Agfa Vista 200 | warm everyday color, slightly green shadows | Casual, warm, everyday |

**Rule**: ONE anchor per prompt. Never combine (e.g., no "Portra 400 + CineStill 800T").

---

## Module 8: Realism Details (사실감 디테일)

| Target | Prompt Fragment | Why It Matters |
|--------|----------------|----------------|
| Skin | natural skin texture, subtle pores, micro-texture visible | Prevents plastic look |
| Eyes | realistic catchlights, focused iris detail, natural eye moisture | Prevents dead eyes |
| Hair | natural flyaway hairs, realistic hair shine, individual strands | Prevents helmet hair |
| Fabric | real fabric texture, visible weave, natural draping | Prevents painted-on clothes |
| Background bokeh | optical bokeh circles, not artificial gaussian blur | Prevents fake blur |
| Highlights | natural highlight roll-off, specular highlights on skin | Prevents flat lighting |
| Facial structure | slight facial asymmetry, realistic bone structure | Prevents uncanny perfection |
| Hands | natural hand positioning, correct finger count | Prevents distortion |
| Overall | not over-retouched, photography-level realism | Prevents AI overshoot |

Pick 2-4 per prompt (don't overload).

---

## Module 9: Negative Constraints (제한 항목)

### Universal (always include)
```
no AI fake face, no plastic skin, no over-retouched skin, no influencer look,
no excessive bokeh, no unnatural catchlights, no distorted hands
```

### Context-Specific Additions
| Context | Add |
|---------|-----|
| Asian subjects | no westernized facial features |
| Night scenes | restrained neon glow, no excessive halation |
| Commercial | natural expression, not stiff, not overly posed |
| Documentary | no beauty filter, no artificial studio look |
| Fashion | no generic model pose |
| Close-up | no skin smoothing filter, no porcelain doll effect |

---

## Complete Example Prompts

### 1. Professional Founder Portrait
```
A professional founder portrait of a young Asian woman, calm and confident expression,
half-body framing, eye-level camera angle, 85mm portrait lens look, f/2.8 feel,
soft natural window light from the left side, minimal workspace background,
navy shirt with black inner layer, neutral editorial tone, natural skin texture,
subtle pores, realistic catchlights, real fabric texture,
no AI fake face, no plastic skin, no over-retouched skin, no westernized facial features.
```

### 2. Film Lifestyle in Café
```
A soft lifestyle portrait of a young Asian woman in a café, relaxed and natural expression,
half-body composition, slightly high angle, 50mm lens look, f/2 feel,
large window natural light, Kodak Portra 400 inspired color tone,
gentle skin tones, subtle film grain, realistic fabric texture, natural catchlights,
elegant everyday atmosphere, no over-retouching, no plastic skin, no artificial blur.
```

### 3. B&W Documentary
```
A black-and-white documentary-style portrait of a young woman, natural and observant expression,
half-body framing, eye-level angle, 50mm lens look, available light,
Ilford HP5 inspired monochrome tone, subtle grain, realistic skin texture,
slight facial asymmetry, candid atmosphere,
no over-retouched skin, no perfect beauty filter, no artificial studio look.
```

### 4. Urban Editorial
```
An editorial urban portrait of a young woman, calm and self-possessed expression,
bust-up framing, eye-level camera angle, 85mm portrait lens look, f/2 feel,
overcast soft light, organized city background with gentle optical bokeh,
Fujifilm Classic Chrome inspired muted color palette, natural skin texture,
quiet magazine atmosphere, no excessive bokeh, no plastic skin, no influencer look.
```

### 5. Cinematic Night
```
A cinematic night portrait of a young woman, introspective expression,
half-body composition, diagonal 45-degree camera angle, 85mm lens look, f/1.8 feel,
mixed neon and tungsten practical lights, CineStill 800T inspired night tone,
subtle halation, restrained neon glow, realistic skin under mixed lighting,
atmospheric but believable, no excessive neon, no plastic skin, no unnatural catchlights.
```

### 6. Japanese Soft Light
```
A gentle soft-light portrait of a young Asian woman, peaceful slight smile,
half-body framing, slightly high angle, 50mm lens look, f/2.8 feel,
soft diffused daylight, clean minimal background, white blouse,
light warm tone with soft pastel cast, natural skin texture, gentle catchlights,
airy and transparent atmosphere, no heavy retouching, no artificial blur, no plastic skin.
```

### 7. Fashion Editorial
```
A high-fashion editorial portrait of a young woman, fierce determined expression,
three-quarter body framing, slightly low angle, 85mm lens look, f/2 feel,
hard direct light from upper left, deep defined shadows, black structured blazer,
neutral desaturated editorial tone, real fabric texture, natural skin texture,
bold magazine atmosphere, no generic model pose, no plastic skin, no excessive bokeh.
```

### 8. Outdoor Golden Hour
```
A warm golden hour portrait of a young woman, gentle natural smile,
half-body composition, eye-level angle, 85mm lens look, f/2 feel,
golden hour backlight with soft rim lighting, subtle warm flare,
outdoor park setting with soft green bokeh, linen dress,
Kodak Portra 400 warm tone, natural skin glow, flyaway hairs catching light,
no over-retouching, no artificial blur, no plastic skin.
```

---

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Writing "realistic" without targets | Specify WHERE realism applies (skin, eyes, bokeh) |
| Multiple film stocks in one prompt | Pick ONE color anchor |
| "Beautiful lighting" (vague) | Specify source, direction, quality |
| No composition specified | Always state framing + angle |
| Negative prompt too short | Include the full universal set |
| Prompt too long (200+ words) | Trim to 50-150 words — quality over quantity |
| Subject is just "a woman" | Add identity + mood + expression |
| No focal length | Always specify lens look |

---

## Model-Specific Notes

### Flux (Pro/Dev)
- Responds well to photographic terminology
- Natural language descriptions work better than keyword stacking
- Supports long prompts (up to 256 tokens effective)

### SDXL / Stable Diffusion
- Benefits from more keyword-style prompts
- Weight syntax available: `(natural skin texture:1.2)`
- Negative prompt field available — move constraints there

### Midjourney
- Prefers concise, evocative descriptions
- `--style raw` for photorealistic results
- `--ar 3:4` or `--ar 2:3` for portrait aspect ratios

### Google Imagen / Gemini
- Prefers natural language over keywords
- Safety filters may block some content — keep descriptions professional
- Excels at lighting descriptions
