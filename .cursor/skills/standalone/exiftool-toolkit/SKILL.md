# exiftool-toolkit

Read, write, and manipulate metadata in virtually every image, video, and audio format via ExifTool CLI (`exiftool`). The single most comprehensive metadata tool available -- supports 26,000+ tag names across EXIF, IPTC, XMP, GPS, ICC Profile, MakerNotes, JFIF, GeoTIFF, ID3, and 400+ file formats. Essential for privacy scrubbing, forensic analysis, photo organization, copyright embedding, and geotagging workflows.

Use when the user asks to "strip metadata", "read EXIF", "GPS coordinates from photo", "batch rename by date", "copyright tag", "remove location data", "photo forensics", "check camera info", "metadata privacy", "exiftool", "EXIF data", "XMP edit", "IPTC keywords", "geotag photos", "embedded thumbnail", "maker notes", "image metadata", "video metadata", "batch metadata", "사진 메타데이터", "EXIF 정보", "GPS 좌표 추출", "메타데이터 제거", "촬영 정보 확인", "저작권 태그", "위치 정보 삭제", "사진 날짜 정리", "exiftool-toolkit", or any task involving reading, writing, or manipulating file metadata.

Do NOT use for pixel-level image editing (use vips-toolkit, opencv-toolkit, or imagemagick-toolkit). Do NOT use for image format conversion (use vips-toolkit). Do NOT use for video encoding/transcoding (use ffmpeg-toolkit). Do NOT use for computer vision or ML inference (use opencv-toolkit).

## Installation

```bash
# macOS (Homebrew)
brew install exiftool

# Verify
exiftool -ver
```

## Step 0: Probe Metadata (Always Start Here)

```bash
# Full metadata dump (all tags, all groups)
exiftool "photo.jpg"

# Compact summary (most useful tags)
exiftool -s -G1 "photo.jpg"
# -s: short tag names, -G1: show group name (EXIF, IPTC, XMP, etc.)

# Specific tag
exiftool -Model -LensModel -FocalLength -ISO -ShutterSpeed -FNumber "photo.jpg"

# All GPS data
exiftool -gps:all "photo.jpg"

# Machine-readable JSON output
exiftool -json "photo.jpg"

# Machine-readable CSV (batch)
exiftool -csv *.jpg > metadata.csv

# List all writable tags for a format
exiftool -listw -JPEG

# Check all tags in a specific group
exiftool -EXIF:all "photo.jpg"
exiftool -XMP:all "photo.jpg"
exiftool -IPTC:all "photo.jpg"
```

## Operation Categories

### Category 1: Read & Extract Metadata

```bash
# Camera and lens info
exiftool -Make -Model -LensModel -LensInfo "photo.jpg"

# Exposure settings
exiftool -ExposureTime -FNumber -ISO -ExposureMode -MeteringMode "photo.jpg"

# Date/time (all variants)
exiftool -AllDates "photo.jpg"
# Shows: DateTimeOriginal, CreateDate, ModifyDate

# File dimensions and format
exiftool -ImageWidth -ImageHeight -FileType -MIMEType -ColorSpace "photo.jpg"

# GPS coordinates (decimal degrees)
exiftool -gpslatitude -gpslongitude -gpsaltitude -n "photo.jpg"
# -n: numeric output (no DMS formatting)

# GPS as Google Maps URL
exiftool -p 'https://maps.google.com/?q=$gpslatitude,$gpslongitude' -n "photo.jpg"

# Embedded thumbnail extraction
exiftool -b -ThumbnailImage "photo.jpg" > thumbnail.jpg

# Extract all embedded images (preview, thumbnail)
exiftool -a -b -W %d%f_%t%-c.%s -preview:all "photo.jpg"

# ICC profile extraction
exiftool -b -ICC_Profile "photo.jpg" > profile.icc

# Video metadata
exiftool -Duration -VideoFrameRate -ImageWidth -ImageHeight \
  -AudioChannels -AudioSampleRate "video.mp4"

# Recursive directory scan with specific tags
exiftool -r -csv -DateTimeOriginal -Model -ImageSize photos/ > inventory.csv
```

