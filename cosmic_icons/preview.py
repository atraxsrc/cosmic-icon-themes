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
