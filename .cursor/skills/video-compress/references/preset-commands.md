# ffmpeg Preset Commands

## Setup

Extract base name and directory before running any preset:

```bash
DIR=$(dirname "<INPUT_FILE>")
BASENAME=$(basename "<INPUT_FILE>")
NAME="${BASENAME%.*}"
```

## Preset: h264-crf32 (default)

```bash
ffmpeg -y -i "<INPUT_FILE>" -vcodec libx264 -crf 32 -preset veryslow -acodec aac -b:a 96k "${DIR}/${NAME}_h264_crf32.mp4"
```

## Preset: h264-crf28

```bash
ffmpeg -y -i "<INPUT_FILE>" -vcodec libx264 -crf 28 -preset fast -acodec aac -b:a 128k "${DIR}/${NAME}_h264_crf28.mp4"
```

## Preset: 720p

```bash
ffmpeg -y -i "<INPUT_FILE>" -vf scale=1280:-1 -vcodec libx264 -crf 28 -preset fast -acodec aac -b:a 128k "${DIR}/${NAME}_720p.mp4"
```

## Preset: hevc

```bash
ffmpeg -y -i "<INPUT_FILE>" -vcodec libx265 -crf 28 -preset slow -acodec aac -b:a 128k "${DIR}/${NAME}_hevc.mp4"
```

## Preset: noaudio

```bash
ffmpeg -y -i "<INPUT_FILE>" -an -vcodec libx264 -crf 28 -preset fast "${DIR}/${NAME}_noaudio.mp4"
```

## Preset: all (parallel)

Run all five preset commands above in parallel using `&`, then `wait` for all to complete.

## Compression Report Format

### Single Preset

```
Compression Report
──────────────────────────────
Input:      {input filename}  ({original human-readable size})
Output:     {output filename} ({compressed human-readable size})
Preset:     {preset name}
Ratio:      {original / compressed}x
Reduction:  {percentage}%
──────────────────────────────
```

### All Presets Comparison

```
Compression Report (all presets)
──────────────────────────────────────────────────────
Preset        Output Size    Ratio    Reduction
──────────────────────────────────────────────────────
h264-crf32    14.5 MB        14.9x    93.3%
h264-crf28    17.1 MB        12.2x    91.8%
720p          3.6 MB         61.2x    98.4%
hevc          20.0 MB        10.4x    90.4%
noaudio       17.0 MB        12.2x    91.8%
──────────────────────────────────────────────────────
Original:     208 MB
```
