// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.25;

/// @title AUPSkillRegistry
/// @notice Skill hash anchoring — deferred to post-MVP
/// @dev Interface defined, no implementation yet
interface IAUPSkillRegistry {
    function attestSkill(uint256 parentAgentId, bytes32 skillHash, string calldata skillURI) external;
    function grantSkillToChild(bytes32 certificateId, bytes32 skillHash) external;
    function getSkillsOf(uint256 parentAgentId) external view returns (bytes32[] memory);
}