### Category 2: Write & Modify Metadata

```bash
# Set copyright and author
exiftool -Copyright="(c) 2026 John Doe" -Artist="John Doe" "photo.jpg"

# Set multiple IPTC keywords
exiftool -Keywords="landscape" -Keywords="sunset" -Keywords="california" "photo.jpg"

# Set XMP description and title
exiftool -XMP:Title="Golden Gate Bridge at Sunset" \
  -XMP:Description="Wide-angle shot from Baker Beach" "photo.jpg"

# Set creation date (fix incorrect camera clock)
exiftool -AllDates="2026:05:04 14:30:00" "photo.jpg"

# Shift all dates by +2 hours (timezone correction)
exiftool -AllDates+=2 "photo.jpg"

# Shift dates by -1 day, 3 hours, 30 minutes
exiftool "-AllDates-=1 3:30:0" "photo.jpg"

# Set GPS coordinates manually
exiftool -GPSLatitude=37.7749 -GPSLongitude=-122.4194 \
  -GPSLatitudeRef=N -GPSLongitudeRef=W "photo.jpg"

# Set GPS from decimal degrees (simpler)
exiftool -XMP:GPSLatitude=37.7749 -XMP:GPSLongitude=-122.4194 "photo.jpg"

# Set rating (1-5 stars)
exiftool -Rating=5 -XMP:Rating=5 "photo.jpg"

# Copy metadata from one file to another
exiftool -TagsFromFile "source.jpg" "destination.jpg"

# Copy only EXIF from source, XMP from another
exiftool -TagsFromFile "src_exif.jpg" -EXIF:all \
  -TagsFromFile "src_xmp.jpg" -XMP:all "target.jpg"
```

### Category 3: Privacy & Security (Strip Metadata)

```bash
# Remove ALL metadata (nuclear option)
exiftool -all= "photo.jpg"

# Remove all metadata but preserve ICC profile and orientation
exiftool -all= --icc_profile:all --orientation "photo.jpg"

# Remove GPS/location only
exiftool -gps:all= "photo.jpg"

# Remove GPS from all images recursively
exiftool -r -gps:all= photos/

# Remove GPS + keep everything else
exiftool -GPS:all= -XMP:GPSLatitude= -XMP:GPSLongitude= \
  -XMP:GPSAltitude= "photo.jpg"

# Strip MakerNotes (camera-specific proprietary data)
exiftool -MakerNotes:all= "photo.jpg"

# Remove personal info but keep technical data
exiftool -Author= -Copyright= -Artist= -OwnerName= \
  -SerialNumber= -InternalSerialNumber= \
  -GPSLatitude= -GPSLongitude= "photo.jpg"

# Remove XMP editing history (Photoshop/Lightroom breadcrumbs)
exiftool -XMP:History:all= -XMP:DocumentID= -XMP:OriginalDocumentID= "photo.jpg"

# Verify metadata is clean
exiftool -gps:all -Author -Copyright -SerialNumber "photo.jpg"
# Should return nothing or "not defined"

# Production pipeline: sanitize for web upload
sanitize_for_web() {
  local src="$1" dst="$2"
  cp "$src" "$dst"
  exiftool -all= \
    --icc_profile:all \
    --orientation \
    --ImageWidth --ImageHeight \
    -overwrite_original "$dst"
}
```

### Category 4: Batch Rename by Metadata

