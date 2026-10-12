#!/usr/bin/env bash
# Package every built pack in dist/ as dist/release/<pack>.tar.xz plus SHA256SUMS,
# ready to attach to a GitHub release. Symlinks are kept as symlinks.
#
#   python3 -m cosmic_icons.build && ./scripts/package.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
OUT="$DIST/release"

shopt -s nullglob
packs=("$DIST"/Cosmic-*/)
if [ ${#packs[@]} -eq 0 ]; then
  echo "no packs in $DIST; run: python3 -m cosmic_icons.build" >&2
  exit 1
fi

rm -rf "$OUT"
mkdir -p "$OUT"
for pack in "${packs[@]}"; do
  name="$(basename "$pack")"
  # Fixed owner and mtime so the same pack always gives the same archive.
  tar -C "$DIST" --sort=name --owner=0 --group=0 --numeric-owner \
    --mtime='2026-01-01 00:00:00Z' -cJf "$OUT/$name.tar.xz" "$name"
  echo "packed $name.tar.xz ($(du -h "$OUT/$name.tar.xz" | cut -f1))"
done

(cd "$OUT" && sha256sum -- *.tar.xz > SHA256SUMS)
echo "wrote $OUT/SHA256SUMS"
