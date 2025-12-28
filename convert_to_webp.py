#!/usr/bin/env python3
"""
Convert all images in the assets folder to WebP format for optimized web delivery.
"""

import os
from pathlib import Path
from PIL import Image
import sys

# Configuration
ASSETS_DIR = Path("assets")
QUALITY = 85  # Good balance between quality and file size
SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}


def convert_image_to_webp(input_path: Path, output_path: Path) -> bool:
    """Convert a single image to WebP format."""
    try:
        # Open and convert the image
        with Image.open(input_path) as img:
            # Convert RGBA for PNGs with transparency, RGB for others
            if img.mode in ("RGBA", "LA", "P"):
                # Preserve transparency
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            # Save as WebP
            img.save(
                output_path,
                "WEBP",
                quality=QUALITY,
                method=6  # Best compression method
            )

        # Get file sizes for comparison
        original_size = input_path.stat().st_size
        webp_size = output_path.stat().st_size
        reduction = ((original_size - webp_size) / original_size) * 100

        print(f"✓ {input_path.name:40s} {original_size/1024/1024:.2f}MB → {webp_size/1024/1024:.2f}MB ({reduction:.1f}% smaller)")
        return True

    except Exception as e:
        print(f"✗ Error converting {input_path.name}: {e}")
        return False


def main():
    """Main conversion function."""
    if not ASSETS_DIR.exists():
        print(f"Error: {ASSETS_DIR} directory not found!")
        sys.exit(1)

    # Find all image files
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(ASSETS_DIR.glob(f"*{ext}"))

    if not image_files:
        print(f"No image files found in {ASSETS_DIR}")
        sys.exit(0)

    print(f"Found {len(image_files)} image(s) to convert...\n")

    converted = 0
    skipped = 0
    failed = 0

    for img_path in sorted(image_files):
        # Create output path with .webp extension
        output_path = img_path.with_suffix(".webp")

        # Skip if WebP already exists and is newer than original
        if output_path.exists():
            if output_path.stat().st_mtime > img_path.stat().st_mtime:
                print(f"⊘ Skipping {img_path.name} (WebP already exists and is up-to-date)")
                skipped += 1
                continue

        # Convert the image
        if convert_image_to_webp(img_path, output_path):
            converted += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"Conversion complete!")
    print(f"  Converted: {converted}")
    print(f"  Skipped:   {skipped}")
    print(f"  Failed:    {failed}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()




