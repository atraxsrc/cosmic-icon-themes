# Cosmic Icon Themes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate 20 icon packs (6 cosmic themes x 3-4 folder color variants, e.g. `Cosmic-DarkGold-Red`) from Fausto Korpsvart's Kanagawa icon pack. Folder colors come from each cosmic-*-theme palette; the symbolic/foreground color comes from each theme's text color.

**Architecture:** A small Python (stdlib only) generator. It fetches the upstream pack at a pinned commit into `vendor/` (gitignored), copies it once per variant with symlinks preserved, and rewrites a fixed set of colors in one regex pass per file. Built packs go to `dist/` (gitignored, ~89 MB each). One PNG preview sheet per theme goes to `previews/` and is committed so results can be judged on GitHub without installing anything.

**Tech Stack:** Python 3.12 stdlib (`re`, `os`, `shutil`, `subprocess`, `unittest`), git (sparse checkout), `rsvg-convert` (librsvg2-bin) and ImageMagick (`montage`, `convert`) for previews.

**Spec:** This document. The design and every color below were agreed in chat on 2026-10-12 after reviewing rendered previews.

## Findings from inspecting the upstream pack

Upstream: `https://github.com/Fausto-Korpsvart/Kanagawa-GKT-Theme`, path `icons/Kanagawa`, pinned commit `55ca4ba249eba21f861b9866b71ab41bb8930318`. License GPL-3.0. Based on Suru++ / Papirus (credits are in its `index.theme` header).

- 13,448 regular files, 18,814 symlinks, 0 PNGs, 89 MB.
- Folder icons live in `places/64/` and `places/16/` (real files). Other size dirs (`22`, `24`, `32`, `48`, every `@2x`) are symlinks to `16` or `64`.
- The default folder set is the `*-oomox-*` family in `places/64/` (70 files). `folder-download.svg`, `user-home.svg` etc. are symlinks to them. They use exactly three Kanagawa colors, found nowhere outside `places/`:
  - `#717C7C` - folder back panel
  - `#2A2A37` - folder front panel
  - `#E6C384` - symbol on the folder
  - plus `#ffffff` / `#fcefe8` shine overlays (leave alone)
- The 16 px folders and all symbolic icons use `currentColor` + `.ColorScheme-Text { color:#DCD7BA; }` or literal `#DCD7BA` (9,101 files, mixed case).
- `.ColorScheme-Highlight { color:#5294e2 }` appears in 6,958 files.
- The trash icons (`places/64/user-trash.svg`, `user-trash-full.svg`) use a teal gradient written as `rgb(26,214,171)` and `rgb(50,157,182)`. The same two values are also used by 36 `devices/` icons and 1 `status/` icon, which must NOT be recolored. So the `rgb()` swap applies only to files under `places/`.
- Other `folder-<color>-*.svg` families (blue, red, green...) are Papirus color variants. Leave them unchanged.

## Variants (agreed)

Per variant, four roles: `front` (folder body), `back` (folder back tab), `symbol` (glyph on folder), `accent` (ColorScheme-Highlight). Defaults: `back = shade(front, 0.75)`, `symbol = theme bg`, `accent = front`. "Dark"/"Ink" variants set all four explicitly (dark folder, accent-colored glyph, like the original Kanagawa).

| Theme | bg | text | Variant | front | back | symbol | accent |
|---|---|---|---|---|---|---|---|
| DarkGold | `#1B1B1B` | `#FFFFFF` | Gold | `#C0AF7F` | default | default | default |
| | | | Red | `#E75A50` | default | default | default |
| | | | Dark | `#2A2A29` | `#7B7972` | `#C0AF7F` | `#C0AF7F` |
| Dossier | `#D0D0C8` | `#242424` | Rust | `#953B19` | default | default | default |
| | | | Olive | `#51573B` | default | default | default |
| | | | Ink | `#242424` | `#59574D` | `#DE6A41` | `#953B19` |
| Monochrome | `#111111` | `#CCCCCC` | Silver | `#AAAAAA` | default | default | default |
| | | | White | `#DDDDDD` | default | default | default |
| | | | Dark | `#2A2A2A` | `#636363` | `#CCCCCC` | `#AAAAAA` |
| Noir | `#171717` | `#CCD0CF` | Orange | `#F25623` | default | default | default |
| | | | Sage | `#88A57D` | default | default | default |
| | | | Dark | `#2A2A2A` | `#686C69` | `#F25623` | `#F25623` |
| TokyoNight | `#1A1B26` | `#C7D1FD` | Blue | `#7AA2F7` | default | default | default |
| | | | Purple | `#BB9AF7` | default | default | default |
| | | | Green | `#9ECE6A` | default | default | default |
| | | | Dark | `#292E42` | `#545C7E` | `#7AA2F7` | `#7AA2F7` |
| WhiteGold | `#DEDBC8` | `#0C0C14` | Red | `#7A1F22` | default | default | default |
| | | | Gold | `#655628` | default | default | default |
| | | | Slate | `#4A545A` | default | default | default |
| | | | Ink | `#0C0C14` | `#665E4A` | `#C9A227` | `#7A6410` |

