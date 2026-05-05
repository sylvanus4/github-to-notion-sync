# Prompt Library

Replace bracketed placeholders before use.

---

## 2x2 Character Identity Grid

```text
A 2x2 grid of 4 different poses of the same cute anime couple (boy and girl) in casual travel outfits. Top-left: front view standing together smiling. Top-right: side view walking hand in hand. Bottom-left: back view looking at scenery. Bottom-right: sitting together at a cafe. Consistent character design: [BOY_DESCRIPTION], [GIRL_DESCRIPTION]. Bright warm colors, illustration style. White background separating each quadrant clearly.
```

**Parameters**:
- Model: `dall-e-3`
- Size: `1024x1024`
- Quality: `hd`

**Placeholder Examples**:
- `[BOY_DESCRIPTION]`: "boy has short dark hair, navy jacket, light jeans"
- `[GIRL_DESCRIPTION]`: "girl has shoulder-length brown hair, beige cardigan, white skirt"

---

## Travel Scene Image

```text
A cute anime couple ([BOY_DESCRIPTION]; [GIRL_DESCRIPTION]) [SCENE_ACTION] in [LOCATION_DESCRIPTION]. [LIGHTING_AND_MOOD]. Illustration style, 16:9 cinematic composition.
```

**Parameters**:
- Model: `dall-e-3`
- Size: `1792x1024`
- Quality: `hd`

**Placeholder Examples**:

| Scene | SCENE_ACTION | LOCATION_DESCRIPTION | LIGHTING_AND_MOOD |
|-------|-------------|---------------------|-------------------|
| Street | walking through a vibrant street | Tokyo with cherry blossoms, neon signs, and traditional lanterns | Warm sunset lighting |
| Cafe | sitting across from each other sharing matcha | a cozy Japanese cafe with wooden interior | Warm interior lighting, soft bokeh background |
| Temple | standing in front of a beautiful temple | a Japanese temple with red torii gates | Autumn leaves falling, golden hour |
| Beach | walking on a serene beach at sunset | a Japanese coastline with gentle waves | Orange and pink sky reflecting on water |
| Night | looking at city lights from a rooftop | an observation deck overlooking a sparkling city | Night sky with stars, romantic atmosphere |
| Market | browsing colorful stalls | a traditional night market with lanterns and steam | Warm golden lamp light, lively atmosphere |

---

## Music Prompt (for Suno/Udio)

If using an external music generation service, provide this prompt:

```text
Create a gentle, warm lo-fi instrumental track for a couple's travel vlog.

Style: Lo-fi hip hop meets Japanese city pop
Mood: Nostalgic, warm, romantic, dreamy
Tempo: 75-85 BPM
Duration: [TOTAL_DURATION] seconds
Instruments: Soft piano, muted guitar, vinyl crackle, light percussion, ambient pads
Key: A minor or C major

No vocals. No sudden changes. Smooth transitions throughout.
Fade in over 2 seconds, fade out over 3 seconds.
```

---

## FFmpeg Command Reference

### Ken Burns Effect (Image to Video)

```bash
ffmpeg -y -loop 1 -i [INPUT_IMAGE] \
  -vf "zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=[FRAMES]:s=1920x1080:fps=30" \
  -t [DURATION] -c:v libx264 -pix_fmt yuv420p [OUTPUT_CLIP]
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| `zoom+0.0015` | Zoom speed | Increase for faster zoom |
| `d=[FRAMES]` | Duration in frames | 150 = 5s at 30fps |
| `s=1920x1080` | Output resolution | Match across all clips |
| `-t [DURATION]` | Duration in seconds | Must match `d/fps` |

### Zoom Variations

| Effect | zoompan expression |
|--------|--------------------|
| Center zoom-in | `z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'` |
| Left-to-right pan | `z='1.2':x='if(eq(on,1),0,x+2)':y='ih/2-(ih/zoom/2)'` |
| Top-down reveal | `z='1.3':x='iw/2-(iw/zoom/2)':y='if(eq(on,1),0,y+1)'` |
| Zoom-out (wide) | `z='if(eq(on,1),1.5,max(zoom-0.001,1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'` |

### Video Concatenation with Crossfade

For N clips of D seconds each, with F seconds fade:

```bash
# Offset formula: offset_n = n * D - n * F
# Example: 5 clips, 5s each, 0.5s fade
ffmpeg -y -i clip_01.mp4 -i clip_02.mp4 -i clip_03.mp4 -i clip_04.mp4 -i clip_05.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5[v01];\
    [v01][2:v]xfade=transition=fade:duration=0.5:offset=9.0[v012];\
    [v012][3:v]xfade=transition=fade:duration=0.5:offset=13.5[v0123];\
    [v0123][4:v]xfade=transition=fade:duration=0.5:offset=18.0[vout]" \
  -map "[vout]" -c:v libx264 -pix_fmt yuv420p vlog_no_music.mp4
```

### Synthetic Background Music (A-minor chord)

```bash
ffmpeg -y \
  -f lavfi -i "sine=frequency=220:duration=[TOTAL]" \
  -f lavfi -i "sine=frequency=277:duration=[TOTAL]" \
  -f lavfi -i "sine=frequency=330:duration=[TOTAL]" \
  -filter_complex "\
    [0:a]volume=0.15[a0];\
    [1:a]volume=0.12[a1];\
    [2:a]volume=0.10[a2];\
    [a0][a1][a2]amix=inputs=3:duration=first[mixed];\
    [mixed]afade=t=in:ss=0:d=2,afade=t=out:st=[FADE_START]:d=2,lowpass=f=800[out]" \
  -map "[out]" -c:a aac -b:a 128k bgm_ambient.m4a
```

- `[TOTAL]` = total video duration in seconds
- `[FADE_START]` = `[TOTAL] - 2`

### Final Assembly (Video + BGM)

```bash
ffmpeg -y -i vlog_no_music.mp4 -i bgm_ambient.m4a \
  -filter_complex "[1:a]volume=0.6[bgm];[bgm]apad[bgmpad]" \
  -map 0:v -map "[bgmpad]" \
  -c:v copy -c:a aac -b:a 128k -shortest \
  final_vlog.mp4
```
