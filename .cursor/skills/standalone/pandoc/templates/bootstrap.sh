#!/usr/bin/env bash
set -euo pipefail

TEMPLATES_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT="${TEMPLATES_DIR}/thaki-report.docx"

if ! command -v pandoc &>/dev/null; then
  echo "ERROR: pandoc not found. Install with: brew install pandoc" >&2
  exit 1
fi

if [ -f "$OUTPUT" ]; then
  echo "Template already exists: $OUTPUT"
  echo "Delete it first if you want to regenerate."
  exit 0
fi

pandoc -o "$OUTPUT" --print-default-data-file reference.docx
echo "Created reference template: $OUTPUT"
echo "Open in Word/LibreOffice to customize styles, then save."