Monochrome `text` is `#CCCCCC` (its Firefox toolbar_text) because the `.ron` text_tint `#828282` is too dim for symbolic icons.

## Color mapping (per variant)

| Source | Where | Target |
|---|---|---|
| `#2A2A37` | anywhere | `front` |
| `#717C7C` | anywhere | `back` |
| `#E6C384` | anywhere | `symbol` |
| `#DCD7BA` | anywhere | theme `text` |
| `#5294E2` | anywhere | `accent` |
| `rgb(26,214,171)` | `places/` only | `front` as `rgb(r,g,b)` |
| `rgb(50,157,182)` | `places/` only | `back` as `rgb(r,g,b)` |

## Global Constraints

- Python stdlib only. No pip installs.
- Never dereference symlinks: copy with `symlinks=True`, walk with `followlinks=False`, skip symlinked files when rewriting.
- Replacement is a single regex pass per file. Hex tokens are `#` + exactly 6 hex digits not followed by another hex digit, matched case-insensitively. `rgb()` tokens are matched with optional whitespace. Never chain `str.replace` calls.
- Pack directory and `index.theme` `Name=` are both `Cosmic-<Theme>-<Variant>` (e.g. `Cosmic-TokyoNight-Purple`).
- Keep upstream `LICENSE` (GPL-3.0) in every built pack, and keep the credit header in `index.theme` unchanged.
- `vendor/` and `dist/` are gitignored. Never commit the upstream pack or built packs.
- No em-dashes or en-dashes anywhere (code, docs, commit messages). Use `-`.
- No emails, names, tokens, or personal data in any file or commit message. No `Co-Authored-By` trailers. Do not change git identity.

## Review Focus

1. **Symlinked dirs and files:** `places/48` is a symlink to `64`. A naive walk rewrites the same file several times or replaces links with copies. Expected: each built pack has exactly 18,814 symlinks with unchanged relative targets.
2. **Chained replacement:** a target can equal another source color (e.g. Monochrome Dark `symbol` `#CCCCCC` vs another role). Expected: each original token maps exactly once.
3. **Lowercase hex in source:** upstream mixes `#DCD7BA` and `#dcd7ba`. Expected: both are replaced.
4. **Device icons sharing the trash teal:** Expected: `devices/` and `status/` files keep `rgb(26,214,171)`; only `places/` trash icons change.
5. **8-digit hex such as `#DCD7BAFF`:** Expected: left unchanged rather than corrupted.

---

## File Structure

```
cosmic-icon-themes/
  .gitignore                 vendor/, dist/, __pycache__/
  README.md                  what it is, build, install, credits, license
  LICENSE                    GPL-3.0 (copied from upstream)
  cosmic_icons/
    __init__.py
    palettes.py              SOURCE, TRASH_SOURCE, THEMES (with variants)
    recolor.py               shade(), to_rgb(), resolve(), build_map(), build_trash_map(), recolor_bytes()
    build.py                 build_pack(), pack_name(), main() CLI
    preview.py               render previews/Cosmic-<Theme>.png from dist/
  scripts/
    fetch-upstream.sh        pinned sparse clone into vendor/
  tests/
    __init__.py
    test_recolor.py
    test_build.py
  previews/                  committed PNG sheets (one per theme)
  docs/superpowers/plans/    this plan
```

---

### Task 1: Repo scaffold and upstream fetch

**Files:**
- Create: `.gitignore`, `scripts/fetch-upstream.sh`, `cosmic_icons/__init__.py`, `tests/__init__.py`, `LICENSE`

**Interfaces:**
- Produces: `vendor/Kanagawa-GKT-Theme/icons/Kanagawa/` (source pack) and `vendor/Kanagawa-GKT-Theme/LICENSE`.

- [ ] **Step 1: Write `.gitignore`**

```gitignore
vendor/
dist/
__pycache__/
*.pyc
.mcp.json
```

- [ ] **Step 2: Write `scripts/fetch-upstream.sh`**

```bash
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
```

- [ ] **Step 3: Make it executable, create empty package files, run it**

```bash
chmod +x scripts/fetch-upstream.sh
mkdir -p cosmic_icons tests
touch cosmic_icons/__init__.py tests/__init__.py
./scripts/fetch-upstream.sh
cp vendor/Kanagawa-GKT-Theme/LICENSE LICENSE
```

- [ ] **Step 4: Verify the fetch**

Run:
```bash
test -f vendor/Kanagawa-GKT-Theme/icons/Kanagawa/index.theme && echo ok
find vendor/Kanagawa-GKT-Theme/icons/Kanagawa -type l | wc -l
head -2 LICENSE
```
Expected: `ok`, `18814`, and `GNU GENERAL PUBLIC LICENSE` in the header.

