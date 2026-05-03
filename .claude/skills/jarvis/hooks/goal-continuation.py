#!/usr/bin/env python3
"""Jarvis Goal Mode — CLI utility for goal state evaluation.

Reads active goal state, runs check_cmd criteria, checks budget, and prints
a JSON status report. Used by Claude during /loop iterations, NOT as a Stop hook.

Usage:
  python3 goal-continuation.py [<goal-id>]

Output (JSON to stdout):
  {
    "goal_id": "...",
    "status": "pursuing|achieved|budget-limited|unmet",
    "criteria_met": ["C1", "C2"],
    "criteria_remaining": ["C3"],
    "budget_status": "ok|max_iters|max_cost|...",
    "consumed": {...},
    "budget": {...},
    "next_iter": 5,
    "continuation_prompt": "..."   // only if status == pursuing
  }

Exit codes:
  0 = pursuing (continue loop)
  1 = terminal (achieved/budget-limited/unmet — stop loop)
  2 = no active goal found
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
GOALS_DIR = REPO_ROOT / ".claude/skills/jarvis/state/goals"
TIMEOUT_SEC = 15


def find_goal(goal_id: str | None) -> tuple[Path | None, dict | None]:
    if not GOALS_DIR.exists():
        return None, None
    if goal_id:
        p = GOALS_DIR / f"{goal_id}.json"
        if p.exists():
            return p, json.loads(p.read_text())
        return None, None
    candidates = []
    for p in sorted(GOALS_DIR.glob("*.json")):
        try:
            g = json.loads(p.read_text())
        except Exception:
            continue
        if g.get("mode") == "dry-run":
            continue
        if g.get("status") == "pursuing":
            candidates.append((p, g))
    if not candidates:
        return None, None
    candidates.sort(key=lambda x: x[1].get("updated_at", ""), reverse=True)
    return candidates[0]


def safe_check_cmd(cmd: str) -> bool:
    if not isinstance(cmd, str) or len(cmd) > 1000:
        return False
    forbidden = [r"\brm\s+-rf\s+/", r":\(\)\s*\{", r"\bdd\s+if=", r"\bmkfs\b",
                 r"\bcurl\b.*\|\s*sh", r"\bwget\b.*\|\s*sh"]
    return not any(re.search(p, cmd) for p in forbidden)


def run_check(cmd: str) -> bool:
    if not safe_check_cmd(cmd):
        return False
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=str(REPO_ROOT),
            capture_output=True, timeout=TIMEOUT_SEC, text=True,
        )
        return r.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False


def evaluate_criteria(g: dict) -> tuple[list, list]:
    met, remaining = [], []
    for c in g.get("evaluation_criteria", []):
        if isinstance(c, dict) and c.get("check_cmd"):
            cid = c.get("id", c.get("desc", "?"))
            if run_check(c["check_cmd"]):
                met.append(cid)
            else:
                remaining.append(cid)
        elif isinstance(c, dict):
            cid = c.get("id", c.get("desc", "?"))
            if cid in g.get("criteria_met", []):
                met.append(cid)
            else:
                remaining.append(cid)
    return met, remaining


def budget_status(g: dict) -> str:
    b, c = g.get("budget", {}), g.get("consumed", {})
    if c.get("iters", 0) >= b.get("max_iters", 999):
        return "max_iters"
    if c.get("cost_usd", 0) >= b.get("max_cost_usd", 1e9):
        return "max_cost"
    if c.get("tokens", 0) >= b.get("max_tokens", 1e9):
        return "max_tokens"
    deadline = b.get("deadline")
    if deadline:
        try:
            dl = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
            now = datetime.now(dl.tzinfo or timezone.utc)
            if now >= dl:
                return "deadline"
        except Exception:
            pass
    return "ok"


def build_continuation_prompt(g: dict, met: list, remaining: list) -> str:
    consumed = g.get("consumed", {})
    budget = g.get("budget", {})
    last = g["iterations"][-1] if g.get("iterations") else {}
    iter_n = consumed.get("iters", 0) + 1
    p = g.get("id", "unknown").replace("goal-", "")
    state_path = f".claude/skills/jarvis/state/goals/{g.get('id', 'unknown')}.json"

    return (
        f"[GOAL: {g.get('objective', '?')}]\n"
        f"goal_id: {g.get('id', '?')}\n"
        f"Iteration: {iter_n}/{budget.get('max_iters', '?')}\n"
        f"Consumed: {consumed.get('tokens', 0)}tok / ${consumed.get('cost_usd', 0):.2f}\n"
        f"Last outcome: {last.get('outcome', '(none)')}\n"
        f"Auto-checked criteria_met: {met}\n"
        f"Remaining: {remaining}\n"
        f"Suggested next: {last.get('next_step', 'inspect state and decide')}\n\n"
        f"가장 작은 유용한 작업 1개를 실행하라.\n"
        f"완료 후 state JSON ({state_path})을 갱신:\n"
        f"  - iterations 배열에 새 항목 추가\n"
        f"  - consumed.iters/tokens/cost_usd 갱신\n"
        f"외부 검증 (check_cmd)이 있는 criteria는 자동 평가됨.\n"
    )


def main() -> int:
    goal_id = sys.argv[1] if len(sys.argv) > 1 else None
    p, g = find_goal(goal_id)

    if g is None:
        print(json.dumps({"error": "no active goal found"}))
        return 2

    bs = budget_status(g)
    met, remaining = evaluate_criteria(g)
    consumed = g.get("consumed", {})
    budget = g.get("budget", {})

    if bs != "ok":
        status = "budget-limited"
    elif not remaining:
        status = "achieved"
    else:
        status = "pursuing"

    result = {
        "goal_id": g["id"],
        "status": status,
        "criteria_met": met,
        "criteria_remaining": remaining,
        "budget_status": bs,
        "consumed": consumed,
        "budget": budget,
        "next_iter": consumed.get("iters", 0) + 1,
    }

    if status == "pursuing":
        result["continuation_prompt"] = build_continuation_prompt(g, met, remaining)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == "pursuing" else 1


if __name__ == "__main__":
    sys.exit(main())
