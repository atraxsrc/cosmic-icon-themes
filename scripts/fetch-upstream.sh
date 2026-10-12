#!/usr/bin/env bash
# Fetch the upstream Kanagawa icon pack at a pinned commit into vendor/.
set -euo pipefail

REPO_URL="https://github.com/Fausto-Korpsvart/Kanagawa-GKT-Theme.git"
COMMIT="55ca4ba249eba21f861b9866b71ab41bb8930318"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/vendor/Kanagawa-GKT-Theme"

if [ -d "$DEST/icons/Kanagawa" ]; then
  echo "upstream already present at $DEST"
  exit 0
fi

rm -rf "$DEST"
mkdir -p "$DEST"
git -C "$DEST" init -q
git -C "$DEST" remote add origin "$REPO_URL"
git -C "$DEST" sparse-checkout set icons/Kanagawa
git -C "$DEST" fetch -q --depth 1 --filter=blob:none origin "$COMMIT"
git -C "$DEST" checkout -q FETCH_HEAD
echo "fetched upstream $COMMIT into $DEST"
