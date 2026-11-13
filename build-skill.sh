#!/usr/bin/env bash
# Package salesforce-diagrams/ into salesforce-diagrams.skill (a zip with the
# skill folder at its root), ready to upload in Claude Desktop / claude.ai.
set -euo pipefail
cd "$(dirname "$0")"
rm -f salesforce-diagrams.skill
find salesforce-diagrams -name '__pycache__' -prune -exec rm -rf {} +
zip -qr -X salesforce-diagrams.skill salesforce-diagrams -x '*:Zone.Identifier' '*.pyc' '*/.DS_Store'
unzip -l salesforce-diagrams.skill
