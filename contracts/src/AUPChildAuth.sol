// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.25;

/// @title AUPChildAuth
/// @notice Parent-Child authorization anchoring + revocation list
interface IAUPChildAuth {
    function authorizeChild(
        uint256 parentAgentId,
        address childAddress,
        string calldata certificateURI,
        uint256 expiresAt
    ) external returns (bytes32 certificateId);

    function revokeChild(bytes32 certificateId) external;
    function renewChild(bytes32 certificateId, uint256 newExpiresAt) external;
    function isAuthorized(bytes32 certificateId) external view returns (bool);
    function getChildrenOf(uint256 parentAgentId) external view returns (bytes32[] memory);
    function getCertificate(bytes32 certificateId) external view returns (Certificate memory);
}

struct Certificate {
    bytes32 certificateId;
    uint256 parentAgentId;
    address childAddress;
    address parentOwner;
    string certificateURI;
    uint256 issuedAt;
    uint256 expiresAt;
    bool revoked;
}
