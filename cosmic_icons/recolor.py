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


def luminance(hex_color: str) -> float:
    value = hex_color.lstrip("#")
    r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def resolve(theme: dict, variant: str) -> dict[str, str]:
    spec = theme["variants"][variant]
    front = spec["front"].upper()
    back = spec.get("back", shade(front, BACK_SHADE)).upper()
    if "trash" in spec:
        trash_top = spec["trash"].upper()
        trash_bottom = shade(trash_top, BACK_SHADE)
    else:
        # Upstream trash gradient runs light to dark, top to bottom.
        trash_top, trash_bottom = sorted((front, back), key=luminance, reverse=True)
    return {
        "front": front,
        "back": back,
        "symbol": spec.get("symbol", theme["bg"]).upper(),
        "accent": spec.get("accent", front).upper(),
        "text": theme["text"].upper(),
        "trash_top": trash_top,
        "trash_bottom": trash_bottom,
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
