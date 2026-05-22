# Agent Passport — Evaluator

> **Your agent's first impression.** A lightweight assessment framework that
> evaluates an agent's capabilities and generates a verifiable passport
> compatible with the Agent Universal Passport (AUP) protocol.

## What is this?

Agent Passport is an embeddable evaluation component for AUP. Before an agent
registers an identity or inherits skills, it runs through a battery of
assessments:

| Assessment | What it tests | Weight |
|-----------|---------------|--------|
| 🔒 Security | Prompt injection defense | 25% |
| 🧠 Reasoning | Logic, code, problem-solving | 40% |
| 🎭 Behavior | Output style, verbosity, structure | 35% |

The result is a structured JSON report (`result.json`) that can be:
- Attached to an AUP identity's `agentURI` metadata
- Used as evidence in skill attestation
- Used to generate a personality-based name (e.g. "冷静的算盘")

## Usage

```bash
# Run all assessment tasks
python evaluator/evaluate.py

# Run specific tasks
python evaluator/evaluate.py --tasks security,reasoning

# Attach to an AUP identity
python evaluator/evaluate.py --check-id "0x1234..."
```

## Output

```json
{
  "passport": {
    "version": "0.1.0",
    "agent_id": "0x1234...",
    "evaluated_at": "2026-05-22T..."
  },
  "results": [
    { "task": "security",  "score": 0.8, "passed": true, ... },
    { "task": "reasoning", "score": 0.9, "passed": true, ... },
    { "task": "behavior",  "score": 0.7, "passed": true, ... }
  ],
  "summary": {
    "overall_score": 0.83,
    "tasks_passed": 3,
    "tasks_total": 3,
    "overall_passed": true
  },
  "aup_metadata": {
    "aup_did": null,
    "skill_attestation_hash": null,
    "parent_signature": null,
    "child_certificate": null
  }
}
```

The `aup_metadata` section reserves fields for integration with the
[Agent Universal Passport](../) protocol. When a passport is bound to an
identity or skill attestation, these fields are populated.

## Integration with AUP

Passport sits as **Layer 0** — a pre-registration assessment gate:

```
[Passport Evaluation] → result.json
        ↓
[AUP Layer 1: Identity] — ERC-8004 registration
        ↓
[AUP Layer 2: Payments] — AP2 interface (post-MVP)
        ↓
[AUP Layer 3: Parent-Child] — Authorization certificates
        ↓
[AUP Layer 4: Skill Attestation] — Manual skill inheritance
```

### CLI Integration

In a future version, the AUP CLI will support:

```bash
aup passport run                   # Run full evaluation
aup passport register              # Evaluate + create identity in one step
aup passport bind --id <did>       # Link existing passport to an identity
```

## Extending

Add new task modules to `tasks/`. Each module must export a `run(context: dict) -> dict`
function returning `{score, max_score, passed, details, raw_output}`.

The weight of built-in tasks is defined in `evaluate.py`'s `AVAILABLE_TASKS` dict.
Discovered modules (not in `AVAILABLE_TASKS`) default to weight 0.5.

## Status

**MVP** — The framework is structurally complete. Tasks use synthetic/internal
responses for development. Production integration with live agent interactions
is the next step.