- [ ] **Step 5: Commit**

```bash
git add .gitignore scripts/fetch-upstream.sh cosmic_icons/__init__.py tests/__init__.py LICENSE
git commit -m "chore: scaffold repo and pinned upstream fetch"
```

---

### Task 2: Palettes and recolor core

**Files:**
- Create: `cosmic_icons/palettes.py`, `cosmic_icons/recolor.py`
- Test: `tests/test_recolor.py`

**Interfaces:**
- Produces:
  - `palettes.SOURCE: dict[str, str]` keys `front, back, symbol, text, accent` -> upstream hex
  - `palettes.TRASH_SOURCE: dict[str, str]` keys `front, back` -> upstream `rgb(...)` strings
  - `palettes.THEMES: dict[str, dict]`, each `{"bg": str, "text": str, "variants": dict[str, dict[str, str]]}`
  - `recolor.shade(hex_color: str, factor: float) -> str` (uppercase `#RRGGBB`)
  - `recolor.to_rgb(hex_color: str) -> str` (e.g. `"rgb(149,59,25)"`)
  - `recolor.resolve(theme: dict, variant: str) -> dict[str, str]` keys `front, back, symbol, accent, text`, all uppercase hex
  - `recolor.build_map(colors: dict[str, str]) -> dict[bytes, bytes]` (hex keys, uppercase)
  - `recolor.build_trash_map(colors: dict[str, str]) -> dict[bytes, bytes]` (`rgb(...)` keys, no spaces)
  - `recolor.recolor_bytes(data: bytes, mapping: dict[bytes, bytes]) -> bytes`

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_recolor.py
import unittest

from cosmic_icons.palettes import THEMES
from cosmic_icons.recolor import (build_map, build_trash_map, recolor_bytes,
                                  resolve, shade, to_rgb)


class ColorMathTest(unittest.TestCase):
    def test_shade_scales_channels(self):
        self.assertEqual(shade("#C0AF7F", 0.75), "#90835F")

    def test_shade_accepts_lowercase(self):
        self.assertEqual(shade("#ffffff", 0.5), "#808080")

    def test_to_rgb(self):
        self.assertEqual(to_rgb("#953B19"), "rgb(149,59,25)")


class ThemesTest(unittest.TestCase):
    def test_all_themes_and_variants(self):
        got = {t: sorted(THEMES[t]["variants"]) for t in THEMES}
        self.assertEqual(got, {
            "DarkGold": ["Dark", "Gold", "Red"],
            "Dossier": ["Ink", "Olive", "Rust"],
            "Monochrome": ["Dark", "Silver", "White"],
            "Noir": ["Dark", "Orange", "Sage"],
            "TokyoNight": ["Blue", "Dark", "Green", "Purple"],
            "WhiteGold": ["Gold", "Ink", "Red", "Slate"],
        })


class ResolveTest(unittest.TestCase):
    def test_defaults_for_accent_variant(self):
        c = resolve(THEMES["TokyoNight"], "Blue")
        self.assertEqual(c, {
            "front": "#7AA2F7",
            "back": shade("#7AA2F7", 0.75),
            "symbol": "#1A1B26",
            "accent": "#7AA2F7",
            "text": "#C7D1FD",
        })

    def test_explicit_dark_variant(self):
        c = resolve(THEMES["DarkGold"], "Dark")
        self.assertEqual(c["front"], "#2A2A29")
        self.assertEqual(c["back"], "#7B7972")
        self.assertEqual(c["symbol"], "#C0AF7F")
        self.assertEqual(c["accent"], "#C0AF7F")
        self.assertEqual(c["text"], "#FFFFFF")

    def test_unknown_variant_raises(self):
        with self.assertRaises(KeyError):
            resolve(THEMES["Noir"], "Pink")


