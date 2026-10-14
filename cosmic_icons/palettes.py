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
    "trash_top": "rgb(26,214,171)",
    "trash_bottom": "rgb(50,157,182)",
}

BACK_SHADE = 0.75

# Variant keys: front (required), back, symbol, accent, trash (optional).
# Defaults: back = shade(front, BACK_SHADE), symbol = theme bg, accent = front.
# Trash gradient defaults to the lighter of front/back on top; "trash" overrides
# it (top = trash, bottom = shade(trash, BACK_SHADE)).
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
            # Darker trash so its white recycle glyph stays readable.
            "White": {"front": "#DDDDDD", "trash": "#828282"},
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
    "TokyoDay": {
        "bg": "#E6E7ED", "text": "#343B59",
        "variants": {
            "Blue": {"front": "#2959AA"},
            "Purple": {"front": "#7B43BA"},
            "Green": {"front": "#33635C"},
            "Ink": {"front": "#343B59", "back": "#565C75", "symbol": "#2959AA", "accent": "#2959AA"},
        },
    },
    "Ember": {
        "bg": "#15171C", "text": "#D6D9E0",
        "variants": {
            "Ember": {"front": "#E8713A"},
            "Moss": {"front": "#8FB58A"},
            "Slate": {"front": "#7FA3C7"},
            "Dark": {"front": "#2A2F38", "back": "#7C8290", "symbol": "#E8713A", "accent": "#E8713A"},
        },
    },
    "EmberDay": {
        "bg": "#E9E6DF", "text": "#2B2E36",
        "variants": {
            "Ember": {"front": "#A4441A"},
            "Moss": {"front": "#4C6B45"},
            "Slate": {"front": "#2F5C8A"},
            "Ink": {"front": "#2B2E36", "back": "#505156", "symbol": "#A4441A", "accent": "#A4441A"},
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
