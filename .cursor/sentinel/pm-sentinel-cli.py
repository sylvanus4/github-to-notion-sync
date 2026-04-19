#!/usr/bin/env python3
"""PM Sentinel CLI -- YAML state DB + validation gate for autonomous PM loop.

Usage:
    python pm-sentinel-cli.py status
    python pm-sentinel-cli.py next
    python pm-sentinel-cli.py start <mission-id>
    python pm-sentinel-cli.py complete-phase <mission-id> <phase-id> --evidence '{"key":"value"}'
    python pm-sentinel-cli.py complete <mission-id> --output <path>
    python pm-sentinel-cli.py fail <mission-id> --reason "description"
    python pm-sentinel-cli.py add-mission <type> [--priority N]
    python pm-sentinel-cli.py heartbeat
    python pm-sentinel-cli.py report
    python pm-sentinel-cli.py tips
    python pm-sentinel-cli.py pause
    python pm-sentinel-cli.py resume
    python pm-sentinel-cli.py seed [--types type1,type2,...]
"""
import argparse
import copy
import json
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

SENTINEL_DIR = Path(__file__).parent
STATE_FILE = SENTINEL_DIR / "sentinel-state.yaml"
TEMPLATES_FILE = SENTINEL_DIR / "mission-templates.yaml"
LOG_FILE = SENTINEL_DIR / "mission-log.yaml"
TIPS_FILE = SENTINEL_DIR / "sentinel-tips.yaml"

