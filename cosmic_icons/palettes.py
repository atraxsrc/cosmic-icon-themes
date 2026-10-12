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
