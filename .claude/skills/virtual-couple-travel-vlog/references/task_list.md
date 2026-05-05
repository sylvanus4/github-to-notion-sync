# Task List: Virtual Couple Travel Vlog (v2.0)

7-step pipeline using DALL-E 3 + FFmpeg. No external video API required.

---

## Step 1: Setup & Character Design

**Goal**: Define couple identity and destination, create output directory.

**Actions**:
1. Confirm couple description (appearance, outfit, art style)
2. Confirm travel destination and 4-6 scene concepts
3. Create output directory structure:
   ```
   outputs/vlog-{destination}/{date}/
   ├── characters/
   ├── scenes/
   ├── clips/
   └── audio/
   ```
4. Load `OPENAI_API_KEY` from `.env`

**Acceptance Criteria**:
- [ ] Couple description locked (hair, outfit, style keywords)
- [ ] 4-6 scene descriptions written
- [ ] Output directory exists
- [ ] API key verified

---

## Step 2: Character Grid Generation

**Goal**: Generate a 2x2 identity grid to establish visual consistency.

**Actions**:
1. Call DALL-E 3 with 2x2 grid prompt (see `prompts.md`)
2. Save as `character_grid.png` (1024x1024 HD)
3. Split into 4 quadrants using Pillow:
   - `characters/front.png`
   - `characters/side.png`
   - `characters/back.png`
   - `characters/cafe.png`

**Acceptance Criteria**:
- [ ] `character_grid.png` exists and is ~1024x1024
- [ ] 4 individual pose files in `characters/`
- [ ] Same couple appears consistently across all 4 poses

---

## Step 3: Scene Image Generation

**Goal**: Generate 4-6 travel scene images with the same couple.

**Actions**:
1. For each scene, call DALL-E 3 with landscape format (1792x1024)
2. Include character description in every prompt for consistency
3. Save as `scenes/scene_01_{name}.png`, `scene_02_{name}.png`, etc.
4. Add 1-second delay between API calls to respect rate limits

**Acceptance Criteria**:
- [ ] 4-6 scene images saved in `scenes/`
- [ ] Each image is 1792x1024 landscape
- [ ] Character appearance is reasonably consistent across scenes
- [ ] Total DALL-E 3 cost logged

---

## Step 4: Ken Burns Video Clips

**Goal**: Convert each static scene image into a 5-second video clip with zoom animation.

**Actions**:
1. For each scene image, run FFmpeg `zoompan` filter:
   ```bash
   ffmpeg -y -loop 1 -i scene.png \
     -vf "zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1920x1080:fps=30" \
     -t 5 -c:v libx264 -pix_fmt yuv420p clip.mp4
   ```
2. Save as `clips/clip_01.mp4`, `clip_02.mp4`, etc.

**Acceptance Criteria**:
- [ ] Each clip is exactly 5 seconds, 1920x1080, 30fps
- [ ] Smooth zoom-in effect visible
- [ ] No encoding errors (ffprobe validates)

---

## Step 5: Background Music

**Goal**: Generate or provide ambient background music matching the vlog duration.

**Actions**:
1. Calculate total video duration: `(N clips x 5s) - ((N-1) x 0.5s fade)`
2. Generate synthetic BGM using FFmpeg sine waves:
   ```bash
   ffmpeg -y -f lavfi -i "sine=frequency=220:duration=TOTAL" \
     -f lavfi -i "sine=frequency=277:duration=TOTAL" \
     -f lavfi -i "sine=frequency=330:duration=TOTAL" \
     -filter_complex "..." \
     bgm_ambient.m4a
   ```
3. OR: provide a `music_prompt.txt` for user to generate BGM on Suno/Udio

**Acceptance Criteria**:
- [ ] `bgm_ambient.m4a` OR user-provided BGM file exists
- [ ] Duration >= total video duration
- [ ] Audio plays cleanly (no clicks, pops)

---

## Step 6: Video Assembly

**Goal**: Concatenate all clips with transitions and mix in background music.

**Actions**:
1. Concatenate clips with crossfade transitions:
   ```bash
   ffmpeg -y -i clip_01.mp4 -i clip_02.mp4 ... \
     -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5..." \
     vlog_no_music.mp4
   ```
2. Mix BGM at 60% volume:
   ```bash
   ffmpeg -y -i vlog_no_music.mp4 -i bgm_ambient.m4a \
     -filter_complex "[1:a]volume=0.6[bgm];[bgm]apad[bgmpad]" \
     -map 0:v -map "[bgmpad]" -c:v copy -c:a aac -shortest \
     final_vlog.mp4
   ```

**Acceptance Criteria**:
- [ ] `vlog_no_music.mp4` plays with smooth transitions
- [ ] `final_vlog.mp4` has both video and audio tracks
- [ ] Total duration is correct
- [ ] File size is reasonable (< 50MB for 30s clip)

---

## Step 7: Verification & Delivery

**Goal**: Validate the final vlog and report results.

**Actions**:
1. Run `ffprobe final_vlog.mp4` to verify:
   - Video: H.264, 1920x1080, 30fps
   - Audio: AAC
   - Duration: matches expected length
2. Report file location and size
3. Log total cost (DALL-E 3 API calls)

**Acceptance Criteria**:
- [ ] `final_vlog.mp4` passes ffprobe validation
- [ ] User can open and play the video
- [ ] Cost report generated

---

## Cost Summary

| Step | API Calls | Estimated Cost |
|------|-----------|---------------|
| Step 2: Character Grid | 1 DALL-E 3 (1024x1024 HD) | $0.08 |
| Step 3: Scene Images | 5 DALL-E 3 (1792x1024 HD) | $0.60 |
| Steps 4-6: FFmpeg | Local processing | $0.00 |
| **Total** | **6 API calls** | **~$0.68** |
