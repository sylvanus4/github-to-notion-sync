#!/usr/bin/env bash
set -euo pipefail

# stop-server.sh — Stop the tutor companion server for a given session directory.

SCREEN_DIR="${1:-}"

if [[ -z "$SCREEN_DIR" ]]; then
  echo '{"type":"error","message":"Usage: stop-server.sh <screen_dir>"}' >&2
  exit 1
fi

SERVER_INFO="$SCREEN_DIR/.server-info"

if [[ ! -f "$SERVER_INFO" ]]; then
  echo '{"type":"error","message":"No .server-info found in '"$SCREEN_DIR"'"}' >&2
  exit 1
fi

PORT="$(grep -o '"port":[[:space:]]*[0-9]*' "$SERVER_INFO" | grep -o '[0-9]*')"

if [[ -z "$PORT" ]]; then
  echo '{"type":"error","message":"Could not read port from .server-info"}' >&2
  exit 1
fi

PIDS="$(lsof -ti :"$PORT" 2>/dev/null || true)"
if [[ -n "$PIDS" ]]; then
  echo "$PIDS" | xargs kill 2>/dev/null || true
fi

echo '{"stopped":true,"port":'"$PORT"'}' > "$SCREEN_DIR/.server-stopped"
rm -f "$SERVER_INFO"
rm -rf "$SCREEN_DIR"

echo '{"type":"server-stopped","screen_dir":"'"$SCREEN_DIR"'"}'
