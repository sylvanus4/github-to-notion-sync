# Authentication & Configuration Commands

## Auth Commands

### tossctl auth login

Start browser-based login flow via Playwright.

```bash
tossctl auth login
```

Opens Chromium browser → user logs in to Toss Securities web → session captured to `session.json`.

### tossctl auth status

Check current authentication status.

```bash
tossctl auth status
tossctl auth status --output json
```

Output formats: `text` (default), `json`

### tossctl auth logout

Clear the local session.

```bash
tossctl auth logout
```

Removes `session.json`.

### tossctl auth import-playwright-state

Import a Playwright browser state file from an external source.

```bash
tossctl auth import-playwright-state /path/to/state.json
```

Useful when session was captured by a separate Playwright script.

### tossctl auth doctor

Run auth-specific diagnostics.

```bash
tossctl auth doctor
```

Checks: Python version, Playwright installation, Chromium binary, auth-helper script.

## Config Commands

### tossctl config init

Create a default `config.json` with all trading features disabled.

```bash
tossctl config init
```

Location: `~/.config/tossctl/config.json`

### tossctl config show

Display the current configuration.

```bash
tossctl config show
```

## Doctor Command

### tossctl doctor

Run full system diagnostics.

```bash
tossctl doctor
```

Checks performed:
- tossctl binary version
- Python 3 availability
- Playwright installation
- Chromium browser binary
- Auth-helper script
- Config file validity
- Session file status

## Version Command

### tossctl version

Display the installed version.

```bash
tossctl version
```
