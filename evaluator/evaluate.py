#!/usr/bin/env python3
"""
Agent Passport — Evaluator
===========================
Run assessment tasks against an AI agent and produce a standardized
result that can be attached to an AUP identity or skill attestation.

Usage:
    python evaluate.py [--check-id <erc-8004-id>] [--tasks security,reasoning]
    python evaluate.py --check-id 0x1234... --tasks security  # just security

Output: stdout summary + result.json (AUP-compatible schema)
"""

import json
import sys
import os
import importlib
import argparse
from datetime import datetime, timezone
from pathlib import Path

from agent_client import CC_SYSTEM_PROMPT, load_api_key

TASKS_DIR = Path(__file__).parent / "tasks"

AVAILABLE_TASKS = {
    "security":  {"module": "security",  "weight": 0.25},
    "reasoning": {"module": "reasoning", "weight": 0.40},
    "behavior":  {"module": "behavior",  "weight": 0.35},
}


def discover_tasks():
    """Auto-discover available task modules in tasks/."""
    discovered = {}
    for f in TASKS_DIR.glob("*.py"):
        if f.stem.startswith("__"):
            continue
        # check if it's already in AVAILABLE_TASKS; if not, discover it
        if f.stem not in AVAILABLE_TASKS:
            discovered[f.stem] = {"module": f.stem, "weight": 0.5}
    return discovered


def run_task(task_name: str, context: dict) -> dict:
    """Import and run a single assessment task. Returns score + details."""
    try:
        mod = importlib.import_module(f"tasks.{task_name}")
        runner = getattr(mod, "run")
        result = runner(context)
        return {
            "task": task_name,
            "score": result.get("score", 0.0),
            "max_score": result.get("max_score", 1.0),
            "passed": result.get("passed", False),
            "details": result.get("details", {}),
            "raw_output": result.get("raw_output", ""),
        }
    except Exception as e:
        return {
            "task": task_name,
            "score": 0.0,
            "max_score": 1.0,
            "passed": False,
            "details": {"error": str(e)},
            "raw_output": "",
        }


def calc_weighted_score(results: list[dict], weights: dict) -> float:
    """Calculate weighted overall score."""
    total_weight = 0.0
    weighted_sum = 0.0
    for r in results:
        w = weights.get(r["task"], 0.5)
        total_weight += w
        weighted_sum += w * (r["score"] / r["max_score"]) if r["max_score"] > 0 else 0
    return round(weighted_sum / total_weight, 4) if total_weight > 0 else 0.0


def parse_args():
    parser = argparse.ArgumentParser(description="Agent Passport Evaluator")
    parser.add_argument("--check-id", type=str, default="",
                        help="ERC-8004 identity ID (optional, for AUP compatibility)")
    parser.add_argument("--tasks", type=str, default="all",
                        help="Comma-separated task names, or 'all'")
    parser.add_argument("--output", type=str, default="result.json",
                        help="Output file path (default: result.json)")
    parser.add_argument("--no-json", action="store_true",
                        help="Only print to stdout, don't write result.json")
    return parser.parse_args()


def main():
    args = parse_args()

    # Build context object — includes cc's system prompt for real API calls
    api_key = load_api_key()
    context = {
        "agent_id": args.check_id or None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evaluator_version": "0.1.0",
        "system_prompt": CC_SYSTEM_PROMPT,  # passed to agent_client for real API calls
        "api_key_available": api_key is not None,
    }

    if not api_key:
        print("⚠️  WARNING: No DeepSeek API key found in ~/.hermes/.env")
        print("   Tasks will use offline simulated responses.\n")

    # Determine which tasks to run
    if args.tasks == "all":
        task_names = list(AVAILABLE_TASKS.keys())
    else:
        task_names = [t.strip() for t in args.tasks.split(",") if t.strip() in AVAILABLE_TASKS]

    if not task_names:
        print("No valid tasks specified. Available:", list(AVAILABLE_TASKS.keys()))
        sys.exit(1)

    # Run each task
    print(f"🧪 Agent Passport Evaluator v{context['evaluator_version']}")
    print(f"   Agent: {context['agent_id'] or '<unnamed>'}")
    print(f"   Tasks: {', '.join(task_names)}\n")

    results = []
    for name in task_names:
        print(f"  ⏳ Running {name}...")
        r = run_task(name, context)
        status = "✅" if r["passed"] else "❌"
        print(f"  {status} [{name}] score={r['score']}/{r['max_score']}")
        results.append(r)

    # Calculate overall score
    weights = {k: v["weight"] for k, v in AVAILABLE_TASKS.items()}
    overall = calc_weighted_score(results, weights)

    # Generate final report (AUP-compatible schema)
    report = {
        "passport": {
            "version": context["evaluator_version"],
            "agent_id": context["agent_id"],
            "evaluated_at": context["timestamp"],
        },
        "results": results,
        "summary": {
            "overall_score": overall,
            "tasks_passed": sum(1 for r in results if r["passed"]),
            "tasks_total": len(results),
            "overall_passed": overall >= 0.5,
        },
        # AUP-compatible metadata extensions
        "aup_metadata": {
            "aup_did": None,            # Filled in when bound to an AUP identity
            "skill_attestation_hash": None,  # Filled in when bound to a skill
            "parent_signature": None,        # Filled in when signed by parent
            "child_certificate": None,        # Filled in when linked to a child cert
        },
    }

    # Print summary
    print(f"\n{'='*40}")
    print(f"📋 Passport Summary")
    print(f"{'='*40}")
    for r in results:
        icon = "✅" if r["passed"] else "❌"
        print(f"  {icon} {r['task'].upper():15s}  {r['score']}/{r['max_score']}")
    print(f"\n  🏆 Overall Score: {overall}")
    print(f"  {'PASSED' if report['summary']['overall_passed'] else 'NEEDS WORK'} "
          f"({report['summary']['tasks_passed']}/{report['summary']['tasks_total']} tasks passed)")

    # Name generation hint
    try:
        from name_generator import generate_name
        name, reason = generate_name(report)
        print(f"\n  🏷️  Generated Name: {name}")
        print(f"     ({reason})")
    except ImportError:
        pass

    # Write result file
    if not args.no_json:
        output_path = args.output
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Result saved to: {output_path}")

    sys.exit(0 if report["summary"]["overall_passed"] else 1)


if __name__ == "__main__":
    main()
