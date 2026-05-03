# REPO_ROOT Path Depth in Skill Scripts

When a Python/Bash script under `.claude/skills/<skill>/...` needs the repo root, count `parents[N]` carefully. Off-by-one bugs are silent and corrupt output paths.

## Reference Table

Script location → correct `parents[N]` for repo root:

| Script Path | parents[N] |
|-------------|-----------|
| `.claude/skills/<skill>/foo.py` | `parents[3]` |
| `.claude/skills/<skill>/scripts/foo.py` | `parents[4]` |
| `.claude/skills/<skill>/hooks/foo.py` | `parents[4]` |
| `.claude/skills/<skill>/scripts/sub/foo.py` | `parents[5]` |
| `.claude/hooks/foo.py` | `parents[2]` |
| `.claude/rules/...` (not executable) | N/A |
| `scripts/foo.py` | `parents[1]` |

`Path(__file__).resolve().parents[N]` — count up from the file itself.

## Verification One-Liner

After setting REPO_ROOT, paste this once during dev:

```python
assert (REPO_ROOT / "CLAUDE.md").exists(), f"REPO_ROOT wrong: {REPO_ROOT}"
```

`CLAUDE.md` is a stable repo-root marker for this project. Failed assert → adjust `parents[N]` and rerun.

## Why This Matters

- Wrong depth → output goes to `.claude/outputs/` instead of `outputs/`, or to user $HOME
- Easy to miss in code review (path looks plausible)
- Bit `extract_sft.py` and `extract_preference.py` once already (parents[3] → parents[4])

## Anti-Patterns

- Don't hardcode `Path("/Users/...")` — non-portable
- Don't use `os.getcwd()` — depends on invocation directory
- Don't compute via `__file__.split('/')` string ops — fragile
