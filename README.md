# TP Classic Modern Controller UI

## Experimental Xbox One S port

**[Download Xbox installer](https://github.com/999sian/dusklight/releases/tag/v2.0.3-xbox-mod-ports.1006)** · [UWP bundle for developers](https://github.com/999sian/TP-CM-Controller-UI/releases/tag/v1.4.0-xbox.1)

This fork builds **TP Classic Modern Controller UI 1.4.0** with the Xbox Dusklight host.
It must be bundled inside a signed Xbox MSIX; copying a desktop `.dusk` into
app data will not work. The Windows/UWP build and a separate 30-second Xbox One S startup test passed.
Gameplay compatibility is not yet confirmed.

[Simple Xbox setup and test results](https://github.com/999sian/dusklight/blob/xbox-mod-ports/docs/xbox-native-mod-ports.md)

[Build progress](https://github.com/999sian/dusklight/actions/runs/39714675293)


**Modern controller prompts, reimagined in the style of Twilight Princess.**

TP Classic Modern Controller UI modernizes the controller interface of **The Legend of Zelda: Twilight Princess** by combining the original game's visual language with custom UI elements designed for modern controllers.

The mod does not aim to reproduce the original HUD exactly. It keeps the recognizable Twilight Princess aesthetic while introducing its own visual identity where appropriate, including custom ornamentation, redesigned controller prompts, and additional presentation options.

## Features

- PlayStation, Xbox and Nintendo Switch controller prompt support.
- Modern controller prompts across the HUD, menus, dialogues, maps, Item Wheel, shops, skills and save screens.
- Custom Twilight Princess-inspired ornamentation and UI elements.
- Animated analog-stick prompts using the game's native animation system.
- Configurable positioning, scaling, glow and animation behavior for multiple UI elements.
- D-Pad customization and related ITEM / MAP presentation controls.

## Controller Mapping

The GameCube column below represents the **original in-game controls used as the reference mapping**. GameCube controller prompts are not an additional supported controller preset; the mod adds modern prompt sets for PlayStation, Xbox and Nintendo Switch.

| Original GameCube Control | PlayStation | Xbox | Nintendo Switch |
| --- | --- | --- | --- |
| A | Cross | A | B |
| B | Circle | B | A |
| X | Triangle | Y | X |
| Y | Square | X | Y |
| Z | R1 | RB | R |
| R | R2 | RT | ZR |
| L | L2 | LT | ZL |
| Start | Options | Menu | + |

The mapping follows the **function of the original GameCube controls**, rather than matching button letters between controllers.

## Custom Texture Replacements

Starting with v1.4.0, the mod's own PlayStation, Xbox, Nintendo Switch and ornament textures can be replaced through Dusklight's native user texture-replacement system.

Place a PNG or DDS with the matching Dolphin-style filename in the user's `texture_replacements/` folder and keep **Texture Replacements** enabled in Dusklight's graphics settings. The mod keeps its controller artwork as normal BTI resources rather than registering higher-priority mod-owned replacements, so user replacements can override the selected prompt without changing layout calibration or editing the `.dusk` file.

The exact filenames are generated from the BTIs shipped with each version. See [Custom Texture Replacements](docs/texture-replacements.md) for the complete PlayStation, Xbox, Nintendo Switch and ornament manifest.

For creators, the repository also includes [reference PNGs converted directly from the original BTIs](extras/texture-bases/README.md). These preserve the original artwork, shadows, highlights, transparency and dimensions, making them a practical base for custom prompt designs. They live under `extras/` and are **not included in the .dusk bundle**.

Game texture packs remain compatible and can be used at the same time.

## Platform Support

This repository uses the official Dusklight native mod template workflow. CI builds the mod for all platforms supported by that template and merges them into one distributable `.dusk` bundle:

- Windows AMD64 and ARM64
- Linux x86_64 and ARM64
- macOS Apple Silicon and Intel
- iOS ARM64
- Android ARM64

Local builds are platform-specific and are intended for testing only. For distribution, use the **`mod-combined`** artifact produced by GitHub Actions.

## Building

A local test build can be created with:

```sh
cmake -B build
cmake --build build
```

The local bundle is written to `build/mods/tp_classic_modern_controller_ui.dusk`.

For a distributable build, push the repository to GitHub and let the included GitHub Actions workflow build every supported platform and create the combined bundle.

## Credits

**Created by XandasLegend.**

Special thanks to the developers and contributors of **Dusklight** and the wider Twilight Princess modding community.

## AI Disclaimer

AI tools were used during parts of development to assist with code analysis, debugging, documentation, naming, and workflow support. Final design decisions, testing, integration, asset selection, configuration, and release decisions were reviewed and carried out by the project author.

AI-assisted output does not represent Nintendo, the Dusklight developers, or any other third party.

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE).