```bash
# Rename by date taken: IMG_1234.jpg → 2026-05-04_143000.jpg
exiftool '-FileName<DateTimeOriginal' -d '%Y-%m-%d_%H%M%S.%%le' *.jpg

# Rename with camera model prefix
exiftool '-FileName<${Model}_${DateTimeOriginal}' -d '%Y%m%d_%H%M%S.%%le' *.jpg
# Result: "iPhone15Pro_20260504_143000.jpg"

# Rename with sequence number for duplicates
exiftool '-FileName<DateTimeOriginal' -d '%Y-%m-%d_%H%M%S%%-c.%%le' *.jpg
# %-c adds -1, -2 suffix for same-second shots

# Organize into date folders
exiftool '-Directory<DateTimeOriginal' -d 'sorted/%Y/%Y-%m-%d' *.jpg
# Creates: sorted/2026/2026-05-04/photo.jpg

# Organize into camera model folders
exiftool '-Directory<${Model}' *.jpg

# Combined: date folder + rename
exiftool '-Directory<DateTimeOriginal' -d 'archive/%Y/%m' \
  '-FileName<DateTimeOriginal' -d '%Y%m%d_%H%M%S%%-c.%%le' *.jpg

# Dry run (preview changes without executing)
exiftool -n '-FileName<DateTimeOriginal' -d '%Y-%m-%d_%H%M%S.%%le' *.jpg
# (No -execute, just shows what would happen... actually use -v flag for preview)

# Safe rename with TestName (preview only)
exiftool '-TestName<DateTimeOriginal' -d '%Y-%m-%d_%H%M%S.%%le' *.jpg
```

### Category 5: Date & Time Operations

```bash
# Show all date fields
exiftool -time:all -s "photo.jpg"

# Fix camera clock that was 2 hours slow
exiftool -AllDates+=2 *.jpg

# Fix FileModifyDate to match EXIF date
exiftool '-FileModifyDate<DateTimeOriginal' *.jpg

# Set date from filename (YYYYMMDD_HHMMSS pattern)
exiftool '-AllDates<${FileName}' -d '%Y%m%d_%H%M%S' *.jpg

# Shift dates for a timezone change (UTC+0 → UTC+9)
exiftool -AllDates+=9 -overwrite_original *.jpg

# Find photos taken in a specific date range
exiftool -if '$DateTimeOriginal ge "2026:05:01" and $DateTimeOriginal lt "2026:06:01"' \
  -FileName *.jpg

# Find photos taken at night (18:00-06:00)
exiftool -if '$DateTimeOriginal =~ /( 1[89]| 2\d| 0[0-5]):/' -FileName *.jpg
```

### Category 6: Conditional Processing

```bash
# Process only photos from a specific camera
exiftool -if '$Model =~ /iPhone/' -Copyright="(c) 2026" *.jpg

# Process only photos wider than 3000px
exiftool -if '$ImageWidth > 3000' -FileName *.jpg

# Process only RAW files
exiftool -if '$FileType =~ /^(CR2|NEF|ARW|DNG|RAF)$/' -s -FileName *.{cr2,nef,arw,dng,raf}

# Find photos with no GPS data
exiftool -if 'not defined $GPSLatitude' -FileName *.jpg

# Find photos with GPS (for privacy audit)
exiftool -if 'defined $GPSLatitude' -FileName -GPSLatitude -GPSLongitude -n *.jpg

# Find edited/modified photos (has XMP history)
exiftool -if 'defined $XMP:History' -FileName *.jpg

# Find photos shot at high ISO (noisy)
exiftool -if '$ISO > 6400' -FileName -ISO -Model *.jpg

# Delete originals where copy already exists (carefully!)
exiftool -if '$Rating >= 3' -FileName *.jpg
```

### Category 7: Video Metadata

```bash
# Full video metadata
exiftool -G1 "video.mp4"

# Key video fields
exiftool -Duration -VideoFrameRate -ImageSize -Rotation \
  -AudioChannels -AudioBitsPerSample -AudioSampleRate \
  -CompressorName -BitDepth "video.mp4"

# GPS from video (phone recordings)
exiftool -GPSLatitude -GPSLongitude -GPSAltitude -n "video.mp4"

# Set video creation date
exiftool -CreateDate="2026:05:04 14:30:00" "video.mp4"

# Copy metadata between video files
exiftool -TagsFromFile "original.mp4" -all:all "transcoded.mp4"

# Extract frame rate and duration for ffmpeg pipeline
fps=$(exiftool -s -s -s -VideoFrameRate "video.mp4")
dur=$(exiftool -s -s -s -Duration "video.mp4")
echo "FPS: $fps, Duration: $dur"

# Batch: list all video durations in a directory
exiftool -csv -FileName -Duration -VideoFrameRate -ImageSize videos/*.mp4
```