class RecolorBytesTest(unittest.TestCase):
    def setUp(self):
        self.colors = resolve(THEMES["Dossier"], "Rust")
        self.hex_map = build_map(self.colors)
        self.full_map = {**self.hex_map, **build_trash_map(self.colors)}

    def test_replaces_folder_colors(self):
        svg = b'<path fill="#2A2A37"/><path fill="#717C7C"/><path fill="#E6C384"/>'
        out = recolor_bytes(svg, self.hex_map)
        self.assertIn(b'fill="#953B19"', out)
        self.assertIn(b'fill="' + shade("#953B19", 0.75).encode() + b'"', out)
        self.assertIn(b'fill="#D0D0C8"', out)

    def test_lowercase_source_is_replaced(self):
        out = recolor_bytes(b".ColorScheme-Text { color:#dcd7ba; }", self.hex_map)
        self.assertEqual(out, b".ColorScheme-Text { color:#242424; }")

    def test_highlight_replaced(self):
        out = recolor_bytes(b"color:#5294e2;", self.hex_map)
        self.assertEqual(out, b"color:#953B19;")

    def test_no_chained_replacement(self):
        m = {b"#AAAAAA": b"#BBBBBB", b"#BBBBBB": b"#CCCCCC"}
        self.assertEqual(recolor_bytes(b"#AAAAAA #BBBBBB", m), b"#BBBBBB #CCCCCC")

    def test_eight_digit_hex_untouched(self):
        data = b'stop-color="#DCD7BAFF"'
        self.assertEqual(recolor_bytes(data, self.hex_map), data)

    def test_unrelated_colors_untouched(self):
        data = b'fill="#ffffff" fill="#fcefe8" fill="#5C6BC0"'
        self.assertEqual(recolor_bytes(data, self.hex_map), data)

    def test_trash_rgb_replaced_with_full_map(self):
        data = b"stop-color:rgb(26,214,171) stop-color:rgb( 50, 157, 182 )"
        out = recolor_bytes(data, self.full_map)
        self.assertEqual(out, b"stop-color:rgb(149,59,25) stop-color:" +
                         to_rgb(shade("#953B19", 0.75)).encode())

    def test_trash_rgb_untouched_with_hex_map(self):
        data = b"stop-color:rgb(26,214,171)"
        self.assertEqual(recolor_bytes(data, self.hex_map), data)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_recolor -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cosmic_icons.palettes'`

- [ ] **Step 3: Write `cosmic_icons/palettes.py`**

```python
"""Upstream Kanagawa colors and the cosmic theme variants that replace them."""

# Colors as they appear in the upstream pack, keyed by role.
SOURCE = {
    "front": "#2A2A37",   # folder front panel (places/64 *-oomox-*)
    "back": "#717C7C",    # folder back tab
    "symbol": "#E6C384",  # glyph on the folder
    "text": "#DCD7BA",    # ColorScheme-Text, 16px folders, symbolic icons
    "accent": "#5294E2",  # ColorScheme-Highlight
}

# Trash icon gradient. Also used by devices/ icons, so only swapped under places/.
TRASH_SOURCE = {
    "front": "rgb(26,214,171)",
    "back": "rgb(50,157,182)",
}

BACK_SHADE = 0.75

# Variant keys: front (required), back, symbol, accent (optional).
# Defaults: back = shade(front, BACK_SHADE), symbol = theme bg, accent = front.
THEMES = {
    "DarkGold": {
        "bg": "#1B1B1B", "text": "#FFFFFF",
        "variants": {
            "Gold": {"front": "#C0AF7F"},
            "Red": {"front": "#E75A50"},
            "Dark": {"front": "#2A2A29", "back": "#7B7972", "symbol": "#C0AF7F", "accent": "#C0AF7F"},
        },
    },
    "Dossier": {
        "bg": "#D0D0C8", "text": "#242424",
        "variants": {
            "Rust": {"front": "#953B19"},
            "Olive": {"front": "#51573B"},
            "Ink": {"front": "#242424", "back": "#59574D", "symbol": "#DE6A41", "accent": "#953B19"},
        },
    },
    "Monochrome": {
        # .ron text_tint #828282 is too dim for symbolic icons; Firefox toolbar_text used.
        "bg": "#111111", "text": "#CCCCCC",
        "variants": {
            "Silver": {"front": "#AAAAAA"},
            "White": {"front": "#DDDDDD"},
            "Dark": {"front": "#2A2A2A", "back": "#636363", "symbol": "#CCCCCC", "accent": "#AAAAAA"},
        },
    },
    "Noir": {
        "bg": "#171717", "text": "#CCD0CF",
        "variants": {
            "Orange": {"front": "#F25623"},
            "Sage": {"front": "#88A57D"},
            "Dark": {"front": "#2A2A2A", "back": "#686C69", "symbol": "#F25623", "accent": "#F25623"},
        },
    },
    "TokyoNight": {
        "bg": "#1A1B26", "text": "#C7D1FD",
        "variants": {
            "Blue": {"front": "#7AA2F7"},
            "Purple": {"front": "#BB9AF7"},
            "Green": {"front": "#9ECE6A"},
            "Dark": {"front": "#292E42", "back": "#545C7E", "symbol": "#7AA2F7", "accent": "#7AA2F7"},
        },
    },
    "WhiteGold": {
        "bg": "#DEDBC8", "text": "#0C0C14",
        "variants": {
            "Red": {"front": "#7A1F22"},
            "Gold": {"front": "#655628"},
            "Slate": {"front": "#4A545A"},
            "Ink": {"front": "#0C0C14", "back": "#665E4A", "symbol": "#C9A227", "accent": "#7A6410"},
        },
    },
}
```

- [ ] **Step 4: Write `cosmic_icons/recolor.py`**

