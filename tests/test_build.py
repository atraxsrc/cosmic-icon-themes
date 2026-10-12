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

    def test_dark_variant_trash_lighter_on_top(self):
        dest = self.build("DarkGold", "Dark")
        trash = (dest / "places/64/user-trash.svg").read_bytes()
        self.assertEqual(
            trash,
            b'<stop style="stop-color:rgb(123,121,114)"/><stop style="stop-color:rgb(42,42,41)"/>',
        )

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
