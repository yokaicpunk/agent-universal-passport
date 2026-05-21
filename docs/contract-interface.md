# Contract Interface Design

## AUPIdentity.sol (MVP)

### registerAgent
Registers a new agent identity via ERC-8004 wrapper.

### updateAgentURI
Updates the agent's metadata URI.

### declareCrossChainAddress
Parent declares their address on another chain (self-declared, one-way).

### getAgent / getDIDDocument
Query functions.

## AUPChildAuth.sol (MVP)

### authorizeChild
Creates a child authorization anchored on-chain.

### revokeChild
Revokes a child authorization before expiry.

### renewChild
Extends or updates a child authorization.

### isAuthorized / getChildrenOf / getCertificate
Query functions.

## AUPSkillRegistry.sol (Post-MVP)

Interface defined. Implementation deferred.
