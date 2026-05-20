#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-cursor}"
SCOPE="${2:-project}"
PROJECT_DIR="${3:-.}"

python "$(dirname "$0")/install.py" --target "$TARGET" --scope "$SCOPE" --project-dir "$PROJECT_DIR"
