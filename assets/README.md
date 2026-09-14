# Profile visuals

These images are self-contained and work as normal GitHub README image assets.
They make no network requests. The memory mosaic, model graph and build stages
are illustrative animations, not GitHub activity, real training metrics or CI results.

| File | Purpose |
| --- | --- |
| `retro-terminal.gif` | 8-second monochrome bitmap terminal and memory mosaic |
| `retro-terminal-static.png` | Complete still version of the terminal |
| `build-loop.gif` | 10-second illustrative build sequence |
| `build-loop-static.png` | Still version of the build sequence |
| `*.svg` | Repository and contact link badges |

To use still images, replace the `.gif` references in the root README with the
corresponding `-static.png` paths. GitHub also lets visitors disable GIF autoplay
in their accessibility settings.

## Regenerate

Use Python 3.10 or newer from the repository root:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/render_retro.py --out assets
python scripts/render_build.py --out assets
```

The retro renderer uses Pillow's bundled bitmap font. The build renderer tries
Monaco or DejaVu Sans Mono, then Pillow's bundled font; exact text appearance
can vary between operating systems. Both renderers check animation and grayscale
output. The SVG badges can be edited directly.
