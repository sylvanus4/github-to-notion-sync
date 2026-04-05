---
name: rhwp-setup
description: >-
  Install and configure the rhwp HWP/HWPX document toolkit: VS Code extension
  for in-IDE viewing, Rust-native CLI for conversion and inspection, and npm
  packages (@rhwp/core, @rhwp/editor) for web/pipeline integration. Runs
  prerequisite checks, builds from source, and verifies all components with a
  diagnostic health check. Use when the user asks to "install rhwp", "setup
  HWP tools", "configure HWP viewer", "rhwp-setup", "rhwp 설치", "HWP 도구
  설정", "HWP 뷰어 설치", or needs the rhwp environment ready for viewing or
  pipeline use. Do NOT use for converting HWP files (use rhwp-converter). Do
  NOT use for debugging HWP document structure (use rhwp-debug). Do NOT use
  for pipeline orchestration (use rhwp-pipeline).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "setup"
---
# rhwp Setup — HWP/HWPX Document Toolkit Installation

Install the complete rhwp toolkit: VS Code extension for IDE-level HWP viewing,
Rust CLI for command-line conversion and inspection, and npm packages for
programmatic web integration.

## Prerequisites

| Tool | Minimum Version | Check Command | Required For |
|------|----------------|---------------|--------------|
| Rust toolchain | 1.75+ | `rustc --version` | CLI build |
| Cargo | (bundled) | `cargo --version` | CLI build |
| Node.js | 18+ | `node --version` | npm packages, web editor |
| npm | 9+ | `npm --version` | npm packages |
| Docker | 20+ | `docker --version` | WASM builds (required for web/extension) |
| VS Code / Cursor | 1.82+ | `code --version` | Extension |

## Workflow

### Step 1: Check Prerequisites

Verify all required tools are installed:

```bash
echo "=== Rust ===" && rustc --version && cargo --version
echo "=== Node.js ===" && node --version && npm --version
echo "=== Docker ===" && docker --version 2>/dev/null || echo "Docker not found (optional)"
echo "=== Cursor/VS Code ===" && (cursor --version 2>/dev/null || code --version 2>/dev/null || echo "Neither cursor nor code CLI found")
```

If Rust is missing, guide the user to install via `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`.

### Step 2: Clone the rhwp Repository

```bash
RHWP_DIR="${HOME}/thaki/rhwp"
if [ -d "$RHWP_DIR" ]; then
  echo "rhwp already cloned at $RHWP_DIR"
  cd "$RHWP_DIR" && git pull
else
  git clone https://github.com/edwardkim/rhwp.git "$RHWP_DIR"
  cd "$RHWP_DIR"
fi
```

### Step 3: Build the CLI

Build the Rust-native CLI binary:

```bash
cd "$RHWP_DIR"
cargo build --release
```

Create a symlink so the `rhwp` command is available globally:

```bash
RHWP_BIN="$RHWP_DIR/target/release/rhwp"
if [ -f "$RHWP_BIN" ]; then
  sudo ln -sf "$RHWP_BIN" /usr/local/bin/rhwp
  echo "rhwp CLI linked to /usr/local/bin/rhwp"
else
  echo "ERROR: Build failed — $RHWP_BIN not found"
fi
```

### Step 4: Install VS Code Extension

Option A — Install from VS Code Marketplace (if published):

```bash
cursor --install-extension edwardkim.rhwp-vscode 2>/dev/null || \
code --install-extension edwardkim.rhwp-vscode 2>/dev/null || \
echo "Marketplace install failed, building from source..."
```

Option B — Build from source (requires WASM build first):

```bash
# WASM build (prerequisite — produces pkg/ directory)
cd "$RHWP_DIR"
cp .env.docker.example .env.docker  # first time only
docker compose --env-file .env.docker run --rm wasm

# Build extension
cd "$RHWP_DIR/rhwp-vscode"
npm install
npm run compile
npx vsce package
VSIX_FILE=$(ls rhwp-vscode-*.vsix 2>/dev/null | head -1)
if [ -n "$VSIX_FILE" ]; then
  cursor --install-extension "$VSIX_FILE" 2>/dev/null || \
  code --install-extension "$VSIX_FILE"
  echo "Extension installed from $VSIX_FILE"
else
  echo "ERROR: VSIX package not found"
fi
```

After installation, `.hwp` and `.hwpx` files open in the custom HWP Viewer
editor automatically when clicked in the file explorer. The extension supports
Canvas 2D rendering, virtual scroll, zoom (Ctrl+mouse wheel), and page navigation.

Also available via:
- [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=edwardkim.rhwp-vscode)
- [Open VSX](https://open-vsx.org/extension/edwardkim/rhwp-vscode)

### Step 5: Install npm Packages (Optional)

For web/pipeline integration:

```bash
cd "$RHWP_DIR"
npm install @rhwp/core @rhwp/editor
```

Or in the current project:

```bash
npm install @rhwp/core @rhwp/editor
```

### Step 6: Diagnostic Health Check

Verify all components:

```bash
echo "=== CLI ===" && rhwp --help 2>/dev/null && echo "OK" || echo "FAIL: rhwp CLI not found"
echo "=== Extension ===" && (cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null) | grep -i rhwp && echo "OK" || echo "FAIL: Extension not installed"
echo "=== npm @rhwp/core ===" && node -e "require('@rhwp/core')" 2>/dev/null && echo "OK" || echo "SKIP: @rhwp/core not installed (optional)"
echo "=== npm @rhwp/editor ===" && node -e "require('@rhwp/editor')" 2>/dev/null && echo "OK" || echo "SKIP: @rhwp/editor not installed (optional)"
```

### Step 7: Quick Smoke Test

Test the CLI with a sample file if available:

```bash
SAMPLE=$(find "$RHWP_DIR" -name "*.hwp" -o -name "*.hwpx" | head -1)
if [ -n "$SAMPLE" ]; then
  mkdir -p /tmp/rhwp-test
  rhwp export-svg "$SAMPLE" -o /tmp/rhwp-test/
  echo "Smoke test output: /tmp/rhwp-test/"
  ls /tmp/rhwp-test/
else
  echo "No sample HWP files found for smoke test"
fi
```

## Examples

### First-Time Setup

User: "rhwp 처음 설치해줘"

```bash
# Step 1: Clone
git clone https://github.com/nickel-org/rhwp.git ~/rhwp

# Step 2: Build
cd ~/rhwp && cargo build --release

# Step 3: Symlink
sudo ln -sf ~/rhwp/target/release/rhwp /usr/local/bin/rhwp

# Step 4: Verify
rhwp --help
```

### Re-Install After Rust Update

User: "Rust 업데이트 후 rhwp가 안 돼"

```bash
cd ~/rhwp && cargo clean && cargo build --release
rhwp --help  # verify
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `cargo build` fails with linker errors | Install build essentials: `xcode-select --install` (macOS) |
| Extension not visible in Cursor | Restart Cursor after installing the VSIX |
| `rhwp` command not found after build | Check symlink: `ls -la /usr/local/bin/rhwp` |
| WASM build needed | Use Docker: `cd rhwp && docker compose up --build` |
| npm package import fails | Ensure Node.js 18+ and run `npm install` in the package directory |

## Output

Report a summary table with component status:

| Component | Status | Path / Version |
|-----------|--------|----------------|
| CLI | OK / FAIL | `/usr/local/bin/rhwp` |
| VS Code Extension | OK / FAIL | `edwardkim.rhwp-vscode` |
| @rhwp/core | OK / SKIP | npm package |
| @rhwp/editor | OK / SKIP | npm package |