### Category 8: Geolocation & Mapping

```bash
# Read GPS as decimal degrees
exiftool -n -GPSLatitude -GPSLongitude "photo.jpg"

# Read GPS as DMS (degrees/minutes/seconds)
exiftool -GPSPosition "photo.jpg"

# Generate KML file from GPS-tagged photos
exiftool -p "$HOME/kml_template.fmt" -n photos/*.jpg > photos.kml

# Geotag photos from GPX track log
exiftool -geotag "track.gpx" photos/*.jpg
# Interpolates timestamps between GPS points

# Geotag with time offset (camera clock was 30 min ahead of GPS)
exiftool -geotag "track.gpx" -geosync=-00:30:00 photos/*.jpg

# Reverse geocode: get address from GPS (needs web lookup)
lat=$(exiftool -s -s -s -n -GPSLatitude "photo.jpg")
lon=$(exiftool -s -s -s -n -GPSLongitude "photo.jpg")
echo "https://nominatim.openstreetmap.org/reverse?lat=$lat&lon=$lon&format=json"

# Find all photos near a location (within ~1km)
exiftool -if '$GPSLatitude and abs($GPSLatitude - 37.7749) < 0.01 and abs($GPSLongitude - (-122.4194)) < 0.01' \
  -FileName -GPSPosition -n photos/*.jpg

# Remove all geolocation from entire library
exiftool -r -overwrite_original \
  -GPS:all= -XMP:GPSLatitude= -XMP:GPSLongitude= -XMP:GPSAltitude= \
  photos/
```

### Category 9: Forensic Analysis

```bash
# Detect if image was edited (check software tags)
exiftool -Software -ProcessingSoftware -HistorySoftwareAgent \
  -XMP:CreatorTool -XMP:History "photo.jpg"

# Compare original vs edited (diff metadata)
exiftool "original.jpg" > /tmp/orig.txt
exiftool "edited.jpg" > /tmp/edit.txt
diff /tmp/orig.txt /tmp/edit.txt

# Check for inconsistencies (dates don't match)
exiftool -AllDates -FileModifyDate -FileCreateDate "photo.jpg"
# If ModifyDate < CreateDate, file was likely backdated

# Extract embedded thumbnail (may show pre-edit version)
exiftool -b -ThumbnailImage "edited.jpg" > embedded_thumb.jpg

# Check serial number chain (identify camera)
exiftool -SerialNumber -InternalSerialNumber -LensSerialNumber "photo.jpg"

# Detect AI-generated images (check for common AI tool signatures)
exiftool -Software -XMP:CreatorTool -Comment -UserComment "suspect.jpg" | \
  grep -iE "(dall-e|midjourney|stable.diffusion|firefly|comfyui)"

# Full provenance chain
exiftool -G1 -s -XMP:History:all -XMP:DerivedFrom:all "photo.jpg"

# Validate file integrity
exiftool -validate -error "photo.jpg"

# ── Advanced Forgery Detection Pipeline ──

# 1. JPEG quantization table fingerprinting
# Different cameras/software produce unique DQT tables
# If DQT doesn't match claimed camera model → likely re-saved or manipulated
exiftool -HtmlDump "suspect.jpg" > /tmp/hexdump.html
# Compare DQT signature with known camera profiles

# 2. EXIF-JPEG consistency check script
check_forgery() {
  local file="$1"
  echo "=== Forgery Indicators for: $file ==="

  # Date chain consistency
  orig=$(exiftool -s -s -s -DateTimeOriginal "$file")
  create=$(exiftool -s -s -s -CreateDate "$file")
  modify=$(exiftool -s -s -s -ModifyDate "$file")
  fmod=$(exiftool -s -s -s -FileModifyDate "$file")
  echo "DateTimeOriginal: $orig"
  echo "CreateDate:       $create"
  echo "ModifyDate:       $modify"
  echo "FileModifyDate:   $fmod"

  # Software trail
  sw=$(exiftool -s -s -s -Software "$file")
  tool=$(exiftool -s -s -s -CreatorTool "$file")
  [ -n "$sw" ] && echo "WARNING: Software tag present: $sw"
  [ -n "$tool" ] && echo "WARNING: CreatorTool present: $tool"

  # Thumbnail vs main image mismatch
  exiftool -b -ThumbnailImage "$file" > /tmp/thumb_$$.jpg 2>/dev/null
  if [ -s /tmp/thumb_$$.jpg ]; then
    thumb_dim=$(exiftool -s -s -s -ImageSize /tmp/thumb_$$.jpg)
    echo "Embedded thumbnail: $thumb_dim (compare visually for pre-edit)"
  fi
  rm -f /tmp/thumb_$$.jpg

  # XMP editing history length
  hist_count=$(exiftool -XMP:HistoryAction "$file" 2>/dev/null | wc -l)
  echo "XMP history entries: $hist_count"
}
check_forgery "suspect.jpg"

# 3. Batch authenticity scan: flag files with editing signatures
exiftool -r -csv \
  -FileName -Model -Software -CreatorTool -ModifyDate -DateTimeOriginal \
  -if '$Software or $CreatorTool or ($ModifyDate and $DateTimeOriginal and $ModifyDate ne $DateTimeOriginal)' \
  photos/ > /tmp/edited_files.csv

# 4. C2PA / Content Credentials (Adobe CAI) inspection
# Modern cameras and tools embed C2PA manifests
exiftool -XMP-c2pa:all "photo.jpg"
# Non-empty result = has Content Credentials chain
```