```python
"""Single-pass color replacement for SVG bytes."""
import re

from .palettes import BACK_SHADE, SOURCE, TRASH_SOURCE

# '#' + exactly six hex digits (not followed by a seventh), or rgb(r,g,b).
TOKEN = re.compile(
    rb"#[0-9A-Fa-f]{6}(?![0-9A-Fa-f])"
    rb"|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)"
)
SPACE = re.compile(rb"\s+")


def shade(hex_color: str, factor: float) -> str:
    value = hex_color.lstrip("#")
    channels = [int(value[i:i + 2], 16) for i in (0, 2, 4)]
    scaled = [max(0, min(255, round(c * factor))) for c in channels]
    return "#" + "".join(f"{c:02X}" for c in scaled)


def to_rgb(hex_color: str) -> str:
    value = hex_color.lstrip("#")
    return "rgb({},{},{})".format(*(int(value[i:i + 2], 16) for i in (0, 2, 4)))


def resolve(theme: dict, variant: str) -> dict[str, str]:
    spec = theme["variants"][variant]
    front = spec["front"].upper()
    return {
        "front": front,
        "back": spec.get("back", shade(front, BACK_SHADE)).upper(),
        "symbol": spec.get("symbol", theme["bg"]).upper(),
        "accent": spec.get("accent", front).upper(),
        "text": theme["text"].upper(),
    }


def build_map(colors: dict[str, str]) -> dict[bytes, bytes]:
    return {SOURCE[role].upper().encode(): colors[role].encode() for role in SOURCE}


def build_trash_map(colors: dict[str, str]) -> dict[bytes, bytes]:
    return {TRASH_SOURCE[role].encode(): to_rgb(colors[role]).encode() for role in TRASH_SOURCE}


def _key(token: bytes) -> bytes:
    return token.upper() if token.startswith(b"#") else SPACE.sub(b"", token)


def recolor_bytes(data: bytes, mapping: dict[bytes, bytes]) -> bytes:
    def swap(match: re.Match) -> bytes:
        token = match.group(0)
        return mapping.get(_key(token), token)

    return TOKEN.sub(swap, data)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m unittest tests.test_recolor -v`
Expected: all PASS. Hand check for `shade("#C0AF7F", 0.75)`: `192*0.75=144=90`, `175*0.75=131.25->131=83`, `127*0.75=95.25->95=5F`.

- [ ] **Step 6: Commit**

```bash
git add cosmic_icons/palettes.py cosmic_icons/recolor.py tests/test_recolor.py
git commit -m "feat: theme variants and single-pass color recolor"
```

---

### Task 3: Pack builder and CLI

**Files:**
- Create: `cosmic_icons/build.py`
- Test: `tests/test_build.py`

**Interfaces:**
- Consumes: `recolor.resolve`, `recolor.build_map`, `recolor.build_trash_map`, `recolor.recolor_bytes`, `palettes.THEMES`
- Produces:
  - `build.pack_name(theme: str, variant: str) -> str` returns `f"Cosmic-{theme}-{variant}"`
  - `build.build_pack(src: Path, out_root: Path, theme: str, variant: str, license_file: Path | None = None) -> Path` returns `out_root / pack_name(theme, variant)`
  - CLI: `python3 -m cosmic_icons.build [--src PATH] [--out PATH] [--theme NAME ...] [--variant NAME ...]`. Defaults: `--src vendor/Kanagawa-GKT-Theme/icons/Kanagawa`, `--out dist`, all themes, all variants. `--variant` filters variants by name within the selected themes.

- [ ] **Step 1: Write the failing tests (synthetic mini pack, no upstream needed)**

