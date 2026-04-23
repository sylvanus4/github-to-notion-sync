"""Unified pipeline orchestrator for the video-use skill.

Chains the full workflow:
  healthcheck → transcribe_batch → pack_transcripts → [user EDL] → render → self_eval

Usage:
    python helpers/pipeline.py <project_dir> --edl <edl.json> -o <output.mp4>
    python helpers/pipeline.py <project_dir> --edl <edl.json> -o <output.mp4> --draft
    python helpers/pipeline.py <project_dir> --stage transcribe
    python helpers/pipeline.py <project_dir> --stage pack
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

HELPERS_DIR = Path(__file__).resolve().parent

STAGES = ["healthcheck", "transcribe", "pack", "render", "eval"]


def run_stage(name: str, cmd: list[str], required: bool = True) -> bool:
    print(f"\n{'=' * 60}")
    print(f"  STAGE: {name}")
    print(f"{'=' * 60}\n")
    t0 = time.time()
    result = subprocess.run(cmd)
    dt = time.time() - t0
    ok = result.returncode == 0
    status = "PASS" if ok else "FAIL"
    print(f"\n  [{status}] {name}  ({dt:.1f}s)")
    if not ok and required:
        print(f"  stage '{name}' failed — aborting pipeline", file=sys.stderr)
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description="video-use full pipeline orchestrator")
    ap.add_argument("project_dir", type=Path, help="Project root directory")
    ap.add_argument("--edl", type=Path, default=None, help="EDL JSON (required for render stage)")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Final output video path")
    ap.add_argument("--raw-dir", type=Path, default=None, help="Directory containing source videos (default: <project_dir>/raw)")
    ap.add_argument("--preview", action="store_true", help="Preview quality render")
    ap.add_argument("--draft", action="store_true", help="Draft quality render")
    ap.add_argument("--workers", type=int, default=4, help="Transcription parallel workers")
    sub_group = ap.add_mutually_exclusive_group()
    sub_group.add_argument("--build-subtitles", action="store_true", help="Build master.srt from transcripts")
    sub_group.add_argument("--no-subtitles", action="store_true", help="Skip subtitles entirely")
    ap.add_argument(
        "--stage",
        type=str,
        default=None,
        choices=STAGES,
        help="Run only a single stage instead of the full pipeline",
    )
    ap.add_argument("--skip-healthcheck", action="store_true", help="Skip the dependency check")
    ap.add_argument("--no-eval", action="store_true", help="Skip post-render evaluation")
    args = ap.parse_args()

    project_dir = args.project_dir.resolve()
    if not project_dir.is_dir():
        sys.exit(f"not a directory: {project_dir}")

    raw_dir = (args.raw_dir or project_dir / "raw").resolve()
    edit_dir = project_dir / "edit"
    edit_dir.mkdir(exist_ok=True)

    python = sys.executable

    if args.stage:
        stages = [args.stage]
    else:
        stages = list(STAGES)
        if args.skip_healthcheck:
            stages.remove("healthcheck")
        if args.no_eval:
            stages = [s for s in stages if s != "eval"]

    results: dict[str, bool] = {}

    for stage in stages:
        if stage == "healthcheck":
            ok = run_stage("healthcheck", [
                python, str(HELPERS_DIR / "healthcheck.py"), "--strict",
            ], required=True)
            results["healthcheck"] = ok
            if not ok:
                break

        elif stage == "transcribe":
            if not raw_dir.is_dir():
                print(f"  WARNING: skipping transcribe — raw directory not found: {raw_dir}", file=sys.stderr)
                results["transcribe"] = True
                continue
            ok = run_stage("transcribe", [
                python, str(HELPERS_DIR / "transcribe_batch.py"),
                str(raw_dir),
                "--edit-dir", str(edit_dir),
                "--workers", str(args.workers),
            ], required=True)
            results["transcribe"] = ok
            if not ok:
                break

        elif stage == "pack":
            transcripts_dir = edit_dir / "transcripts"
            if not transcripts_dir.is_dir() or not list(transcripts_dir.glob("*.json")):
                print("  WARNING: skipping pack — no transcripts found in edit/transcripts/", file=sys.stderr)
                results["pack"] = True
                continue
            ok = run_stage("pack", [
                python, str(HELPERS_DIR / "pack_transcripts.py"),
                "--edit-dir", str(edit_dir),
            ], required=False)
            results["pack"] = ok

        elif stage == "render":
            if not args.edl:
                print("  skipping render — no --edl provided")
                results["render"] = True
                continue
            if not args.output:
                args.output = edit_dir / "final.mp4"
            cmd = [
                python, str(HELPERS_DIR / "render.py"),
                str(args.edl),
                "-o", str(args.output),
            ]
            if args.build_subtitles:
                cmd.append("--build-subtitles")
            if args.no_subtitles:
                cmd.append("--no-subtitles")
            if args.draft:
                cmd.append("--draft")
            elif args.preview:
                cmd.append("--preview")
            ok = run_stage("render", cmd, required=True)
            results["render"] = ok
            if not ok:
                break

        elif stage == "eval":
            output_path = args.output or (edit_dir / "final.mp4")
            if not output_path.exists():
                print(f"  skipping eval — output not found: {output_path}")
                results["eval"] = True
                continue
            cmd = [
                python, str(HELPERS_DIR / "self_eval.py"),
                str(output_path),
            ]
            if args.edl:
                cmd += ["--edl", str(args.edl)]
            ok = run_stage("eval", cmd, required=False)
            results["eval"] = ok

    print(f"\n{'=' * 60}")
    print("  PIPELINE SUMMARY")
    print(f"{'=' * 60}")
    all_pass = True
    for name, ok in results.items():
        icon = "\u2705" if ok else "\u274c"
        print(f"  {icon} {name}")
        if not ok:
            all_pass = False
    status = "ALL PASS" if all_pass else "FAILED"
    print(f"\n  Result: {status}")
    print(f"{'=' * 60}\n")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
