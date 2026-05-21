# Agent Universal Passport (AUP)

> **Give every AI agent a cross-chain verified identity, inheritable skills, and self-sovereign payment capability.**

AUP extends the ERC-8004 identity layer with **skill heredity** and **parent-child agent management**. It integrates the AP2 (A2A + x402) payment protocol for agent-to-agent commerce, while focusing on what no existing protocol addresses: **an agent's experience should outlive the agent itself.**

---

## One-Liner

**The parent is the root. The child is the executor. Skills can be passed down and evolved through manual attestation.**

---

## The Problem

Today's AI agents are disposable. When you retire an agent, everything it learned—prompt recipes, tool configurations, behavioral patterns—is lost. The next agent starts from scratch.

Existing protocols (ERC-8004 for identity, A2A for communication, x402 for payments) solve individual pieces, but none connect identity + experience + payment into a single inheritable system.

AUP is that missing layer.

---

## Protocol Stack

```
┌─────────────────────────────────────┐
│  Layer 4 | Skill Heredity           │
│  Skill standardization → manual     │
│  attestation → inheritance          │
├─────────────────────────────────────┤
│  Layer 3 | Parent-Child Management  │
│  Parent wallet issues authorization │
│  certificates to child agents       │
├─────────────────────────────────────┤
│  Layer 2 | Payment & Communication  │
│  AP2 (A2A + x402) — agent            │
│  discovery, handshake, micropayments │
├─────────────────────────────────────┤
│  Layer 1 | Identity                 │
│  ERC-8004 Identity Registry         │
│  (directly used, not reinvented)    │
└─────────────────────────────────────┘
```

**Key design principle:** AUP does not rebuild existing standards. It composes them.

---

## Design Decisions

### 1. No custom wallet

Users manage their parent identity through existing wallets (OKX / MetaMask / Rabby). AUP only defines the signature format and authorization scheme—no new wallet.

### 2. Single L2 deployment

Contracts live on **Base L2**. Cross-chain identity is handled through self-declared DID documents. The parent registers on Base, then signs a statement declaring its addresses on other chains (Ethereum / Solana / BNB). Verifiers read the DID document and verify the Base signature. No multi-chain contract deployment, no cross-chain bridge dependency.

### 3. Child authorization with configurable expiry

Every child agent receives a time-limited authorization certificate. Options: 7 days / 30 days / 90 days / custom / permanent. Each child generates ephemeral session keys that self-destruct when the child is terminated.

### 4. Skill attestation is manual

Children submit skills as JSON files. These land in a pending queue. The parent manually reviews and either approves (skills enter the library) or rejects. No automated verification engine—the protocol is honest about the theoretical limits of skill validation (halting problem, LLM nondeterminism).

**Known gap:** Cross-device skill synchronization is not yet solved for v1. Git-based sync is recommended for MVP; IPFS-based syncing via DID document updates is planned for v1.1.

### 5. No third-party scoring

The chain only records which projects an agent has participated in and the parent's self-reported feedback on those projects. No mechanism allows a project to rate an agent, preventing reputation extortion.

### 6. Unrestricted child count

No artificial limit on how many children a parent can authorize. If a parent can manage 100 children effectively, that's a testament to its capability.

---

## Killer Use Case: Test-to-Earn

Project teams need testnet participation. Agents need to prove their track record. AUP bridges the two:

1. A project publishes a testing task
2. Agents apply with their on-chain resumes (completed projects, success rates, active duration)
3. Agents execute the test
4. The project distributes incentives based on resume quality

**Why this is different from traditional airdrop farming:** An agent's resume is accumulated on-chain and verifiable. High-resume agents get access to high-value tasks. New agents start with small tasks and build their resume. The system rewards consistent quality, not wallet count.

**Sybil resistance:** AUP does not provide Sybil resistance by itself. It provides **verifiable work history**, which is a different problem. Projects can use resume quality thresholds independently of Sybil detection.

---

## Current Status

**Early concept stage.** The protocol stack is designed and the core decisions are finalized. Several components remain open for discussion:

- Skill cross-device synchronization (IPFS vs Git vs custom service)
- Rating system design (how parent self-reports translate to meaningful metrics)
- Project-side verification incentives (why would a project sign a confirmation?)

**What AUP is NOT:**
- Not a new EIP
- Not a replacement for ERC-8004
- Not a cross-chain bridge
- Not an automated skill verification engine
- Not a payment processor

---

## License

CC0 1.0 Universal
 
