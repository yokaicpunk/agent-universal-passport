#!/usr/bin/env bash
# Test-to-Earn demo — Child flow
# This script demonstrates the child accepting a task, executing it,
# and submitting results.

set -euo pipefail

echo "=== AUP Child Flow Demo ==="

echo "1. Initializing child with certificate..."
# aup-child init /path/to/certificate.json

echo "2. Checking identity..."
# aup-child identity show

echo "3. Listing inherited skills..."
# aup-child skill list

echo "4. Accepting task..."
# aup-child task accept "t-001"

echo "5. Running task..."
# aup-child task run "t-001"

echo "6. Submitting results..."
# aup-child task submit "t-001" '{"txHash":"0x...","gasUsed":21000,"success":true}'

echo "=== Child flow complete ==="
