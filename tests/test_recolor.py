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
            "trash_top": "#7AA2F7",
            "trash_bottom": shade("#7AA2F7", 0.75),
        })

    def test_trash_puts_lighter_color_on_top(self):
        # Dark variants have a back tab lighter than the front panel.
        c = resolve(THEMES["DarkGold"], "Dark")
        self.assertEqual(c["trash_top"], "#7B7972")
        self.assertEqual(c["trash_bottom"], "#2A2A29")

    def test_trash_override(self):
        # White glyph needs a darker trash than the #DDDDDD folders.
        c = resolve(THEMES["Monochrome"], "White")
        self.assertEqual(c["trash_top"], "#828282")
        self.assertEqual(c["trash_bottom"], shade("#828282", 0.75))

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