VALID_STATUSES = {"pending", "in_progress", "blocked", "completed", "skipped"}
VALID_SENTINEL_STATUSES = {"running", "paused", "completed_cycle"}


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def save_yaml(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def next_mission_id(state: dict) -> str:
    existing = [m["id"] for m in state.get("missions", [])]
    nums = []
    for mid in existing:
        try:
            nums.append(int(mid.split("-")[1]))
        except (IndexError, ValueError):
            pass
    next_num = max(nums, default=0) + 1
    return f"M-{next_num:03d}"


def get_mission(state: dict, mission_id: str) -> dict | None:
    for m in state.get("missions", []):
        if m["id"] == mission_id:
            return m
    return None


def get_phase(state: dict, mission_id: str, phase_id: str) -> dict | None:
    phases = state.get("phases", {}).get(mission_id, [])
    for p in phases:
        if p["id"] == phase_id:
            return p
    return None


def all_deps_completed(state: dict, dep_ids: list, context_type: str = "mission") -> tuple[bool, list]:
    """Check if all dependencies are completed. Returns (ok, missing_list)."""
    missing = []
    if context_type == "mission":
        for dep_id in dep_ids:
            m = get_mission(state, dep_id)
            if not m or m["status"] != "completed":
                missing.append(dep_id)
    elif context_type == "phase":
        mission_id = dep_ids[0] if dep_ids else None
        phase_deps = dep_ids[1] if len(dep_ids) > 1 else []
        phases = state.get("phases", {}).get(mission_id, [])
        phase_map = {p["id"]: p for p in phases}
        for dep_id in phase_deps:
            p = phase_map.get(dep_id)
            if not p or p["status"] != "completed":
                missing.append(dep_id)
    return len(missing) == 0, missing


def resolve_next_action(state: dict) -> dict:
    """Determine the next action based on YAML state. Returns action descriptor."""
    sentinel = state.get("sentinel", {})
    if sentinel.get("status") == "paused":
        return {"action": "paused", "message": "Sentinel is paused. Run 'resume' to continue."}

    in_progress = [m for m in state.get("missions", []) if m["status"] == "in_progress"]
    if in_progress:
        mission = in_progress[0]
        phases = state.get("phases", {}).get(mission["id"], [])
        for phase in sorted(phases, key=lambda p: p["order"]):
            if phase["status"] == "pending":
                deps = phase.get("depends_on", [])
                phase_map = {p["id"]: p for p in phases}
                deps_ok = all(phase_map.get(d, {}).get("status") == "completed" for d in deps)
                if deps_ok:
                    return {
                        "action": "execute_phase",
                        "mission_id": mission["id"],
                        "mission_type": mission["type"],
                        "phase_id": phase["id"],
                        "phase_name": phase["name"],
                        "evidence_required": phase.get("evidence_required", []),
                        "skill": phase.get("skill", "general"),
                        "message": f"Execute phase {phase['id']}: {phase['name']}",
                    }
        all_done = all(p["status"] == "completed" for p in phases)
        if all_done:
            return {
                "action": "complete_mission",
                "mission_id": mission["id"],
                "message": f"All phases complete for {mission['id']}. Run: complete {mission['id']} --output <report_path>",
            }
        return {
            "action": "blocked",
            "mission_id": mission["id"],
            "message": f"Mission {mission['id']} has incomplete phases with unmet dependencies.",
        }

    pending = [m for m in state.get("missions", []) if m["status"] == "pending"]
    if not pending:
        return {"action": "idle", "message": "No pending missions. Run 'seed' to generate missions or 'add-mission' to add one."}

    pending.sort(key=lambda m: (m.get("priority", 5), m.get("created_at", "")))
    best = pending[0]
    deps = best.get("dependencies", [])
    deps_ok, missing = all_deps_completed(state, deps)
    if deps_ok:
        return {
            "action": "start_mission",
            "mission_id": best["id"],
            "mission_type": best["type"],
            "priority": best.get("priority", 5),
            "message": f"Start mission {best['id']} ({best['type']}). Run: start {best['id']}",
        }
    return {
        "action": "blocked",
        "mission_id": best["id"],
        "message": f"Mission {best['id']} blocked on dependencies: {missing}",
    }


def get_warnings(state: dict) -> list[str]:
    warnings = []
    for m in state.get("missions", []):
        if m.get("error_count", 0) >= m.get("max_retries", 2):
            warnings.append(f"Mission {m['id']} ({m['type']}) has exhausted retries ({m['error_count']}/{m['max_retries']})")
        if m["status"] == "in_progress":
            started = m.get("started_at")
            if started:
                try:
                    start_dt = datetime.fromisoformat(started)
                    elapsed = datetime.now(timezone.utc) - start_dt
                    if elapsed > timedelta(hours=2):
                        warnings.append(f"Mission {m['id']} running for {elapsed.total_seconds()/3600:.1f}h (stale?)")
                except (ValueError, TypeError):
                    pass
    sentinel = state.get("sentinel", {})
    if sentinel.get("status") == "paused":
        warnings.append("Sentinel is PAUSED. No missions will execute until resumed.")
    if not state.get("missions"):
        warnings.append("No missions in queue. Run 'seed' to populate.")
    return warnings


def render_reminder(state: dict, tips_data: dict) -> str:
    action = resolve_next_action(state)
    warnings = get_warnings(state)
    next_desc = action.get("message", "No pending actions")
    warn_text = warnings[0] if warnings else "No warnings"

    general_tips = tips_data.get("general", ["Keep evidence specific and verifiable."])
    mission_type = action.get("mission_type", "")
    phase_tips = tips_data.get(mission_type.replace("-", "_"), [])
    all_tips = phase_tips + general_tips
    random.shuffle(all_tips)
    tip1 = all_tips[0] if len(all_tips) > 0 else "Stay focused."
    tip2 = all_tips[1] if len(all_tips) > 1 else "Check your evidence."

    lines = [
        "",
        "═══ SENTINEL REMINDER ═══",
        f"NEXT: {next_desc}",
        f"WARN: {warn_text}",
        f"TIP1: {tip1}",
        f"TIP2: {tip2}",
        "══════════════════════════",
    ]
    return "\n".join(lines)


def cmd_status(state: dict, tips: dict) -> None:
    sentinel = state.get("sentinel", {})
    missions = state.get("missions", [])
    counts = {}
    for m in missions:
        s = m["status"]
        counts[s] = counts.get(s, 0) + 1

    print(f"Sentinel Status: {sentinel.get('status', 'unknown')}")
    print(f"Current Cycle:   {sentinel.get('current_cycle', 0)}")
    print(f"Last Heartbeat:  {sentinel.get('last_heartbeat', 'never')}")
    print(f"Next Heartbeat:  {sentinel.get('next_heartbeat', 'not scheduled')}")
    print(f"Total Missions:  {len(missions)}")
    for s, c in sorted(counts.items()):
        print(f"  {s}: {c}")
    print()

    in_progress = [m for m in missions if m["status"] == "in_progress"]
    if in_progress:
        m = in_progress[0]
        phases = state.get("phases", {}).get(m["id"], [])
        done = sum(1 for p in phases if p["status"] == "completed")
        total = len(phases)
        print(f"Active Mission: {m['id']} ({m['type']})")
        print(f"  Progress: {done}/{total} phases completed")
        for p in sorted(phases, key=lambda x: x["order"]):
            marker = "✓" if p["status"] == "completed" else "○" if p["status"] == "pending" else "→"
            print(f"  {marker} {p['id']}: {p['name']} [{p['status']}]")
        print()

    action = resolve_next_action(state)
    print(f"Next Action: {action['action']}")
    print(f"  {action['message']}")
    print(render_reminder(state, tips))


def cmd_next(state: dict, tips: dict) -> None:
    action = resolve_next_action(state)
    print(json.dumps(action, indent=2, ensure_ascii=False))
    print(render_reminder(state, tips))


def cmd_start(state: dict, tips: dict, mission_id: str) -> None:
    mission = get_mission(state, mission_id)
    if not mission:
        print(f"ERROR: Mission {mission_id} not found.", file=sys.stderr)
        print(f"REMEDIATION: Run 'status' to see available missions.", file=sys.stderr)
        sys.exit(1)

    if mission["status"] != "pending":
        print(f"ERROR: Mission {mission_id} status is '{mission['status']}', expected 'pending'.", file=sys.stderr)
        print(f"REMEDIATION: Only pending missions can be started.", file=sys.stderr)
        sys.exit(1)

    deps = mission.get("dependencies", [])
    deps_ok, missing = all_deps_completed(state, deps)
    if not deps_ok:
        print(f"ERROR: Dependencies not met for {mission_id}: {missing}", file=sys.stderr)
        print(f"REMEDIATION: Complete missions {missing} first.", file=sys.stderr)
        sys.exit(1)

    in_progress = [m for m in state.get("missions", []) if m["status"] == "in_progress"]
    if in_progress:
        print(f"ERROR: Mission {in_progress[0]['id']} is already in_progress.", file=sys.stderr)
        print(f"REMEDIATION: Complete or fail {in_progress[0]['id']} before starting a new mission.", file=sys.stderr)
        sys.exit(1)

    mission["status"] = "in_progress"
    mission["started_at"] = now_iso()
    save_yaml(STATE_FILE, state)
    print(f"OK: Mission {mission_id} ({mission['type']}) started.")
    phases = state.get("phases", {}).get(mission_id, [])
    if phases:
        first = sorted(phases, key=lambda p: p["order"])[0]
        print(f"First phase: {first['id']} - {first['name']}")
        print(f"Evidence required: {first.get('evidence_required', [])}")
    print(render_reminder(state, tips))


def cmd_complete_phase(state: dict, tips: dict, mission_id: str, phase_id: str, evidence_json: str) -> None:
    mission = get_mission(state, mission_id)
    if not mission:
        print(f"ERROR: Mission {mission_id} not found.", file=sys.stderr)
        sys.exit(1)
    if mission["status"] != "in_progress":
        print(f"ERROR: Mission {mission_id} is not in_progress (status: {mission['status']}).", file=sys.stderr)
        sys.exit(1)

    phase = get_phase(state, mission_id, phase_id)
    if not phase:
        print(f"ERROR: Phase {phase_id} not found in mission {mission_id}.", file=sys.stderr)
        phases = state.get("phases", {}).get(mission_id, [])
        valid_ids = [p["id"] for p in phases]
        print(f"REMEDIATION: Valid phase IDs: {valid_ids}", file=sys.stderr)
        sys.exit(1)

    if phase["status"] == "completed":
        print(f"WARNING: Phase {phase_id} is already completed. Skipping.")
        print(render_reminder(state, tips))
        return

    deps = phase.get("depends_on", [])
    if deps:
        phases_list = state.get("phases", {}).get(mission_id, [])
        phase_map = {p["id"]: p for p in phases_list}
        for dep in deps:
            dep_phase = phase_map.get(dep)
            if not dep_phase or dep_phase["status"] != "completed":
                print(f"ERROR: Phase dependency {dep} is not completed.", file=sys.stderr)
                print(f"REMEDIATION: Complete phase {dep} before {phase_id}.", file=sys.stderr)
                sys.exit(1)

    try:
        evidence = json.loads(evidence_json)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON evidence: {e}", file=sys.stderr)
        print(f"REMEDIATION: Provide valid JSON, e.g. '{{\"key\": \"value\"}}'", file=sys.stderr)
        sys.exit(1)

    required = phase.get("evidence_required", [])
    missing = [r for r in required if r not in evidence]
    if missing:
        print(f"ERROR: Missing required evidence fields: {missing}", file=sys.stderr)
        print(f"REMEDIATION: Provide all required fields: {required}", file=sys.stderr)
        print(f"  You provided: {list(evidence.keys())}", file=sys.stderr)
        sys.exit(1)

    empty = [k for k in required if k in evidence and (evidence[k] is None or evidence[k] == "" or evidence[k] == [])]
    if empty:
        print(f"ERROR: Evidence fields cannot be empty/null: {empty}", file=sys.stderr)
        print(f"REMEDIATION: Provide actual values for: {empty}", file=sys.stderr)
        sys.exit(1)

    phase["status"] = "completed"
    phase["evidence_provided"] = evidence
    phase["completed_at"] = now_iso()
    mission["evidence"].append({
        "phase_id": phase_id,
        "evidence": evidence,
        "timestamp": now_iso(),
    })
    save_yaml(STATE_FILE, state)

    phases_list = state.get("phases", {}).get(mission_id, [])
    done = sum(1 for p in phases_list if p["status"] == "completed")
    total = len(phases_list)
    print(f"OK: Phase {phase_id} completed with evidence ({done}/{total} phases done).")
    if done == total:
        print(f"All phases complete. Run: complete {mission_id} --output <report_path>")
    print(render_reminder(state, tips))


def cmd_complete(state: dict, tips: dict, mission_id: str, output_path: str) -> None:
    mission = get_mission(state, mission_id)
    if not mission:
        print(f"ERROR: Mission {mission_id} not found.", file=sys.stderr)
        sys.exit(1)
    if mission["status"] != "in_progress":
        print(f"ERROR: Mission {mission_id} is not in_progress.", file=sys.stderr)
        sys.exit(1)

    phases = state.get("phases", {}).get(mission_id, [])
    incomplete = [p for p in phases if p["status"] != "completed"]
    if incomplete:
        names = [f"{p['id']}({p['name']})" for p in incomplete]
        print(f"ERROR: Cannot complete mission with {len(incomplete)} incomplete phases: {names}", file=sys.stderr)
        print(f"REMEDIATION: Complete all phases first using 'complete-phase'.", file=sys.stderr)
        sys.exit(1)

    mission["status"] = "completed"
    mission["completed_at"] = now_iso()
    mission["output"] = output_path

    log = load_yaml(LOG_FILE)
    log.setdefault("completed_missions", []).append({
        "id": mission["id"],
        "type": mission["type"],
        "started_at": mission.get("started_at"),
        "completed_at": mission["completed_at"],
        "output": output_path,
        "evidence_count": len(mission.get("evidence", [])),
        "cycle": state.get("sentinel", {}).get("current_cycle", 0),
    })
    metrics = log.setdefault("metrics", {})
    metrics["total_missions_completed"] = metrics.get("total_missions_completed", 0) + 1
    metrics["last_updated"] = now_iso()
    save_yaml(LOG_FILE, log)
    save_yaml(STATE_FILE, state)

    print(f"OK: Mission {mission_id} ({mission['type']}) completed.")
    print(f"Output: {output_path}")
    print(render_reminder(state, tips))


def cmd_fail(state: dict, tips: dict, mission_id: str, reason: str) -> None:
    mission = get_mission(state, mission_id)
    if not mission:
        print(f"ERROR: Mission {mission_id} not found.", file=sys.stderr)
        sys.exit(1)

    mission["error_count"] = mission.get("error_count", 0) + 1
    mission["notes"] = f"[FAIL {now_iso()}] {reason}"

    if mission["error_count"] >= mission.get("max_retries", 2):
        mission["status"] = "blocked"
        print(f"WARNING: Mission {mission_id} blocked after {mission['error_count']} failures.")

        log = load_yaml(LOG_FILE)
        metrics = log.setdefault("metrics", {})
        metrics["total_missions_failed"] = metrics.get("total_missions_failed", 0) + 1
        metrics["last_updated"] = now_iso()
        save_yaml(LOG_FILE, log)
    else:
        mission["status"] = "pending"
        print(f"OK: Mission {mission_id} failed (attempt {mission['error_count']}/{mission.get('max_retries', 2)}). Reset to pending for retry.")
        phases = state.get("phases", {}).get(mission_id, [])
        for p in phases:
            if p["status"] != "completed":
                p["status"] = "pending"
                p["evidence_provided"] = {}

    save_yaml(STATE_FILE, state)
    print(f"Reason: {reason}")
    print(render_reminder(state, tips))


def cmd_add_mission(state: dict, tips: dict, mission_type: str, priority: int) -> None:
    templates = load_yaml(TEMPLATES_FILE)
    template = templates.get("templates", {}).get(mission_type)
    if not template:
        valid = list(templates.get("templates", {}).keys())
        print(f"ERROR: Unknown mission type '{mission_type}'.", file=sys.stderr)
        print(f"REMEDIATION: Valid types: {valid}", file=sys.stderr)
        sys.exit(1)

    mid = next_mission_id(state)
    mission = {
        "id": mid,
        "type": mission_type,
        "priority": priority or template.get("priority", 3),
        "status": "pending",
        "phase": None,
        "created_at": now_iso(),
        "started_at": None,
        "completed_at": None,
        "evidence": [],
        "dependencies": [],
        "output": None,
        "error_count": 0,
        "max_retries": 2,
        "notes": "",
    }
    state.setdefault("missions", []).append(mission)

    phases = []
    for pt in template.get("phases", []):
        phase = {
            "id": f"{mid}-{pt['id']}",
            "name": pt["name"],
            "status": "pending",
            "evidence_required": pt.get("evidence_required", []),
            "evidence_provided": {},
            "order": pt["order"],
            "skill": pt.get("skill", "general"),
        }
        if pt.get("depends_on"):
            phase["depends_on"] = [f"{mid}-{d}" for d in pt["depends_on"]]
        phases.append(phase)
    state.setdefault("phases", {})[mid] = phases

    save_yaml(STATE_FILE, state)
    print(f"OK: Mission {mid} ({mission_type}) added with {len(phases)} phases, priority={mission['priority']}.")
    print(render_reminder(state, tips))


def cmd_seed(state: dict, tips: dict, types: list[str] | None = None) -> None:
    templates = load_yaml(TEMPLATES_FILE)
    all_types = list(templates.get("templates", {}).keys())
    if types:
        invalid = [t for t in types if t not in all_types]
        if invalid:
            print(f"ERROR: Unknown types: {invalid}. Valid: {all_types}", file=sys.stderr)
            sys.exit(1)
        seed_types = types
    else:
        seed_types = all_types

    existing_types = {m["type"] for m in state.get("missions", []) if m["status"] in ("pending", "in_progress")}
    added = 0
    for mt in seed_types:
        if mt in existing_types:
            print(f"SKIP: {mt} already has a pending/in_progress mission.")
            continue
        template = templates["templates"][mt]
        mid = next_mission_id(state)
        mission = {
            "id": mid,
            "type": mt,
            "priority": template.get("priority", 3),
            "status": "pending",
            "phase": None,
            "created_at": now_iso(),
            "started_at": None,
            "completed_at": None,
            "evidence": [],
            "dependencies": [],
            "output": None,
            "error_count": 0,
            "max_retries": 2,
            "notes": "",
        }
        state.setdefault("missions", []).append(mission)

        phases = []
        for pt in template.get("phases", []):
            phase = {
                "id": f"{mid}-{pt['id']}",
                "name": pt["name"],
                "status": "pending",
                "evidence_required": pt.get("evidence_required", []),
                "evidence_provided": {},
                "order": pt["order"],
                "skill": pt.get("skill", "general"),
            }
            if pt.get("depends_on"):
                phase["depends_on"] = [f"{mid}-{d}" for d in pt["depends_on"]]
            phases.append(phase)
        state.setdefault("phases", {})[mid] = phases
        added += 1
        print(f"  Added: {mid} ({mt}), priority={mission['priority']}, phases={len(phases)}")

    save_yaml(STATE_FILE, state)
    print(f"\nOK: Seeded {added} missions ({len(seed_types) - added} skipped as duplicates).")
    print(render_reminder(state, tips))


def cmd_heartbeat(state: dict, tips: dict) -> None:
    sentinel = state.get("sentinel", {})
    if sentinel.get("status") == "paused":
        print("Sentinel is PAUSED. Run 'resume' to enable heartbeat.")
        print(render_reminder(state, tips))
        return

    sentinel["last_heartbeat"] = now_iso()
    sentinel["next_heartbeat"] = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    sentinel["current_cycle"] = sentinel.get("current_cycle", 0) + 1
    state["sentinel"] = sentinel
    save_yaml(STATE_FILE, state)

    print(f"=== HEARTBEAT #{sentinel['current_cycle']} @ {sentinel['last_heartbeat']} ===")
    print()
    action = resolve_next_action(state)
    print(json.dumps(action, indent=2, ensure_ascii=False))
    print(render_reminder(state, tips))


def cmd_report(state: dict, tips: dict) -> None:
    log = load_yaml(LOG_FILE)
    metrics = log.get("metrics", {})
    completed = log.get("completed_missions", [])

    print("=== PM SENTINEL REPORT ===")
    print(f"Total Completed: {metrics.get('total_missions_completed', 0)}")
    print(f"Total Failed:    {metrics.get('total_missions_failed', 0)}")
    print(f"Total Cycles:    {state.get('sentinel', {}).get('current_cycle', 0)}")
    print(f"Evidence Rejections: {metrics.get('evidence_rejection_count', 0)}")
    print()

    if completed:
        print("Recent Completed Missions:")
        for m in completed[-10:]:
            print(f"  {m['id']} ({m['type']}) - completed {m.get('completed_at', '?')}")
    else:
        print("No completed missions yet.")

    by_type = {}
    for m in completed:
        t = m["type"]
        by_type[t] = by_type.get(t, 0) + 1
    if by_type:
        print("\nCompletions by Type:")
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")

    print(render_reminder(state, tips))


def cmd_pause(state: dict, tips: dict) -> None:
    state.setdefault("sentinel", {})["status"] = "paused"
    save_yaml(STATE_FILE, state)
    print("OK: Sentinel paused. No missions will execute until resumed.")
    print(render_reminder(state, tips))


def cmd_resume(state: dict, tips: dict) -> None:
    state.setdefault("sentinel", {})["status"] = "running"
    save_yaml(STATE_FILE, state)
    print("OK: Sentinel resumed. Missions will execute on next heartbeat.")
    print(render_reminder(state, tips))


def cmd_tips(state: dict, tips: dict) -> None:
    print(render_reminder(state, tips))


def main():
    parser = argparse.ArgumentParser(description="PM Sentinel CLI -- YAML state DB + validation gate")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show current sentinel state")
    subparsers.add_parser("next", help="Determine and return next action")

    start_p = subparsers.add_parser("start", help="Start a mission")
    start_p.add_argument("mission_id")

    cp_p = subparsers.add_parser("complete-phase", help="Complete a phase with evidence")
    cp_p.add_argument("mission_id")
    cp_p.add_argument("phase_id")
    cp_p.add_argument("--evidence", required=True, help="JSON evidence object")

    comp_p = subparsers.add_parser("complete", help="Complete a mission")
    comp_p.add_argument("mission_id")
    comp_p.add_argument("--output", required=True, help="Path to output artifact")

    fail_p = subparsers.add_parser("fail", help="Mark a mission as failed")
    fail_p.add_argument("mission_id")
    fail_p.add_argument("--reason", required=True, help="Failure reason")

    add_p = subparsers.add_parser("add-mission", help="Add a new mission")
    add_p.add_argument("type", help="Mission type")
    add_p.add_argument("--priority", type=int, default=0, help="Priority (1=critical, 5=low)")

    subparsers.add_parser("heartbeat", help="Run a heartbeat cycle")
    subparsers.add_parser("report", help="Generate cycle summary report")
    subparsers.add_parser("tips", help="Output reminder block")
    subparsers.add_parser("pause", help="Pause the sentinel")
    subparsers.add_parser("resume", help="Resume the sentinel")

    seed_p = subparsers.add_parser("seed", help="Seed missions from templates")
    seed_p.add_argument("--types", help="Comma-separated mission types to seed")

    args = parser.parse_args()
    state = load_yaml(STATE_FILE)
    tips = load_yaml(TIPS_FILE)

    dispatch = {
        "status": lambda: cmd_status(state, tips),
        "next": lambda: cmd_next(state, tips),
        "start": lambda: cmd_start(state, tips, args.mission_id),
        "complete-phase": lambda: cmd_complete_phase(state, tips, args.mission_id, args.phase_id, args.evidence),
        "complete": lambda: cmd_complete(state, tips, args.mission_id, args.output),
        "fail": lambda: cmd_fail(state, tips, args.mission_id, args.reason),
        "add-mission": lambda: cmd_add_mission(state, tips, args.type, args.priority),
        "heartbeat": lambda: cmd_heartbeat(state, tips),
        "report": lambda: cmd_report(state, tips),
        "tips": lambda: cmd_tips(state, tips),
        "pause": lambda: cmd_pause(state, tips),
        "resume": lambda: cmd_resume(state, tips),
        "seed": lambda: cmd_seed(state, tips, args.types.split(",") if args.types else None),
    }
    dispatch[args.command]()


if __name__ == "__main__":
    main()
