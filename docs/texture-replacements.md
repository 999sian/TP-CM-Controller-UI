# Custom Texture Replacements

TP Classic Modern Controller UI supports Dusklight's native user texture replacement system.
Create a PNG or DDS replacement, use the filename below, and place it in the user's `texture_replacements/` folder.

Enable **Texture Replacements** in Dusklight's graphics settings.

> Generated from the exact BTI resources shipped by the mod.
> After changing a BTI run `python tools/generate_texture_replacement_manifest.py --write`.

## Notes

- Dusklight matches the original texture by dimensions, GX format and XXH64 content hash.
- Replacement images may be higher resolution; keep the same aspect ratio for predictable HUD geometry.
- Removing the replacement restores the texture bundled with the mod.
- The mod intentionally keeps these as normal `res/` BTIs, not mod-owned `textures/` replacements, so the user's native replacements can win.
- If a base BTI changes, its replacement filename can change. CI verifies this manifest.
- Shared entries use the same source hash, so one replacement affects every context sharing that filename.

## PlayStation

| Texture | Replacement filename | Base resource | Notes |
| --- | --- | --- | --- |
| Cross | `tex1_128x128_3e54123cb4ecaa18_5.png` | `res/buttons/cross.bti` |  |
| Circle | `tex1_128x128_a5e729c7ac812df9_5.png` | `res/buttons/circle.bti` |  |
| Square | `tex1_128x128_cb0770ed5287fdc0_5.png` | `res/buttons/square.bti` |  |
| Triangle | `tex1_128x128_efa7c5331847519b_5.png` | `res/buttons/triangle.bti` |  |
| R1 | `tex1_128x64_3eef6db5e91b52cd_5.png` | `res/buttons/r1.bti` | Shared replacement hash. |
| R1 HUD | `tex1_128x64_3eef6db5e91b52cd_5.png` | `res/buttons/r1_hud.bti` | Shared replacement hash. |
| L3 | `tex1_128x128_de5a71facb5615ba_5.png` | `res/buttons/l3.bti` |  |
| Animated analog base | `tex1_128x128_cba447d454fe0656_5.png` | `res/buttons/animated_analog_base.bti` |  |
| Skill L3 overlay | `tex1_128x128_400c592450df8c99_5.png` | `res/buttons/skill_l3.bti` |  |
| Shop L3 overlay | `tex1_128x128_ddba1be34c6750d0_5.png` | `res/buttons/shop_l3_right.bti` |  |
| R3 | `tex1_128x128_54b5f4b307b51d30_5.png` | `res/buttons/r3.bti` |  |
| L2 | `tex1_128x96_3c1a209c2fd12805_5.png` | `res/buttons/l2.bti` |  |
| R2 | `tex1_128x96_6211d10ac9f70856_5.png` | `res/buttons/r2.bti` |  |
| Options | `tex1_128x128_f0386aa10a20accd_5.png` | `res/buttons/options.bti` |  |
| D-Pad | `tex1_128x128_317bb82cb2cd7f96_5.png` | `res/buttons/dpad.bti` |  |

## Xbox

| Texture | Replacement filename | Base resource | Notes |
| --- | --- | --- | --- |
| A | `tex1_128x128_b8f1c94c5a79215f_5.png` | `res/xbox/cross.bti` |  |
| B | `tex1_128x128_3c11c2793a584011_5.png` | `res/xbox/circle.bti` |  |
| X | `tex1_128x128_5dbd8bb31e151b1d_5.png` | `res/xbox/square.bti` |  |
| Y | `tex1_128x128_6add597c2abd89a6_5.png` | `res/xbox/triangle.bti` |  |
| RB | `tex1_128x64_5caeda085ab56596_5.png` | `res/xbox/r1.bti` | Shared replacement hash. |
| RB HUD | `tex1_128x64_5caeda085ab56596_5.png` | `res/xbox/r1_hud.bti` | Shared replacement hash. |
| L3 | `tex1_128x128_9f317f9be52ec0d1_5.png` | `res/xbox/l3.bti` |  |
| Animated analog base | `tex1_128x128_d63add593898019d_5.png` | `res/xbox/animated_analog_base.bti` | Shared with Switch. Shared replacement hash. |
| Skill L3 overlay | `tex1_128x128_9c0afe58a7346669_5.png` | `res/xbox/skill_l3.bti` | Shared with Switch. Shared replacement hash. |
| Shop L3 overlay | `tex1_128x128_02493dc9d3f52692_5.png` | `res/xbox/shop_l3_right.bti` | Shared with Switch. Shared replacement hash. |
| R3 | `tex1_128x128_63c66fe9189d8afa_5.png` | `res/xbox/r3.bti` |  |
| LT | `tex1_128x96_525bfc72b1138ff4_5.png` | `res/xbox/l2.bti` |  |
| RT | `tex1_128x96_50ead79d94dd9024_5.png` | `res/xbox/r2.bti` |  |
| Menu | `tex1_128x128_4c8bc9e47d2c156b_5.png` | `res/xbox/options.bti` |  |
| D-Pad | `tex1_128x128_50063108d5e05805_5.png` | `res/xbox/dpad.bti` |  |

## Nintendo Switch

| Texture | Replacement filename | Base resource | Notes |
| --- | --- | --- | --- |
| A | `tex1_128x128_153235550d47301c_5.png` | `res/switch/a.bti` |  |
| B | `tex1_128x128_d7aa333fb474cb2b_5.png` | `res/switch/b.bti` |  |
| Y | `tex1_128x128_f651f6f3ffb6335a_5.png` | `res/switch/y.bti` |  |
| X | `tex1_128x128_c5e5b1dd933bca15_5.png` | `res/switch/x.bti` |  |
| R | `tex1_128x64_2425bbc8201f59f3_5.png` | `res/switch/r.bti` | Shared replacement hash. |
| R HUD | `tex1_128x64_2425bbc8201f59f3_5.png` | `res/switch/r.bti` | Same texture as R. Shared replacement hash. |
| L Stick | `tex1_128x128_8b72b5b07f152afc_5.png` | `res/switch/l_stick.bti` |  |
| Animated analog base | `tex1_128x128_d63add593898019d_5.png` | `res/xbox/animated_analog_base.bti` | Shared with Xbox. Shared replacement hash. |
| Skill stick overlay | `tex1_128x128_9c0afe58a7346669_5.png` | `res/xbox/skill_l3.bti` | Shared with Xbox. Shared replacement hash. |
| Shop stick overlay | `tex1_128x128_02493dc9d3f52692_5.png` | `res/xbox/shop_l3_right.bti` | Shared with Xbox. Shared replacement hash. |
| R Stick | `tex1_128x128_77efdaceec3cd894_5.png` | `res/switch/r_stick.bti` |  |
| ZL | `tex1_128x96_3ddbe04b45831a84_5.png` | `res/switch/zl.bti` |  |
| ZR | `tex1_128x96_a48cdfc446ea7542_5.png` | `res/switch/zr.bti` |  |
| + | `tex1_128x128_6733f3814e9e2f77_5.png` | `res/switch/plus.bti` |  |
| D-Pad | `tex1_128x128_358db030326136ba_5.png` | `res/switch/dpad.bti` |  |

## Shared UI

| Texture | Replacement filename | Base resource | Notes |
| --- | --- | --- | --- |
| Menu ornament | `tex1_256x256_3c619db4dec78bef_5.png` | `res/ornament/menu_ornament.bti` |  |
| HUD ornament | `tex1_256x256_76e1dacce216c722_5.png` | `res/ornament/hud_ornament.bti` |  |
