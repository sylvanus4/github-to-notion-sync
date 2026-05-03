"""
Smoke-test calibration mini-builder for Qwen3-30B-A3B NVFP4 PTQ.

Target: 400 samples (100 each from C4-en, wikitext, mteb-ko, synthetic tool-call).
Output: calib_mini.jsonl  (one JSON per line: {"text": "..."})

Smoke-test sizing — full PTQ should use 8.6K samples (Thaki internal).
"""
import json
import os
import random
from pathlib import Path

OUT = Path(os.environ.get("CALIB_OUT", str(Path(__file__).parent.parent / "calib_mini.jsonl")))
SEED = 1337
N_PER_SOURCE = int(os.environ.get("CALIB_N_PER_SOURCE", "100"))

random.seed(SEED)


def fetch_c4(n):
    from datasets import load_dataset
    ds = load_dataset("allenai/c4", "en", split="train", streaming=True)
    out = []
    for ex in ds:
        t = (ex.get("text") or "").strip()
        if 200 <= len(t) <= 2000:
            out.append(t)
        if len(out) >= n:
            break
    return out


def fetch_wikitext(n):
    from datasets import load_dataset
    ds = load_dataset("wikitext", "wikitext-103-v1", split="train", streaming=True)
    out = []
    for ex in ds:
        t = (ex.get("text") or "").strip()
        if 200 <= len(t) <= 2000:
            out.append(t)
        if len(out) >= n:
            break
    return out


def fetch_korean(n):
    """Korean instruction-tuning text. KoAlpaca v1.1a is public + ungated."""
    from datasets import load_dataset
    ds = load_dataset("beomi/KoAlpaca-v1.1a", split="train", streaming=True)
    out = []
    for ex in ds:
        instr = (ex.get("instruction") or "").strip()
        output = (ex.get("output") or "").strip()
        t = (instr + "\n\n" + output).strip() if output else instr
        if 100 <= len(t) <= 2000:
            out.append(t)
        if len(out) >= n:
            break
    return out


def synth_tool_call(n):
    """Synthesize tool-call style JSON prompts. Shape mirrors Qwen3 template."""
    tools = [
        ("get_weather", ["city", "unit"]),
        ("search_web", ["query", "limit"]),
        ("send_email", ["to", "subject", "body"]),
        ("calculate", ["expression"]),
        ("get_stock_price", ["symbol"]),
        ("translate", ["text", "target_lang"]),
        ("create_calendar_event", ["title", "start", "end"]),
        ("read_file", ["path"]),
    ]
    cities = ["Seoul", "Riyadh", "Tokyo", "Dubai", "London", "New York"]
    units = ["celsius", "fahrenheit"]
    out = []
    for _ in range(n):
        name, params = random.choice(tools)
        if name == "get_weather":
            args = {"city": random.choice(cities), "unit": random.choice(units)}
        elif name == "search_web":
            args = {"query": "thaki cloud serverless", "limit": random.randint(3, 10)}
        elif name == "send_email":
            args = {"to": "team@thakicloud.co.kr", "subject": "Update", "body": "Daily standup notes."}
        elif name == "calculate":
            args = {"expression": f"{random.randint(1,99)} * {random.randint(1,99)}"}
        elif name == "get_stock_price":
            args = {"symbol": random.choice(["NVDA", "AAPL", "TSLA", "MSFT"])}
        elif name == "translate":
            args = {"text": "Hello world", "target_lang": random.choice(["ko", "ar", "ja"])}
        elif name == "create_calendar_event":
            args = {"title": "Sync", "start": "2026-05-02T09:00:00", "end": "2026-05-02T10:00:00"}
        else:
            args = {"path": "/etc/hostname"}
        prompt = (
            "User: " + random.choice([
                "What's the weather like?",
                "Search this for me.",
                "Send a quick note.",
                "Compute this please.",
                "Fetch the price.",
                "Translate this.",
                "Book a meeting.",
                "Read this file.",
            ])
            + "\nAssistant: "
            + json.dumps({"tool": name, "arguments": args}, ensure_ascii=False)
        )
        out.append(prompt)
    return out


def main():
    sources = {
        "c4": fetch_c4,
        "wikitext": fetch_wikitext,
        "korean": fetch_korean,
        "tool-call": synth_tool_call,
    }
    total = 0
    with OUT.open("w", encoding="utf-8") as f:
        for src, fn in sources.items():
            print(f"[{src}] fetching {N_PER_SOURCE} samples...", flush=True)
            try:
                samples = fn(N_PER_SOURCE)
            except Exception as e:
                print(f"  WARN: {src} failed ({e}); skipping", flush=True)
                continue
            for t in samples:
                f.write(json.dumps({"text": t, "source": src}, ensure_ascii=False) + "\n")
                total += 1
            print(f"  -> wrote {len(samples)}", flush=True)
    print(f"DONE: {total} samples -> {OUT}")


if __name__ == "__main__":
    main()