```python
# tests/test_build.py
import os
import tempfile
import unittest
from pathlib import Path

from cosmic_icons.build import build_pack, pack_name

INDEX = b"""# credit header kept
[Icon Theme]
Name=oomox-Kanagawa
Comment=x
Inherits=Yaru,gnome,hicolor
"""

FOLDER = b'<svg><path fill="#717C7C"/><path fill="#2A2A37"/><path fill="#E6C384"/></svg>'
SYMBOLIC = b'<style>.ColorScheme-Text { color:#dcd7ba; }</style>'
TRASH = b'<stop style="stop-color:rgb(26,214,171)"/><stop style="stop-color:rgb(50,157,182)"/>'


def make_pack(root: Path) -> Path:
    src = root / "Kanagawa"
    (src / "places" / "64").mkdir(parents=True)
    (src / "places" / "symbolic").mkdir(parents=True)
    (src / "devices" / "64").mkdir(parents=True)
    (src / "index.theme").write_bytes(INDEX)
    (src / "places" / "64" / "folder-oomox-download.svg").write_bytes(FOLDER)
    os.symlink("folder-oomox-download.svg", src / "places" / "64" / "folder-download.svg")
    os.symlink("64", src / "places" / "48")
    (src / "places" / "64" / "user-trash.svg").write_bytes(TRASH)
    (src / "devices" / "64" / "printer.svg").write_bytes(TRASH)
    (src / "places" / "symbolic" / "folder-symbolic.svg").write_bytes(SYMBOLIC)
    return src


class BuildPackTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.src = make_pack(self.root)
        self.out = self.root / "dist"

    def tearDown(self):
        self.tmp.cleanup()

    def build(self, theme="Dossier", variant="Rust"):
        return build_pack(self.src, self.out, theme, variant)

    def test_pack_name(self):
        self.assertEqual(pack_name("TokyoNight", "Purple"), "Cosmic-TokyoNight-Purple")

    def test_output_dir_name(self):
        self.assertEqual(self.build(), self.out / "Cosmic-Dossier-Rust")

    def test_folder_recolored(self):
        dest = self.build()
        data = (dest / "places/64/folder-oomox-download.svg").read_bytes()
        self.assertIn(b"#953B19", data)
        self.assertNotIn(b"#2A2A37", data)
        self.assertNotIn(b"#717C7C", data)
        self.assertNotIn(b"#E6C384", data)

    def test_dark_variant_uses_explicit_colors(self):
        dest = self.build("DarkGold", "Dark")
        data = (dest / "places/64/folder-oomox-download.svg").read_bytes()
        self.assertIn(b'fill="#2A2A29"', data)
        self.assertIn(b'fill="#7B7972"', data)
        self.assertIn(b'fill="#C0AF7F"', data)

    def test_trash_recolored_in_places_only(self):
        dest = self.build()
        trash = (dest / "places/64/user-trash.svg").read_bytes()
        self.assertIn(b"rgb(149,59,25)", trash)
        self.assertNotIn(b"rgb(26,214,171)", trash)
        printer = (dest / "devices/64/printer.svg").read_bytes()
        self.assertEqual(printer, TRASH)

    def test_symlinks_preserved(self):
        dest = self.build()
        link = dest / "places/64/folder-download.svg"
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), "folder-oomox-download.svg")
        self.assertTrue((dest / "places/48").is_symlink())
        self.assertEqual(os.readlink(dest / "places/48"), "64")

    def test_light_theme_has_no_original_text_color(self):
        dest = self.build()
        for dirpath, _dirs, files in os.walk(dest, followlinks=False):
            for f in files:
                path = Path(dirpath) / f
                if f.endswith(".svg") and not path.is_symlink():
                    self.assertNotIn(b"#DCD7BA", path.read_bytes().upper())

    def test_index_theme_renamed_and_header_kept(self):
        dest = self.build()
        text = (dest / "index.theme").read_text()
        self.assertIn("Name=Cosmic-Dossier-Rust\n", text)
        self.assertNotIn("oomox-Kanagawa", text)
        self.assertIn("# credit header kept", text)
        self.assertIn("Inherits=Yaru,gnome,hicolor", text)

    def test_rebuild_replaces_previous_output(self):
        self.build()
        dest = self.build()
        self.assertTrue((dest / "places/64/folder-download.svg").is_symlink())

    def test_source_untouched(self):
        self.build()
        self.assertEqual((self.src / "places/64/folder-oomox-download.svg").read_bytes(), FOLDER)
        self.assertEqual((self.src / "places/64/user-trash.svg").read_bytes(), TRASH)

    def test_license_copied(self):
        lic = self.root / "LICENSE"
        lic.write_text("GNU GENERAL PUBLIC LICENSE")
        dest = build_pack(self.src, self.out, "Noir", "Orange", license_file=lic)
        self.assertEqual((dest / "LICENSE").read_text(), "GNU GENERAL PUBLIC LICENSE")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_build -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'cosmic_icons.build'`

- [ ] **Step 3: Write `cosmic_icons/build.py`**