### Category 10: Config Files & Advanced

```bash
# Custom config file for recurring operations
cat > ~/.ExifTool_config << 'PERL'
# Define shortcut tags
%Image::ExifTool::UserDefined::Shortcuts = (
    WebClean => [
        'GPS:all', 'MakerNotes:all', 'SerialNumber',
        'InternalSerialNumber', 'OwnerName',
        'XMP:History:all', 'XMP:DocumentID',
    ],
    BasicInfo => [
        'Model', 'LensModel', 'FocalLength', 'FNumber',
        'ExposureTime', 'ISO', 'DateTimeOriginal',
    ],
);
PERL

# Usage with shortcuts
exiftool -WebClean= "photo.jpg"           # strip all privacy-sensitive tags
exiftool -BasicInfo "photo.jpg"            # quick camera info

# Structured output formats
exiftool -json "photo.jpg"                 # JSON
exiftool -csv "photo.jpg"                  # CSV
exiftool -xml "photo.jpg"                  # XMP/XML
exiftool -htmlDump "photo.jpg" > dump.html # visual hex dump

# Process arg file (list of specific files)
find photos/ -name '*.jpg' -newer lastrun > /tmp/new_files.txt
exiftool -@ /tmp/new_files.txt -Copyright="(c) 2026"

# Preserve original files (creates .jpg_original backup)
exiftool -Copyright="test" "photo.jpg"
# To suppress backup: -overwrite_original
# To restore: mv photo.jpg_original photo.jpg
```

### Category 11: Integration with Other Toolkits

```bash
# Pipeline: exiftool (read metadata) → vips (process) → exiftool (write back)
# Step 1: Extract key metadata
exiftool -json "original.jpg" > /tmp/meta.json

# Step 2: Process image (vips strips most metadata)
vipsthumbnail "original.jpg" -s 1200x --delete -o "processed.jpg[Q=85]"

# Step 3: Restore metadata from original
exiftool -TagsFromFile "original.jpg" \
  -EXIF:all -IPTC:all -XMP:all \
  -GPS:all= \
  -overwrite_original "processed.jpg"
# Copies all metadata but strips GPS (privacy)

# Pipeline: ffmpeg (extract frame) → exiftool (read video GPS → write to frame)
ffmpeg -i "video.mp4" -vframes 1 -q:v 2 "frame.jpg" 2>/dev/null
exiftool -TagsFromFile "video.mp4" \
  -GPSLatitude -GPSLongitude -GPSAltitude \
  -DateTimeOriginal -CreateDate \
  -overwrite_original "frame.jpg"
```

