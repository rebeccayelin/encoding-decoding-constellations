#!/usr/bin/env python3
"""
Convert images in assets/ to optimized WebP and resized JPG/PNG for web delivery.
Originals are kept; output goes to assets/web/.
"""

from pathlib import Path
from PIL import Image
import sys

# Configuration
ASSETS_DIR = Path("assets")
OUTPUT_DIR = Path("assets/web")  # Web-optimized copies; originals stay in assets/
QUALITY = 78  # Slightly lower for smaller files; still sharp on web
MAX_DIMENSION = 2000  # Cap long side (good for 1000px layout @ 2x retina)
SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}


def prepare_image(input_path: Path):
    """Load, convert mode, and resize image. Returns (PIL Image, original_size)."""
    with Image.open(input_path) as img:
        original_size = input_path.stat().st_size
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        w, h = img.size
        if w > MAX_DIMENSION or h > MAX_DIMENSION:
            ratio = min(MAX_DIMENSION / w, MAX_DIMENSION / h)
            new_size = (int(w * ratio), int(h * ratio))
            try:
                resample = Image.Resampling.LANCZOS
            except AttributeError:
                resample = Image.LANCZOS
            img = img.resize(new_size, resample)

        return img, original_size


def convert_image(input_path: Path, webp_path: Path, fallback_path: Path) -> bool:
    """Convert a single image to WebP and resized fallback (JPG/PNG)."""
    try:
        img, original_size = prepare_image(input_path)
        ext = input_path.suffix.lower()

        # Save WebP
        img.save(webp_path, "WEBP", quality=QUALITY, method=6)
        webp_size = webp_path.stat().st_size

        # Save resized fallback in original format
        if ext in (".png", ".PNG"):
            img.save(fallback_path, "PNG", optimize=True)
        else:
            if img.mode == "RGBA":
                img = img.convert("RGB")
            img.save(fallback_path, "JPEG", quality=QUALITY, optimize=True)
        fallback_size = fallback_path.stat().st_size

        total_out = webp_size + fallback_size
        reduction = ((original_size - total_out) / original_size) * 100
        print(f"✓ {input_path.name:40s} {original_size/1024/1024:.2f}MB → webp {webp_size/1024/1024:.2f}MB + fallback {fallback_size/1024/1024:.2f}MB ({reduction:.1f}% smaller)")
        return True

    except Exception as e:
        print(f"✗ Error converting {input_path.name}: {e}")
        return False


def main():
    """Main conversion function."""
    force = "--force" in sys.argv or "-f" in sys.argv

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

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for img_path in sorted(image_files):
        webp_path = OUTPUT_DIR / img_path.with_suffix(".webp").name
        fallback_path = OUTPUT_DIR / img_path.name

        # Skip if both outputs exist and are newer than original (unless --force)
        if not force and webp_path.exists() and fallback_path.exists():
            if webp_path.stat().st_mtime > img_path.stat().st_mtime and fallback_path.stat().st_mtime > img_path.stat().st_mtime:
                print(f"⊘ Skipping {img_path.name} (web assets already up-to-date)")
                skipped += 1
                continue

        # Convert the image
        if convert_image(img_path, webp_path, fallback_path):
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




