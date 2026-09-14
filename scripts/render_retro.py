#!/usr/bin/env python3
"""Render a self-contained monochrome, pixel-terminal README animation.

Requires Python 3.10+ and Pillow 12.3.
Usage: python scripts/render_retro.py --out assets
Every numeric signal and moving cursor is an illustrative visual demo.
No external fonts, network requests, API tokens, or user activity are used.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

WIDTH, HEIGHT, SCALE = 600, 340, 2
FRAME_COUNT, FRAME_MS = 80, 100
BACKGROUND = 9
# Pillow bundles this classic 6x11 bitmap font. No system-specific paths.
try:
    FONT = ImageFont.load_default_imagefont()
except AttributeError:
    FONT = ImageFont.load_default()


def pixel_text(image: Image.Image, xy: tuple[int, int], text: str,
               color: int = 210, scale: int = 1) -> None:
    """Hard-edge bitmap glyphs, including when the fallback is a TTF."""
    box = FONT.getbbox(text)
    glyphs = Image.new("1", (max(1, box[2] + 2), max(1, box[3] + 2)), 0)
    ImageDraw.Draw(glyphs).text((0, 0), text, font=FONT, fill=1)
    if scale != 1:
        glyphs = glyphs.resize((glyphs.width * scale, glyphs.height * scale),
                               Image.Resampling.NEAREST)
    image.paste(color, xy, glyphs)


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    draw.rectangle(box, fill=BACKGROUND, outline=106)
    x0, y0, x1, _ = box
    draw.rectangle((x0 + 1, y0 + 1, x1 - 1, y0 + 18), fill=31)
    draw.line((x0, y0 + 19, x1, y0 + 19), fill=106)


ASSEMBLY = [
    "; x86-64 / Linux / NASM",
    "section .data",
    '  msg db "build. learn. repeat.", 10',
    "  len equ $ - msg",
    "section .text",
    "global _start",
    "_start:",
    "  mov eax, 1      ; SYS_write",
    "  mov edi, 1      ; stdout",
    "  lea rsi, [rel msg]",
    "  mov edx, len",
    "  syscall",
    "  mov eax, 60     ; SYS_exit",
    "  xor edi, edi",
    "  syscall",
]


def frame(number: int) -> Image.Image:
    image = Image.new("L", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    t = number / FRAME_COUNT
    # Square, old-workstation chrome. Identity is readable on frame zero.
    draw.rectangle((1, 1, 598, 338), outline=194)
    draw.rectangle((4, 4, 595, 19), fill=207)
    pixel_text(image, (10, 6), "MEDUCAE@WORKBENCH : TTY01", 9)
    pixel_text(image, (409, 6), "[ SYS ] [ MEM ] [ CODE ]", 9)
    pixel_text(image, (15, 31), "SOATMUROD XURRAMOV", 238, 3)
    pixel_text(image, (17, 68), "SOFTWARE ENGINEER  /  ANDROID  /  BACKEND  /  AI", 176)
    pixel_text(image, (17, 83), "> build. learn. repeat.", 231)
    pixel_text(image, (379, 83), "ASSEMBLY + MACHINE LEARNING", 148)

    # A small block cursor, with low-contrast pulse rather than on/off flashes.
    pulse = round(93 + 70 * (0.5 + 0.5 * math.sin(2 * math.pi * t)))
    draw.rectangle((157, 87, 162, 94), fill=pulse)
    # A retro geometric mark in the unused title margin.
    icon = ["1111111111", "1000000001", "1010110101", "1001101001",
            "1010010101", "1000000001", "1111111111", "0000110000",
            "0011111100"]
    for iy, row in enumerate(icon):
        for ix, value in enumerate(row):
            if value == "1":
                draw.rectangle((548 + ix * 3, 35 + iy * 3,
                                550 + ix * 3, 37 + iy * 3), fill=188)

    # Readable, real x86-64 source; animated selection is a code-study demo.
    panel(draw, (12, 107, 279, 304))
    pixel_text(image, (19, 111), "01 / BOOT.ASM", 237)
    pixel_text(image, (169, 111), "CODE STUDY", 155)
    selected = 7 + (number // 10) % 8
    for index, line in enumerate(ASSEMBLY):
        y = 132 + index * 10
        if index == selected:
            draw.rectangle((15, y + 1, 276, y + 10), fill=40)
            draw.rectangle((15, y + 2, 17, y + 9), fill=216)
        pixel_text(image, (23, y), f"{index + 1:02}", 91)
        pixel_text(image, (47, y), line,
                   133 if line.startswith(";") else 214)
    draw.line((20, 289, 270, 289), fill=58)
    pixel_text(image, (23, 292), "SOURCE -> OBJECT -> EXECUTABLE", 149)

    # A large square-cell memory mosaic. Deterministic gray byte values.
    panel(draw, (290, 107, 588, 229))
    pixel_text(image, (297, 111), "02 / MEMORY MOSAIC", 237)
    pixel_text(image, (549, 111), "DEMO", 153)
    for group in range(6):
        pixel_text(image, (334 + group * 36, 130), f"{group * 4:02X}", 118)
    cursor = int(t * 24) % 24
    levels = (28, 54, 85, 125, 174, 214)
    for row in range(8):
        pixel_text(image, (298, 143 + row * 9), f"{row * 24:04X}", 118)
        for col in range(24):
            value = ((col * 11) ^ (row * 19) ^ ((col // 4) * (row + 3))) % 6
            shade = levels[value]
            # One narrow scanning column and its tail change quietly.
            distance = (col - cursor) % 24
            if distance == 0:
                shade = min(242, shade + 63)
            elif distance == 23:
                shade = min(231, shade + 21)
            x, y = 334 + col * 9, 145 + row * 9
            draw.rectangle((x, y, x + 6, y + 6), fill=shade)
    pixel_text(image, (297, 218), f"ADDR 0x{cursor:04X}  /  24 x 8 CELLS  /  HEX", 144)

    # Square nodes and a pixel staircase loss graph: unmistakably synthetic.
    panel(draw, (290, 238, 588, 304))
    pixel_text(image, (297, 242), "03 / MODEL SIGNAL", 237)
    pixel_text(image, (519, 242), "SYNTHETIC", 153)
    nodes = [[(306, 271), (306, 280), (306, 289)],
             [(343, 267), (343, 276), (343, 285), (343, 294)],
             [(380, 273), (380, 288)]]
    for layer, following in zip(nodes, nodes[1:]):
        for x, y in layer:
            for xx, yy in following:
                draw.line((x, y, xx, yy), fill=51)
    for layer_index, layer in enumerate(nodes):
        for node_index, (x, y) in enumerate(layer):
            strength = .5 + .5 * math.sin(2 * math.pi * t - layer_index * 1.4 - node_index * .5)
            draw.rectangle((x - 2, y - 2, x + 2, y + 2), fill=round(101 + 117 * strength))
    draw.line((399, 260, 399, 299), fill=57)
    plot_x, plot_y = 413, 265
    draw.line((plot_x, plot_y, plot_x, 291, 577, 291), fill=86)
    for y in (273, 282):
        for x in range(416, 579, 4):
            draw.point((x, y), fill=45)
    points = []
    for index in range(32):
        x = plot_x + index * 5
        loss = .88 * math.exp(-index / 10.0) + .065
        y = 289 - round(loss * 23)
        if points:
            points.append((x, points[-1][1]))
        points.append((x, y))
    draw.line(points, fill=187, width=1)
    marker_index = int(t * 31)
    mx = plot_x + marker_index * 5
    my = 289 - round((.88 * math.exp(-marker_index / 10.0) + .065) * 23)
    draw.rectangle((mx - 1, my - 1, mx + 1, my + 1), fill=237)
    pixel_text(image, (413, 292), "LOSS / ILLUSTRATIVE", 131)

    # Numeric footer: no invented build success, CI runs, or live metrics.
    pixel_text(image, (14, 312), "[ VISUAL DEMO ]", 195)
    binary = f"{(0xA53C + (number // 4) * 0x13):016b}"
    pixel_text(image, (116, 312), binary, 130)
    pixel_text(image, (242, 312), f"0x{0x401000 + (number // 4) * 0x10:06X}", 153)
    pixel_text(image, (356, 312), "F1 HELP  F2 CODE  F3 MEMORY", 178)
    pixel_text(image, (14, 326), "MONO / PIXEL / REPEAT", 94)
    pixel_text(image, (410, 326), "MEDUCAE  //  LOCAL LAB", 94)

    # Nearest-neighbor scaling preserves crisp bitmap edges. Fine static
    # scanlines keep GIF size compact and avoid broad flashing or flicker.
    image = image.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.Resampling.NEAREST)
    scan = Image.new("L", image.size, 0)
    scan_draw = ImageDraw.Draw(scan)
    for y in range(1, image.height, 4):
        scan_draw.line((0, y, image.width - 1, y), fill=7)
    image = ImageChops.subtract(image, scan)
    # An identical palette for all frames guarantees monochrome output.
    palette = Image.new("P", (1, 1))
    palette.putpalette([channel for value in range(256) for channel in (value, value, value)])
    return image.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)


def build(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    frames = [frame(index) for index in range(FRAME_COUNT)]
    gif = out / "retro-terminal.gif"
    frames[0].save(gif, save_all=True, append_images=frames[1:],
                   duration=FRAME_MS, loop=0, optimize=True, disposal=1)
    frames[0].convert("RGB").save(out / "retro-terminal-static.png")
    with Image.open(gif) as rendered:
        assert rendered.n_frames == FRAME_COUNT
        duration = 0
        for index in range(rendered.n_frames):
            rendered.seek(index)
            duration += rendered.info.get("duration", 0)
            red, green, blue = rendered.convert("RGB").split()
            assert not ImageChops.difference(red, green).getbbox()
            assert not ImageChops.difference(red, blue).getbbox()
        assert duration == FRAME_COUNT * FRAME_MS
    assert ImageChops.difference(frames[0].convert("RGB"), frames[40].convert("RGB")).getbbox()
    assert gif.stat().st_size <= 1_500_000, "GIF exceeds the 1.5 MB budget"
    print(f"{gif}: {WIDTH*SCALE}x{HEIGHT*SCALE}, {FRAME_COUNT} frames, "
          f"{duration/1000:g}s, {gif.stat().st_size:,} bytes, strict grayscale")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("assets"))
    build(parser.parse_args().out)
