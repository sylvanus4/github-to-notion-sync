#!/bin/bash
# Skill Curator Registry Bootstrap
# Scans all skills, extracts git metadata, classifies origin, outputs registry.json

SKILLS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$SKILLS_DIR/.curator/registry.json"
TODAY=$(date +%Y-%m-%d)

echo "{"

first=true
for skill_dir in "$SKILLS_DIR"/*/; do
  [ -f "$skill_dir/SKILL.md" ] || continue

  name=$(basename "$skill_dir")

  # Skip hidden directories
  [[ "$name" == .* ]] && continue

  # Git metadata
  created=$(git log --diff-filter=A --format=%as -- "$skill_dir/SKILL.md" 2>/dev/null | tail -1)
  [ -z "$created" ] && created="$TODAY"

  last_modified=$(git log -1 --format=%as -- "$skill_dir/SKILL.md" 2>/dev/null)
  [ -z "$last_modified" ] && last_modified="$TODAY"

  # Size
  size_bytes=$(wc -c < "$skill_dir/SKILL.md" 2>/dev/null | tr -d ' ')

  # Origin classification via commit message pattern matching
  # All skills were bulk-imported, so we classify by the commit that last touched them
  # and by naming conventions
  commit_msg=$(git log -1 --format=%s -- "$skill_dir/SKILL.md" 2>/dev/null)
  all_msgs=$(git log --format=%s -- "$skill_dir/SKILL.md" 2>/dev/null)

  if echo "$all_msgs" | grep -qiE 'autoimprove|write-a-skill|hermes|auto-generate|skill-evolver|autoskill|self-improve'; then
    origin="agent"
  elif echo "$name" | grep -qE '^(kwp-|agency-|goose-|alphaear-|tab-|trading-|vibe-trading-|demo-|toss-|kis-|rr-|kb-|ecc-|ce-|sp-)'; then
    # Namespace-prefixed skills are generated via bulk skill pipelines
    origin="agent"
  elif echo "$name" | grep -qE '^(anthropic-|hf-|gws-|mcp-)'; then
    # Platform/integration skills are externally sourced
    origin="external"
  else
    origin="user"
  fi

  # Determine state based on protect_patterns
  state="active"
  case "$name" in
    hermes-*|omc-*|skill-curator) state="pinned" ;;
  esac

  # Output JSON entry
  if [ "$first" = true ]; then
    first=false
  else
    echo ","
  fi

  cat <<ENTRY
  "$name": {
    "state": "$state",
    "origin": "$origin",
    "created_at": "$created",
    "last_modified": "$last_modified",
    "last_used": "$last_modified",
    "use_count": 0,
    "tags": [],
    "size_bytes": $size_bytes,
    "consolidation_group": null,
    "notes": ""
  }
ENTRY

done

echo ""
echo "}"
