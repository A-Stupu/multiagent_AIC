#!/usr/bin/env python3
"""Batch runner for Minimax and AlphaBeta experiments."""
from __future__ import annotations

import subprocess
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

CONFIGS = [
    {"label": "ac", "k": 1, "ghost": "RandomGhost", "description": "1 ghost, random"},
    {"label": "ae", "k": 1, "ghost": "DirectionalGhost", "description": "1 ghost, directional"},
    {"label": "bc", "k": 2, "ghost": "RandomGhost", "description": "2 ghosts, random"},
    {"label": "be", "k": 2, "ghost": "DirectionalGhost", "description": "2 ghosts, directional"},
]

AGENTS = ["MinimaxAgent", "AlphaBetaAgent"]
DEPTHS = [2, 3, 4]
MAX_DURATION = 180  # seconds, per lab requirement
NUM_GAMES = 10
LAYOUT = "smallClassic"


def run_case(agent: str, depth: int, config: dict[str, str | int]) -> None:
    label = f"{agent.lower()}_{config['label']}_d{depth}"
    log_path = RESULTS_DIR / f"{label}.log"

    cmd = [
        "python3",
        "pacman_AIC.py",
        "-p",
        agent,
        "-a",
        f"depth={depth}",
        "-l",
        LAYOUT,
        "-k",
        str(config["k"]),
        "-g",
        config["ghost"],
        "-n",
        str(NUM_GAMES),
        "-q",
    ]

    print(f"Running {label} ...", flush=True)
    try:
        completed = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            timeout=MAX_DURATION,
            check=False,
        )
        output = completed.stdout + ("\n" + completed.stderr if completed.stderr else "")
        if completed.returncode != 0:
            output += f"\nRUN FAILURE EXIT {completed.returncode}\n"
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        output = stdout + ("\n" + stderr if stderr else "")
        output += "\nRUN FAILURE EXIT TIMEOUT\n"

    log_path.write_text(output)


if __name__ == "__main__":
    for agent in AGENTS:
        for config in CONFIGS:
            for depth in DEPTHS:
                run_case(agent, depth, config)
