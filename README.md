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
