# Agent-Reach Setup Guide

## Installation

Agent-Reach is installed via pipx (isolated from project venv):

```bash
pipx install git+https://github.com/Panniantong/Agent-Reach.git
agent-reach install --env=auto --safe
```

The `--safe` flag previews all changes before applying. `--env=auto` detects the local environment and installs appropriate tools.

## Verifying Installation

```bash
agent-reach doctor
```

This shows all 16 channels and their status. At minimum, the following should be ✅:

- GitHub (gh CLI)
- YouTube (yt-dlp)
- Reddit (rdt-cli)
- RSS/Atom (curl)
- General Web (Jina Reader via curl)
- V2EX (public API)

## Cookie Configuration

Platforms that require login (Twitter/X, Xiaohongshu, Weibo) need browser cookies.

### Extracting Cookies

1. Install the **Cookie-Editor** browser extension ([Chrome](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/))
2. Log into the target platform with a **secondary account**
3. Click Cookie-Editor → Export → Copy as JSON
4. Run the configure command:

```bash
# Twitter
agent-reach configure twitter --cookie-from-clipboard

# Xiaohongshu
agent-reach configure xiaohongshu --cookie-from-clipboard
```

### Security Warning

- **Always use secondary/throwaway accounts** for cookie-based platforms
- Platforms may detect automated access and suspend the account
- Cookies are stored locally in `~/.agent-reach/` — never commit this directory
- Rotate cookies periodically (every 1-2 weeks)

## Proxy Configuration

For geo-restricted platforms:

```bash
agent-reach configure proxy --http "http://proxy:port"
agent-reach configure proxy --socks5 "socks5://proxy:port"
```

## Installing Individual Channels

```bash
# Install specific channel
agent-reach install --channels=twitter --safe
agent-reach install --channels=reddit --safe
agent-reach install --channels=xiaohongshu --safe

# Install all available channels
agent-reach install --env=auto --safe
```

## Updating

```bash
agent-reach check-update
pipx upgrade agent-reach
```

## Doctor Troubleshooting

| Doctor Output | Fix |
|--------------|-----|
| `twitter-cli: not found` | `agent-reach install --channels=twitter` or check `npm list -g twitter-cli` |
| `rdt-cli: not found` | `pipx install rdt-cli` |
| `mcporter: not found` | `npm install -g mcporter` |
| `yt-dlp: JS runtime not configured` | Add `--js-runtimes node` to yt-dlp config: `echo '--js-runtimes node' >> ~/Library/Application\ Support/yt-dlp/config` |
| `Exa not configured` | `mcporter config add exa https://mcp.exa.ai/mcp` (requires Exa API key) |
| `Cookie expired` | Re-extract from browser using Cookie-Editor extension |

## Uninstalling

```bash
agent-reach uninstall          # Removes config, tokens, skill files
pipx uninstall agent-reach     # Removes the CLI itself
```
