# Architecture Overview

## Four-Layer Protocol Stack

```
┌─────────────────────────────────────┐
│  Layer 4 | Skill Attestation         │
├─────────────────────────────────────┤
│  Layer 3 | Parent-Child Management  │
├─────────────────────────────────────┤
│  Layer 2 | Payment & Communication  │
├─────────────────────────────────────┤
│  Layer 1 | Identity (ERC-8004)      │
└─────────────────────────────────────┘
```

### Layer 1 — Identity
Directly uses ERC-8004 Identity Registry. No new identity standard.

### Layer 2 — Payment & Communication
Defines AP2 (A2A + x402) interface. Post-MVP.

### Layer 3 — Parent-Child Management
Parent wallet issues authorization certificates. Children use ephemeral session keys.

### Layer 4 — Skill Attestation
Skills are submitted as JSON by children, reviewed manually by the parent, and stored in a local Git-managed library. Optional on-chain hash anchoring.

## Data Flow

```
Parent registers on-chain (ERC-8004)
  → Parent signs authorization certificate
  → Child receives certificate + inherited skills
  → Child executes tasks
  → Child proposes new skills
  → Parent manually attests or rejects
  → Attested skills enter library
  → New children inherit from updated library
```

## Contract Architecture

Three contracts planned:

1. **AUPIdentity.sol** — Agent registration + DID declarations
2. **AUPChildAuth.sol** — Authorization anchoring + revocation
3. **AUPSkillRegistry.sol** — Skill hash anchoring (post-MVP)

See [contract-interface.md](./contract-interface.md) for details.
