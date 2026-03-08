#!/usr/bin/env bash
set -euo pipefail

# Install Skill Seekers with all extras
# Usage: bash .cursor/skills/skill-seekers/scripts/install.sh [extras]
# Examples:
#   bash install.sh          # Install with all extras
#   bash install.sh mcp      # Install with MCP support only
#   bash install.sh video    # Install with video extraction

EXTRAS="${1:-all}"

echo "Installing skill-seekers[${EXTRAS}]..."

if command -v pip3 &>/dev/null; then
  pip3 install "skill-seekers[${EXTRAS}]"
elif command -v pip &>/dev/null; then
  pip install "skill-seekers[${EXTRAS}]"
else
  echo "Error: pip not found. Install Python 3.10+ first."
  exit 1
fi

echo "Verifying installation..."
skill-seekers --version

echo "Done. Run 'skill-seekers --help' for usage."
