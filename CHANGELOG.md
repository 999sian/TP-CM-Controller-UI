# Changelog

## v1.4.0

- Added native Dusklight user texture replacement support for the mod's PlayStation, Xbox and Nintendo Switch controller artwork.
- Added replacement support for the custom HUD and menu ornaments.
- Added a generated manifest with the exact Dolphin-compatible replacement filename for every supported mod texture.
- Added a dependency-free manifest generator that calculates the same XXH64 source hash used by Dusklight/Aurora.
- Added CI validation so changing a BTI without updating its replacement manifest is caught before release.
- Custom replacement images can use higher resolutions while keeping the mod's existing HUD layout and calibration.
- Existing controller presets, mappings and calibration values are unchanged.


## v1.3.2

- Fixed Linux and Android crashes caused by game-structure ABI offsets being compiled into the mod.
- Updated the pinned Dusklight SDK so game-state accessors such as `dComIfGp_getPlayer()` use the exported game ABI instead of direct structure offsets.
- Public CI builds now use `Release` explicitly on every platform.
- Added CI checks to reject Linux/Android release libraries that contain `.debug_info` or inline the player lookup instead of importing the game ABI function.
- No controller layout or calibration changes are included in this release.


## v1.0.0 - Initial Release

- Initial release of **TP Classic Modern Controller UI**.
- Added PlayStation and Xbox controller prompts across the HUD and menus.
- Uses the original GameCube controls as the reference mapping for modern controller layouts.
- Added custom Twilight Princess-inspired UI elements, animations and controller customization options.
- Improved prompt scaling, positioning and visual consistency throughout the interface.
- Added official multi-platform build workflow using the Dusklight mod template.
