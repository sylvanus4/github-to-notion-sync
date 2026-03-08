#!/usr/bin/env bash
set -euo pipefail

# Convert a Skill Seekers output to Cursor format and install
# Usage: bash convert-to-cursor.sh <output-dir> [skill-name]
# Example: bash convert-to-cursor.sh output/react react-docs

OUTPUT_DIR="${1:?Usage: convert-to-cursor.sh <output-dir> [skill-name]}"
SKILL_NAME="${2:-$(basename "$OUTPUT_DIR")}"
CURSOR_SKILLS_DIR=".cursor/skills"
TARGET_DIR="${CURSOR_SKILLS_DIR}/${SKILL_NAME}"

if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Error: Output directory '$OUTPUT_DIR' not found."
  echo "Run 'skill-seekers create <source>' first."
  exit 1
fi

echo "Packaging for Cursor..."
skill-seekers package "$OUTPUT_DIR" --target cursor

echo "Checking for conflicts..."
if [ -d "$CURSOR_SKILLS_DIR" ]; then
  skill-seekers detect-conflicts "$OUTPUT_DIR" --skills-dir "$CURSOR_SKILLS_DIR" || true
fi

echo "Installing to ${TARGET_DIR}..."
mkdir -p "$TARGET_DIR"
skill-seekers install-agent "$OUTPUT_DIR/" --agent cursor

echo "Installed skill '${SKILL_NAME}' to ${TARGET_DIR}/"
echo "Restart Cursor to pick up the new skill."
