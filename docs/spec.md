# Protocol Specification

## Agent Identity

Agents are registered via ERC-8004 Identity Registry. Each agent has a unique tokenId and an agentURI pointing to its metadata.

## Parent-Child Relationship

A parent registers an agent identity, then authorizes children by signing authorization certificates. Certificates are anchored on-chain for verifiability.

### Authorization Certificate Schema
See `schemas/child-certificate.json`.

## Skill Attestation

Skills are standardized JSON documents. Children submit skills to the parent's pending queue. The parent manually attests (approves) or rejects.

### Skill Schema
See `schemas/skill-attestation.json`.

## DID Document

The parent's DID document declares its identity across chains. It is stored off-chain and pointed to by agentURI.

### DID Document Schema
See `schemas/did-document.json`.

## Payment

Post-MVP. Interface defined but not implemented. See Layer 2 AP2 specification.
