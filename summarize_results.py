#!/usr/bin/env python3
"""Summarize experiment logs into a markdown table."""
from __future__ import annotations

import re
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"
CONFIG_LABELS = {
    "ac": "1 ghost, random",
    "ae": "1 ghost, directional",
    "bc": "2 ghosts, random",
    "be": "2 ghosts, directional",
}

SUMMARY_PATH = RESULTS_DIR / "summary.md"

AVG_RE = re.compile(r"Average Score:\s*(-?\d+(?:\.\d+)?)")
WIN_RE = re.compile(r"Win Rate:\s*(\d+)/(\d+)\s*\(([^)]+)\)")


def parse_log(path: Path) -> dict[str, str]:
    text = path.read_text().strip()
    parts = path.stem.split("_")
    if len(parts) < 3:
        raise ValueError(f"Unexpected file name: {path.name}")
    agent = parts[0]
    label = parts[1]
    depth = parts[2]

    entry: dict[str, str] = {
        "agent": agent,
        "label": label,
        "depth": depth[1:] if depth.startswith("d") else depth,
        "config": CONFIG_LABELS.get(label, label),
        "avg": "-",
        "win": "-",
        "status": "ok",
    }

    if "RUN FAILURE" in text or not text:
        entry["status"] = "failure"
        return entry

    avg_match = AVG_RE.search(text)
    win_match = WIN_RE.search(text)

    if avg_match:
        entry["avg"] = avg_match.group(1)
    if win_match:
        wins, total, rate = win_match.groups()
        entry["win"] = f"{wins}/{total} ({rate})"
    else:
        entry["status"] = "missing-win"

    return entry


def main() -> None:
    rows = []
    for path in sorted(RESULTS_DIR.glob("*agent_*.log")):
        rows.append(parse_log(path))

    lines = ["| Agent | Config | Depth | Avg Score | Win Rate | Status |", "|-------|--------|-------|-----------|----------|--------|"]
    for row in rows:
        lines.append(
            "| {agent} | {config} | {depth} | {avg} | {win} | {status} |".format(**row)
        )

    SUMMARY_PATH.write_text("\n".join(lines))
    print(f"Wrote {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
