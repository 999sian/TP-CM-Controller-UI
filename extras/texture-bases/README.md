# Texture Base PNGs

These PNGs are creator reference files for **TP Classic Modern Controller UI**.

They are direct, pixel-for-pixel conversions of the BTI textures used by the mod. The conversion preserves the original button artwork, shadows, highlights, transparency, dimensions, and RGB5A3 color values. No resizing, filtering, repainting, or AI image generation is used.

## Folders

- `playstation/` — the BTIs stored in `res/buttons/`.
- `xbox/` — the Xbox prompt BTIs.
- `switch/` — the Nintendo Switch prompt BTIs generated from `assets/switch/`.
- `ornaments/` — HUD and menu ornament artwork.
- `internal/` — internal/reference artwork that is not normally a player-facing replacement target.

## Making a custom texture

1. Copy the PNG that is closest to the texture you want to customize.
2. Edit the copy in your image editor, keeping the transparent canvas and aspect ratio as a reference.
3. The final replacement may use a higher resolution if desired.
4. Rename the finished PNG or DDS to the exact Dusklight replacement filename listed in [`docs/texture-replacements.md`](../../docs/texture-replacements.md).
5. Put the renamed file in Dusklight's user `texture_replacements/` directory.

The filenames in this folder are intentionally human-readable reference names. **Do not use these reference filenames directly as Dusklight replacement filenames.** Use the hash-based filename from the replacement manifest.

## Repository only

This entire `extras/texture-bases/` directory is intentionally outside `res/`. It is **not packaged into the .dusk file** and does not increase the installed mod size.

## Keeping the bases current

After changing any BTI artwork, regenerate these PNGs with:

```sh
python tools/export_texture_reference_pngs.py --write
```

CI verifies that the committed reference PNGs still match the BTIs exactly.
