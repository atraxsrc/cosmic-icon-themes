# Cosmic Icon Themes

Recolored builds of the Kanagawa icon pack by Fausto Korpsvart, matched to the cosmic-*-theme rices. Each theme comes in several folder colors taken from its own palette:

| Theme | Variants (first is the default) | Rice |
|---|---|---|
| DarkGold | Gold, Red, Dark | [cosmic-darkgold-theme](https://github.com/atraxsrc/cosmic-darkgold-theme) |
| Dossier | Rust, Olive, Ink | [cosmic-dossier-theme](https://github.com/atraxsrc/cosmic-dossier-theme) |
| K3 | Steel, Terracotta, Dark | [cosmic-k3-theme](https://github.com/atraxsrc/cosmic-k3-theme) |
| Monochrome | Silver, White, Dark | [cosmic-monochrome-theme](https://github.com/atraxsrc/cosmic-monochrome-theme) |
| Noir | Orange, Sage, Dark | [cosmic-noir-theme](https://github.com/atraxsrc/cosmic-noir-theme) |
| TokyoNight | Blue, Purple, Green, Dark | [cosmic-tokyonight-theme](https://github.com/atraxsrc/cosmic-tokyonight-theme) |
| TokyoDay | Blue, Purple, Green, Ink | [cosmic-tokyoday-theme](https://github.com/atraxsrc/cosmic-tokyoday-theme) |
| Ember | Ember, Moss, Slate, Dark | [cosmic-ember-theme](https://github.com/atraxsrc/cosmic-ember-theme) |
| EmberDay | Ember, Moss, Slate, Ink | [cosmic-emberday-theme](https://github.com/atraxsrc/cosmic-emberday-theme) |
| WhiteGold | Gold, Red, Slate, Ink | [cosmic-whitegold-theme](https://github.com/atraxsrc/cosmic-whitegold-theme) |
| Cinder | Orange, Brick, Dark | [cosmic-cinder-theme](https://github.com/atraxsrc/cosmic-cinder-theme) |
| Brass | Sand, Brick, Dark | [cosmic-brass-theme](https://github.com/atraxsrc/cosmic-brass-theme) |
| Sorbet | Mint, Rose, Dark | [cosmic-sorbet-theme](https://github.com/atraxsrc/cosmic-sorbet-theme) |
| Prism | Petal, Ruby, Dark | [cosmic-prism-theme](https://github.com/atraxsrc/cosmic-prism-theme) |
| PrismDay | Petal, Ruby, Dark | [cosmic-prismday-theme](https://github.com/atraxsrc/cosmic-prismday-theme) |
| Nebula | Teal, Rose, Dark | [cosmic-nebula-theme](https://github.com/atraxsrc/cosmic-nebula-theme) |
| NebulaDay | Teal, Rose, Dark | [cosmic-nebuladay-theme](https://github.com/atraxsrc/cosmic-nebuladay-theme) |
| Sumi | Moss, Vermilion, Dark | [cosmic-sumi-theme](https://github.com/atraxsrc/cosmic-sumi-theme) |
| SumiDay | Moss, Vermilion, Dark | [cosmic-sumiday-theme](https://github.com/atraxsrc/cosmic-sumiday-theme) |
| Tweed | Tan, Brick, Dark | [cosmic-tweed-theme](https://github.com/atraxsrc/cosmic-tweed-theme) |
| TweedDay | Tan, Brick, Dark | [cosmic-tweedday-theme](https://github.com/atraxsrc/cosmic-tweedday-theme) |
| Blush | Rose, Crimson, Dark | [cosmic-blush-theme](https://github.com/atraxsrc/cosmic-blush-theme) |

Symbolic and small icons take the theme's text color, so light themes stay readable.

## Previews

![DarkGold](previews/Cosmic-DarkGold.png)
![Dossier](previews/Cosmic-Dossier.png)
![K3](previews/Cosmic-K3.png)
![Monochrome](previews/Cosmic-Monochrome.png)
![Noir](previews/Cosmic-Noir.png)
![TokyoNight](previews/Cosmic-TokyoNight.png)
![TokyoDay](previews/Cosmic-TokyoDay.png)
![Ember](previews/Cosmic-Ember.png)
![EmberDay](previews/Cosmic-EmberDay.png)
![WhiteGold](previews/Cosmic-WhiteGold.png)
![Cinder](previews/Cosmic-Cinder.png)
![Brass](previews/Cosmic-Brass.png)
![Sorbet](previews/Cosmic-Sorbet.png)
![Prism](previews/Cosmic-Prism.png)
![PrismDay](previews/Cosmic-PrismDay.png)
![Nebula](previews/Cosmic-Nebula.png)
![NebulaDay](previews/Cosmic-NebulaDay.png)
![Sumi](previews/Cosmic-Sumi.png)
![SumiDay](previews/Cosmic-SumiDay.png)
![Tweed](previews/Cosmic-Tweed.png)
![TweedDay](previews/Cosmic-TweedDay.png)
![Blush](previews/Cosmic-Blush.png)

## Install

**With a rice:** each theme repo above has `./icons/install.sh`, which downloads its pack from the latest release, checks the SHA256 and sets it as the COSMIC icon theme:

```bash
./icons/install.sh                    # default folder color
./icons/install.sh --variant Red      # see --list
./icons/install.sh --system           # /usr/share/icons, all users + login screen (sudo)
```

**By hand:** download a pack from [Releases](https://github.com/atraxsrc/cosmic-icon-themes/releases/latest), then:

```bash
sha256sum -c --ignore-missing SHA256SUMS
tar -C ~/.local/share/icons -xJf Cosmic-Noir-Orange.tar.xz
```

Then pick the icon theme in COSMIC Settings > Desktop > Appearance > Icons. Restart open apps (COSMIC Files caches icons per window).

## Build

```bash
./scripts/fetch-upstream.sh
python3 -m cosmic_icons.build                                   # all 59 packs into dist/
python3 -m cosmic_icons.build --theme Noir                      # all Noir variants
python3 -m cosmic_icons.build --theme TokyoNight --variant Purple
python3 -m cosmic_icons.preview                                 # refresh previews/
./scripts/package.sh                                            # dist/release/*.tar.xz + SHA256SUMS
```

Each pack is about 89 MB unpacked (about 6 MB as `.tar.xz`), so build only what you use. A local build installs with `cp -a dist/Cosmic-Noir-Orange ~/.local/share/icons/`.

## Tests

```bash
python3 -m unittest discover -s tests -t . -v
```

## Credits and license

Based on the Kanagawa icon pack from https://github.com/Fausto-Korpsvart/Kanagawa-GKT-Theme (pinned commit in `scripts/fetch-upstream.sh`), which builds on Suru++ and Papirus. Full credits are kept in each pack's `index.theme`. Licensed GPL-3.0, see `LICENSE`.
