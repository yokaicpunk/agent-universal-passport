#!/usr/bin/env bash
# Test-to-Earn demo — Parent flow
# This script demonstrates the parent registering, creating a skill,
# authorizing a child, and publishing a task.

set -euo pipefail

echo "=== AUP Parent Flow Demo ==="

echo "1. Creating AUP identity..."
# aup-parent identity create "ipfs://QmDemoURI"

echo "2. Adding a skill..."
# echo '{"id":"skill-swap-v1","name":"Token Swap","type":"tool-config","body":{"template":"swap"}}' > /tmp/skill.json
# aup-parent skill add /tmp/skill.json

echo "3. Attesting the skill..."
# aup-parent skill attest skill-swap-v1

echo "4. Creating a child agent..."
# aup-parent child create "agent-alpha" --skills "skill-swap-v1" --expires 30d

echo "5. Publishing a test task..."
# aup-parent task publish examples/test-to-earn/task-template.json

echo "=== Parent setup complete ==="
echo "Child certificate and task are ready."