```python
"""Build Cosmic-<Theme>-<Variant> icon packs from the upstream Kanagawa pack."""
import argparse
import os
import re
import shutil
import sys
from pathlib import Path

from .palettes import THEMES
from .recolor import build_map, build_trash_map, recolor_bytes, resolve

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = ROOT / "vendor" / "Kanagawa-GKT-Theme" / "icons" / "Kanagawa"
DEFAULT_LICENSE = ROOT / "vendor" / "Kanagawa-GKT-Theme" / "LICENSE"
DEFAULT_OUT = ROOT / "dist"


def pack_name(theme: str, variant: str) -> str:
    return f"Cosmic-{theme}-{variant}"


def build_pack(src: Path, out_root: Path, theme: str, variant: str,
               license_file: Path | None = None) -> Path:
    name = pack_name(theme, variant)
    dest = out_root / name
    if dest.exists() or dest.is_symlink():
        shutil.rmtree(dest)
    out_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest, symlinks=True)

    colors = resolve(THEMES[theme], variant)
    hex_map = build_map(colors)
    places_map = {**hex_map, **build_trash_map(colors)}
    places_root = dest / "places"

    for dirpath, _dirnames, filenames in os.walk(dest, followlinks=False):
        in_places = Path(dirpath).is_relative_to(places_root)
        mapping = places_map if in_places else hex_map
        for filename in filenames:
            if not filename.endswith(".svg"):
                continue
            path = Path(dirpath) / filename
            if path.is_symlink():
                continue
            data = path.read_bytes()
            new = recolor_bytes(data, mapping)
            if new != data:
                path.write_bytes(new)

    index = dest / "index.theme"
    text = index.read_text(encoding="utf-8")
    index.write_text(re.sub(r"(?m)^Name=.*$", f"Name={name}", text, count=1),
                     encoding="utf-8")

    if license_file is not None and license_file.is_file():
        shutil.copyfile(license_file, dest / "LICENSE")
    return dest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--theme", action="append", choices=sorted(THEMES))
    parser.add_argument("--variant", action="append")
    args = parser.parse_args(argv)

    if not (args.src / "index.theme").is_file():
        print(f"source pack not found at {args.src}; run scripts/fetch-upstream.sh",
              file=sys.stderr)
        return 1

    built = 0
    for theme in args.theme or sorted(THEMES):
        for variant in THEMES[theme]["variants"]:
            if args.variant and variant not in args.variant:
                continue
            dest = build_pack(args.src, args.out, theme, variant, DEFAULT_LICENSE)
            print(f"built {dest}")
            built += 1
    if built == 0:
        print("nothing matched --theme/--variant", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Note: `os.walk(followlinks=False)` lists a symlinked dir like `places/48` in `dirnames` but does not descend into it, so each real file is rewritten exactly once.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m unittest discover -s tests -t . -v`
Expected: all PASS (recolor + build).

- [ ] **Step 5: Build all 20 real packs and verify**

Run:
```bash
python3 -m cosmic_icons.build
ls -d dist/Cosmic-* | wc -l
for d in dist/Cosmic-*; do
  printf "%s links=%s oldfront=%s oldtext=%s devteal=%s name=%s\n" "$(basename "$d")" \
    "$(find "$d" -type l | wc -l)" \
    "$(grep -rliE '#2A2A37' "$d" | wc -l)" \
    "$(grep -rliE '#DCD7BA([^0-9A-Fa-f]|$)' "$d" | wc -l)" \
    "$(grep -rlF 'rgb(26,214,171)' "$d/devices" | wc -l)" \
    "$(grep -m1 '^Name=' "$d/index.theme")"
done
```
Expected: `20`, then for every pack `links=18814 oldfront=0 oldtext=0 devteal=36 name=Name=Cosmic-<Theme>-<Variant>`.

- [ ] **Step 6: Commit**

```bash
git add cosmic_icons/build.py tests/test_build.py
git commit -m "feat: build Cosmic-<Theme>-<Variant> packs with symlinks preserved"
```

---

### Task 4: Preview sheets

**Files:**
- Create: `cosmic_icons/preview.py`, `previews/Cosmic-<Theme>.png` (6 files, generated)

**Interfaces:**
- Consumes: built packs in `dist/Cosmic-<Theme>-<Variant>`, `palettes.THEMES`, `build.pack_name`
- Produces: one PNG per theme. Title row, then one row per variant: label (`<Variant> <front hex>`), 7 icons at 96 px (folder, folder-open, folder-documents, folder-download, folder-music, user-home, user-trash) from `places/64`, and 4 icons from `places/16` at 32 px (folder, folder-open, user-home, folder-download). Background is the theme `bg`, text is the theme `text`.
- CLI: `python3 -m cosmic_icons.preview`

- [ ] **Step 1: Ensure tools exist (cloud VM may lack them)**

```bash
command -v rsvg-convert >/dev/null || sudo apt-get install -y librsvg2-bin
command -v montage >/dev/null || sudo apt-get install -y imagemagick
```

- [ ] **Step 2: Write `cosmic_icons/preview.py`**

