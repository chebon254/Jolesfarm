#!/usr/bin/env python3
"""
Generates JPEG thumbnails and WebP versions for all gallery images.
Output goes to images/gallery/thumbs/ — originals are never modified.

Usage: python3 scripts/optimize-gallery.py
"""

import os
from pathlib import Path
from PIL import Image

GALLERY_DIR = Path(__file__).parent.parent / "images" / "gallery"
THUMBS_DIR = GALLERY_DIR / "thumbs"
MAX_WIDTH = 800
JPEG_QUALITY = 75
WEBP_QUALITY = 80

THUMBS_DIR.mkdir(exist_ok=True)

sources = sorted(
    f for f in GALLERY_DIR.iterdir()
    if f.suffix.lower() in (".jpg", ".jpeg") and f.parent == GALLERY_DIR
)

total = len(sources)
print(f"Processing {total} images...")

for i, src in enumerate(sources, 1):
    stem = src.stem  # e.g. "jolesfarm87"
    jpg_out = THUMBS_DIR / f"{stem}.jpg"
    webp_out = THUMBS_DIR / f"{stem}.webp"

    if jpg_out.exists() and webp_out.exists():
        print(f"[{i}/{total}] skip {src.name} (already done)")
        continue

    with Image.open(src) as img:
        img = img.convert("RGB")
        # Resize only if wider than MAX_WIDTH
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_size = (MAX_WIDTH, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        img.save(jpg_out, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        img.save(webp_out, "WEBP", quality=WEBP_QUALITY, method=6)

    print(f"[{i}/{total}] {src.name} -> {jpg_out.name} + {webp_out.name}")

print(f"\nDone. Thumbnails saved to: {THUMBS_DIR}")
