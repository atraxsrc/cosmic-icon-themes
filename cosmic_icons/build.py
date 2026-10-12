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
