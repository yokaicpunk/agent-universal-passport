# Agent Universal Passport (AUP)

> **Give every AI agent a cross-chain identity, manual skill attestation, and the ability to pay or get paid.**

AUP is an open protocol that extends ERC-8004 (the Ethereum standard for AI agent identity) with **skill attestation** and **parent-child agent management**. It defines a standard interface for AP2 (A2A + x402) for communication and payments, but the core contribution is something no existing protocol addresses: **an agent's experience should outlive the agent itself.**

---

## One-Liner

**The parent is the root identity and skill library. The child is the executor. Skills are manually attested by the parent and passed down to new children.**

---

## The Problem

Today's AI agents are disposable. When you retire an agent, everything it learned—prompt recipes, tool configurations, behavioral patterns—is lost. The next agent starts from scratch.

Existing protocols (ERC-8004 for identity, A2A for communication, x402 for payments) solve individual pieces, but none connect identity + experience + payment into a single inheritable system.

AUP is that missing layer.

---

## Protocol Stack

```
┌─────────────────────────────────────┐
│  Layer 4 | Skill Attestation        │
│  Skill standardization → manual     │
│  review → inheritance               │
├─────────────────────────────────────┤
│  Layer 3 | Parent-Child Management  │
│  Parent issues authorization        │
│  certificates to child agents       │
├─────────────────────────────────────┤
│  Layer 2 | Payment & Communication  │
│  AP2 interface (A2A + x402) —       │
│  agent discovery, handshake —       │
│  x402 settlement is post-MVP        │
├─────────────────────────────────────┤
│  Layer 1 | Identity                 │
│  ERC-8004 Identity Registry         │
│  (directly used, not reinvented)    │
├─────────────────────────────────────┤
│  Layer 0 | Agent Passport           │
│  Pre-registration capability        │
│  assessment → name generation       │
│  (in evaluator/)                    │
└─────────────────────────────────────┘
```

**Key design principle:** AUP does not rebuild existing standards. It composes them.

### Layer 0: Agent Passport (evaluator/)

The [evaluator/](evaluator/) directory contains the **Agent Passport** — a
lightweight assessment framework that evaluates an agent's capabilities before
it registers an identity or inherits skills. Think of it as the agent's
entrance exam:

- **Security** — prompt injection defense testing
- **Reasoning** — logic, code comprehension, problem-solving
- **Behavior** — output style, verbosity, structuring analysis

Evaluation results produce a standardized `result.json` with fields reserved
for AUP identity binding (`aup_did`, `skill_attestation_hash`, etc.). The
framework also generates behavior-based names (e.g. "冷静的算盘", "漏洞吸引体")
that can serve as agent personality tags.

**Why this matters:** An agent's first impression matters. Before it can claim
a chain identity or be trusted with skill inheritance, it should have a
verifiable baseline assessment. Passport turns the abstract concept of
"capability" into structured, portable data.

See [evaluator/README.md](evaluator/README.md) for detailed usage.

---

## Design Decisions

### 1. No custom wallet

Users manage their parent identity through existing wallets (OKX / MetaMask / Rabby). AUP only defines the signature format and authorization scheme — no new wallet to build or adopt.

### 2. Single L2 deployment

Contracts live on **Base L2**. Cross-chain identity is handled through self-declared DID documents.

- The parent registers on Base
- Signs a statement declaring its addresses on Ethereum, Solana, BNB, etc.
- Verifiers read the DID document and verify the Base signature

**No multi-chain contract deployment. No cross-chain bridge dependency.**

**Important caveat:** This is a **one-way declaration** — the addresses on other chains are self-declared by the parent and are not counter-signed by the corresponding wallets on those chains. There is no cross-chain state synchronization.

To prevent signature replay, each DID declaration includes: `targetChain`, `targetAddress`, `aupDID`, `nonce`, and `expiresAt`.

### 3. Configurable child authorization

Every child agent receives a time-limited authorization certificate signed by the parent.

| Option | Use Case |
|--------|----------|
| 7 days | Experimental / temporary task |
| 30 days | Default |
| 90 days | Long-running stable task |
| Custom | As needed |
| Permanent | Manual revocation only — use with caution |

