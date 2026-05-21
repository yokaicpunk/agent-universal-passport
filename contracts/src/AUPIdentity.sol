// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.25;

/// @title AUPIdentity
/// @notice ERC-8004 wrapper + DID cross-chain declarations
/// @dev MVP version — interface defined, implementation pending
interface IAUPIdentity {
    function registerAgent(string calldata agentURI) external returns (uint256 agentId);
    function updateAgentURI(uint256 agentId, string calldata newAgentURI) external;
    function getAgent(uint256 agentId) external view returns (AgentInfo memory);
    function declareCrossChainAddress(
        uint256 agentId,
        string calldata targetChain,
        bytes calldata targetAddress,
        uint256 nonce,
        uint256 expiresAt
    ) external;
    function getDIDDocument(uint256 agentId) external view returns (DIDDocument memory);
}

struct AgentInfo {
    uint256 agentId;
    address owner;
    string agentURI;
    uint256 registeredAt;
    bool exists;
}

struct CrossChainDeclaration {
    string targetChain;
    bytes targetAddress;
    uint256 nonce;
    uint256 expiresAt;
    uint256 declaredAt;
}

struct DIDDocument {
    uint256 agentId;
    address baseAddress;
    CrossChainDeclaration[] crossChainAddresses;
    string didVersion;
}