```python
"""Render one folder preview sheet per theme from the packs in dist/."""
import subprocess
import sys
import tempfile
from pathlib import Path

from .build import DEFAULT_OUT, ROOT, pack_name
from .palettes import THEMES
from .recolor import resolve

BIG = ["folder", "folder-open", "folder-documents", "folder-download",
       "folder-music", "user-home", "user-trash"]
SMALL = ["folder", "folder-open", "user-home", "folder-download"]
PREVIEWS = ROOT / "previews"


def run(*args: str) -> None:
    subprocess.run(list(args), check=True)


def render(svg: Path, px: int, out: Path) -> Path:
    run("rsvg-convert", "-w", str(px), "-h", str(px), str(svg), "-o", str(out))
    return out


def label(text: str, bg: str, fg: str, size: int, out: Path) -> Path:
    run("convert", "-background", bg, "-fill", fg, "-pointsize", str(size),
        f"label: {text}", str(out))
    return out


def theme_sheet(theme: str, dist: Path, tmp: Path) -> Path:
    spec = THEMES[theme]
    bg, fg = spec["bg"], spec["text"]
    rows = [label(f"Cosmic-{theme}", bg, fg, 30, tmp / "title.png")]
    for variant in spec["variants"]:
        pack = dist / pack_name(theme, variant)
        icons = [render(pack / "places/64" / f"{n}.svg", 96, tmp / f"{variant}-b-{n}.png")
                 for n in BIG]
        icons += [render(pack / "places/16" / f"{n}.svg", 32, tmp / f"{variant}-s-{n}.png")
                  for n in SMALL]
        strip = tmp / f"{variant}-strip.png"
        run("montage", *map(str, icons), "-tile", f"{len(icons)}x1",
            "-geometry", "+8+8", "-background", bg, str(strip))
        front = resolve(spec, variant)["front"]
        name = label(f"{variant:<7} {front}", bg, fg, 22, tmp / f"{variant}-label.png")
        row = tmp / f"{variant}-row.png"
        run("convert", str(name), str(strip), "-background", bg,
            "-gravity", "center", "+append", str(row))
        rows.append(row)
    PREVIEWS.mkdir(exist_ok=True)
    out = PREVIEWS / f"Cosmic-{theme}.png"
    run("convert", *map(str, rows), "-background", bg, "-gravity", "west",
        "-append", "-bordercolor", bg, "-border", "10", "+repage", str(out))
    return out


def main() -> int:
    for theme in sorted(THEMES):
        with tempfile.TemporaryDirectory() as tmp:
            print(f"wrote {theme_sheet(theme, DEFAULT_OUT, Path(tmp))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Note: do not use `-splice` with `-gravity west` when stacking images; it inserts the gap in the vertical middle of each image and draws bars through the icons.

- [ ] **Step 3: Run it**

```bash
python3 -m cosmic_icons.preview
ls -la previews/
```
Expected: six PNGs, `Cosmic-DarkGold.png` ... `Cosmic-WhiteGold.png`.

- [ ] **Step 4: Look at every PNG (use the Read tool on each image)**

Per row check: folder body is the `front` color, back tab is darker, glyph contrasts with the folder, trash matches the folder, the 4 small icons on the right are visible against the background (especially Dossier and WhiteGold). Note anything off in the final report. Do not change palette values on your own; list concerns instead.

- [ ] **Step 5: Commit**

```bash
git add cosmic_icons/preview.py previews/*.png
git commit -m "feat: per-theme folder preview sheets"
```

---

### Task 5: README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write `README.md`**

````markdown
# Cosmic Icon Themes

Recolored builds of the Kanagawa icon pack by Fausto Korpsvart, matched to the cosmic-*-theme rices. Each theme comes in several folder colors taken from its own palette:

| Theme | Variants |
|---|---|
| DarkGold | Gold, Red, Dark |
| Dossier | Rust, Olive, Ink |
| Monochrome | Silver, White, Dark |
| Noir | Orange, Sage, Dark |
| TokyoNight | Blue, Purple, Green, Dark |
| WhiteGold | Red, Gold, Slate, Ink |

Symbolic and small icons take the theme's text color, so light themes stay readable.

## Previews

![DarkGold](previews/Cosmic-DarkGold.png)
![Dossier](previews/Cosmic-Dossier.png)
![Monochrome](previews/Cosmic-Monochrome.png)
![Noir](previews/Cosmic-Noir.png)
![TokyoNight](previews/Cosmic-TokyoNight.png)
![WhiteGold](previews/Cosmic-WhiteGold.png)

## Build

```bash
./scripts/fetch-upstream.sh
python3 -m cosmic_icons.build                                   # all 20 packs into dist/
python3 -m cosmic_icons.build --theme Noir                      # all Noir variants
python3 -m cosmic_icons.build --theme TokyoNight --variant Purple
python3 -m cosmic_icons.preview                                 # refresh previews/
```

Each pack is about 89 MB, so build only what you use.

## Install

```bash
cp -a dist/Cosmic-Noir-Orange ~/.local/share/icons/
gtk-update-icon-cache -f ~/.local/share/icons/Cosmic-Noir-Orange
```

Then pick the icon theme in COSMIC Settings > Desktop > Appearance.

## Tests

```bash
python3 -m unittest discover -s tests -t . -v
```

## Credits and license

Based on the Kanagawa icon pack from https://github.com/Fausto-Korpsvart/Kanagawa-GKT-Theme (pinned commit in `scripts/fetch-upstream.sh`), which builds on Suru++ and Papirus. Full credits are kept in each pack's `index.theme`. Licensed GPL-3.0, see `LICENSE`.
````

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: README with variants, previews, build, install, credits"
```

---

## Final report (for an unattended / cloud run)

When done, push the branch and write a short report with: the test output summary, the Task 3 Step 5 verification lines for all 20 packs, and any visual concerns from Task 4 Step 4. Do not open a PR unless asked.