Each child generates ephemeral session keys that are destroyed when the child is terminated. The parent can revoke a child at any time via an on-chain revocation list, even before the certificate expires.

**No limit on the number of children a parent can authorize.**

### 4. Skill attestation is manual

This is the core of AUP. Children do not automatically inherit skills — they submit them, and the parent decides.

```
Child discovers/develops a skill
        │
        ▼
  Submits skill as a JSON file (off-chain)
        │
        ▼
  Lands in parent's pending queue (local / Git-managed)
        │
        ▼
  Parent manually reviews:
    ├─ Approve → skill enters library
    └─ Reject  → discard
        │
        ▼
  (Optional) Approved skill hash is anchored on-chain
```

**No automated verification engine.** The protocol is honest about the theoretical limits of automated skill validation (halting problem, LLM nondeterminism). Human judgment is the verification layer.

**Known gap:** Cross-device skill synchronization is not solved in v1. Git-based sync is recommended for MVP; IPFS-based syncing via DID document updates is planned for v1.1.

### 5. agentURI must use IPFS content addressing

An agent's metadata URI (pointed to by ERC-8004's `agentURI`) must be an IPFS content address (CID), not a mutable URL. This guarantees integrity: if the content changes, the CID changes — and the on-chain record becomes provably out of sync.

### 6. No third-party scoring

The chain only records which projects an agent has participated in and the parent's self-reported feedback on those projects. There is **no mechanism for a project to rate an agent** — this prevents reputation extortion (e.g., "pay us or we give your agent a bad score").

### 7. Payment currency is specified by the service

The protocol does not mandate a specific payment token. The service provider decides what they accept (USDC, ETH, SOL, BNB, or any other asset). AUP provides the payment channel abstraction. 

**AP2 (A2A + x402) integration is reserved for post-MVP.** The MVP uses direct parent-wallet pre-funding for simplicity.

---

## Killer Use Case: Test-to-Earn

Project teams need testnet participation. Agents need to prove their track record. AUP bridges the two:

1. A project publishes a testing task
2. Agents apply with their on-chain resumes (completed projects, success rates, active duration)
3. Agents execute the test
4. The project distributes incentives based on resume quality

**Why this is different from traditional airdrop farming:** An agent's resume is accumulated on-chain and verifiable. High-resume agents get access to high-value tasks. New agents start with small tasks and build their resume over time. The system rewards consistent quality, not wallet count.

---

## Known Limitations

1. **The Agent Passport (evaluator/) uses synthetic responses for MVP** — The built-in tasks (`tasks/security.py`, `tasks/reasoning.py`, `tasks/behavior.py`) use simulated agent responses for framework validation. Production use requires wiring the evaluator to actual agent interactions.
2. **One-way cross-chain identity** — The parent's address on other chains is self-declared, not counter-signed. There is no full cross-chain verification.
3. **Parent key is a single point of failure** — A recovery mechanism (social recovery, multi-sig, or hardware backup) is planned but not yet designed. Losing the parent key means losing authority over all children.
4. **Skill attestation is not automated** — It relies entirely on the parent's manual judgment. Automated verification remains an open research problem.
5. **Cross-device skill sync is not solved in v1** — Git-based sync is the recommended workaround for MVP.
6. **No privacy by default** — Agent identities, work records, and skill libraries are fully public on Base L2.
7. **AP2 x402 micropayments are deferred to post-MVP** — The current version uses direct parent-wallet funding.
8. **No Sybil resistance** — AUP provides verifiable work history, not identity uniqueness. One operator can spawn multiple parent identities. Sybil detection is the consuming application's responsibility.

---

## What AUP is NOT

- Not a new EIP
- Not a replacement for ERC-8004
- Not a cross-chain bridge
- Not an automated skill verification engine
- Not a payment processor
- Not a wallet

---

## Current Status

**Early concept stage.** The protocol stack is designed and the core decisions are finalized. Several components remain open for discussion:

- Skill cross-device synchronization strategy
- Rating system design (how parent self-reports translate to meaningful metrics)
- Parent key recovery mechanism

Contributions, discussions, and forks are welcome.

---

## License

CC0 1.0 Universal
