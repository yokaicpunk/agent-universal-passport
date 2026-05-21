# Smart Contracts

## Structure

```
contracts/
├── README.md
├── src/
│   ├── AUPIdentity.sol       # ERC-8004 wrapper + DID declarations
│   ├── AUPChildAuth.sol      # Authorization anchoring + revocation
│   └── AUPSkillRegistry.sol  # Skill hash anchoring (post-MVP)
├── test/
│   ├── AUPIdentity.t.sol
│   └── AUPChildAuth.t.sol
└── foundry.toml
```

## Prerequisites

- [Foundry](https://book.getfoundry.sh/)
- Base Sepolia testnet ETH

## Deploy

```bash
forge build
forge test
forge script script/Deploy.s.sol --rpc-url base-sepolia --broadcast
```