## Error Handling & Troubleshooting

| Error / Symptom | Root Cause | Fix |
|---|---|---|
| `Warning: Tag 'XXX' is not defined` | Typo in tag name or proprietary tag | Check exact name: `exiftool -list -EXIF:all \| grep -i xxx`; use `-f` to force unknown tags |
| `Error: File not found` on wildcards | Shell glob expansion issue with spaces | Quote paths: `exiftool "dir with spaces/*.jpg"` or use `-r "dir"` |
| `0 image files updated` | Tag is read-only or value format wrong | Verify writable: `exiftool -listw \| grep TagName`; check YYYY:MM:DD format for dates |
| `Nothing to do` | Tag already has the target value | Normal; exiftool skips no-change writes by design |
| `Minor error in IFD0` / IFD warnings | Corrupted EXIF structure from editing software | Rebuild: `exiftool -all= -TagsFromFile @ -all:all -unsafe file.jpg` |
| Garbled Korean/CJK characters | Missing charset specification | Add `-charset UTF8 -charset IPTC=UTF8` |
| Backup files filling disk | `-overwrite_original` not set in batch scripts | Set in `~/.ExifTool_config`: `%Image::ExifTool::UserDefined::Options = (Overwrite => 1);` |

```bash
# Debug: verbose trace of what exiftool reads/writes
exiftool -v3 "photo.jpg" 2>&1 | head -100
# -v0 to -v5: increasing verbosity; -v3 is usually sufficient

# Validate file structure without modifying
exiftool -validate -warning -error "photo.jpg"
# Exit code 0 = clean; non-zero = structural issues

# Dry run before destructive batch
exiftool -r -FileName -FileSize -Model "photos/" | head -20
# Read-only: lists matching files without modification

# Measure performance on large directories
time exiftool -fast2 -r -FileName "archive/"
# -fast2 skips composite tags (2-5x faster for 10K+ files)
```

## Gotchas

- **Backup files**: By default, exiftool creates `*.jpg_original` backups. Use `-overwrite_original` to skip, but only after verifying your command is correct. Use `-overwrite_original_in_place` for atomic replacement (safer on shared filesystems).
- **Character encoding**: Tag values with non-ASCII characters (Korean, Japanese) require UTF-8. Add `-charset UTF8` for safe handling. For IPTC tags specifically: `-charset IPTC=UTF8`.
- **Date format**: ExifTool uses `YYYY:MM:DD HH:MM:SS` (colons in date). Not `YYYY-MM-DD`. Using hyphens silently fails or corrupts the tag.
- **Writable vs readable**: Not all tags are writable. `exiftool -listw` shows writable tags. Attempting to write a read-only tag silently does nothing.
- **MakerNotes fragility**: MakerNotes are binary blobs tied to file structure. Resizing an image and then copying MakerNotes from the original can corrupt them. Copy MakerNotes only between unmodified files of the same camera model.
- **Video metadata limitations**: MP4/MOV metadata writing is well-supported, but some containers (MKV, AVI) have limited write support. Always test with `-v2` verbose mode first.
- **Recursive safety**: `-r` flag processes ALL matching files in subdirectories. Always do a dry run first: `exiftool -r -FileName photos/` (read-only) before `exiftool -r -all= photos/` (destructive).
- **GPS precision**: `-n` flag gives raw decimal degrees. Without it, you get DMS strings that are harder to parse programmatically. Always use `-n` in scripts.
- **Large batch performance**: For 10K+ files, use `-fast2` (skip processing composite tags) or `-fast` (skip extracting MakerNotes) to speed up reads.
