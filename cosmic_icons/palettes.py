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
    "K3": {
        "bg": "#101315", "text": "#CACCCC",
        "variants": {
            "Steel": {"front": "#798186"},
            "Terracotta": {"front": "#DE6145"},
            "Dark": {"front": "#2C2C2D", "back": "#565D60", "symbol": "#798186", "accent": "#798186"},
        },
    },
    "Cinder": {
        "bg": "#121212", "text": "#B3ADAD",
        "variants": {
            "Orange": {"front": "#CC6528"},
            "Brick": {"front": "#C75E57"},
            "Dark": {"front": "#222228", "back": "#626A78", "symbol": "#CC6528", "accent": "#CC6528"},
        },
    },
    "Brass": {
        "bg": "#1C1B19", "text": "#F0E4C5",
        "variants": {
            "Sand": {"front": "#D4BD99"},
            "Brick": {"front": "#DD6A5C"},
            "Dark": {"front": "#2C2925", "back": "#6B655C", "symbol": "#D4BD99", "accent": "#D4BD99"},
        },
    },
    "Sorbet": {
        "bg": "#05080A", "text": "#FFF6FF",
        "variants": {
            "Mint": {"front": "#B2FFF3"},
            "Rose": {"front": "#FF9FBC"},
            "Dark": {"front": "#1A1727", "back": "#5E616C", "symbol": "#B2FFF3", "accent": "#B2FFF3"},
        },
    },
    "Prism": {
        "bg": "#060D1F", "text": "#E0F7FA",
        "variants": {
            "Petal": {"front": "#F7C3C6"},
            "Ruby": {"front": "#E95C4B"},
            "Dark": {"front": "#161F33", "back": "#5A6B8C", "symbol": "#F7C3C6", "accent": "#F7C3C6"},
        },
    },
    "PrismDay": {
        "bg": "#DFEAEC", "text": "#242B3D",
        "variants": {
            "Petal": {"front": "#804C4F"},
            "Ruby": {"front": "#B52817"},
            "Dark": {"front": "#242B3D", "back": "#515B7C", "symbol": "#804C4F", "accent": "#804C4F"},
        },
    },
    "Nebula": {
        "bg": "#181C22", "text": "#E0E6ED",
        "variants": {
            "Teal": {"front": "#4ECDC4"},
            "Rose": {"front": "#FF7B92"},
            "Dark": {"front": "#272C34", "back": "#5B6478", "symbol": "#4ECDC4", "accent": "#4ECDC4"},
        },
    },
    "NebulaDay": {
        "bg": "#E2E5E9", "text": "#2B2F35",
        "variants": {
            "Teal": {"front": "#186A61"},
            "Rose": {"front": "#A8243B"},
            "Dark": {"front": "#2B2F35", "back": "#555F72", "symbol": "#186A61", "accent": "#186A61"},
        },
    },
    "Sumi": {
        "bg": "#050505", "text": "#D6D0C5",
        "variants": {
            "Moss": {"front": "#8B9388"},
            "Vermilion": {"front": "#DA614E"},
            "Dark": {"front": "#1E1E1E", "back": "#5F5D58", "symbol": "#8B9388", "accent": "#8B9388"},
        },
    },
    "SumiDay": {
        "bg": "#EDE8DE", "text": "#1C1B19",
        "variants": {
            "Moss": {"front": "#566658"},
            "Vermilion": {"front": "#AC3320"},
            "Dark": {"front": "#1C1B19", "back": "#64615E", "symbol": "#566658", "accent": "#566658"},
        },
    },
    "Tweed": {
        "bg": "#292B31", "text": "#D6D1C9",
        "variants": {
            "Tan": {"front": "#BDA07F"},
            "Brick": {"front": "#E77D6C"},
            "Dark": {"front": "#363840", "back": "#6B6B6E", "symbol": "#BDA07F", "accent": "#BDA07F"},
        },
    },
    "TweedDay": {
        "bg": "#E9E6E2", "text": "#2C2E34",
        "variants": {
            "Tan": {"front": "#76593D"},
            "Brick": {"front": "#B32A19"},
            "Dark": {"front": "#2C2E34", "back": "#655F58", "symbol": "#76593D", "accent": "#76593D"},
        },
    },
    "Blush": {
        "bg": "#F5E6D3", "text": "#35302A",
        "variants": {
            "Rose": {"front": "#9E4F5B"},
            "Crimson": {"front": "#A02B16"},
            "Dark": {"front": "#35302A", "back": "#756454", "symbol": "#9E4F5B", "accent": "#9E4F5B"},
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
    "K3Day": {
        "bg": "#E5E6E6", "text": "#1A1B1B",
        "variants": {
            "Steel": {"front": "#586065"},
            "Terracotta": {"front": "#B03316"},
            "Dark": {"front": "#1A1B1B", "back": "#616161", "symbol": "#586065", "accent": "#586065"},
        },
    },
    "CinderDay": {
        "bg": "#E8E3E3", "text": "#1B1A1A",
        "variants": {
            "Orange": {"front": "#A33D00"},
            "Brick": {"front": "#9E352E"},
            "Dark": {"front": "#1B1A1A", "back": "#626060", "symbol": "#A33D00", "accent": "#A33D00"},
        },
    },
    "BrassDay": {
        "bg": "#F4ECD6", "text": "#1D1C17",
        "variants": {
            "Sand": {"front": "#77603B"},
            "Brick": {"front": "#A63426"},
            "Dark": {"front": "#1D1C17", "back": "#67645B", "symbol": "#77603B", "accent": "#77603B"},
        },
    },
    "SorbetDay": {
        "bg": "#E9E2E9", "text": "#1B1A1B",
        "variants": {
            "Mint": {"front": "#1C685C"},
            "Rose": {"front": "#963653"},
            "Dark": {"front": "#1B1A1B", "back": "#635F63", "symbol": "#1C685C", "accent": "#1C685C"},
        },
    },
    "MonochromeDay": {
        "bg": "#E6E6E6", "text": "#1A1A1A",
        "variants": {
            "Silver": {"front": "#5C5C5C"},
            "Graphite": {"front": "#424242"},
            "Dark": {"front": "#1A1A1A", "back": "#616161", "symbol": "#E6E6E6", "accent": "#5C5C5C"},
        },
    },
    "BlushNight": {
        "bg": "#17130E", "text": "#DACCBC",
        "variants": {
            "Rose": {"front": "#CD7F8B"},
            "Crimson": {"front": "#E8735E"},
            "Dark": {"front": "#312D28", "back": "#66615A", "symbol": "#CD7F8B", "accent": "#CD7F8B"},
        },
    },
}
