#!/usr/bin/env python3
"""
Create web-delivery MP4s and poster images for the site.

Original source videos remain in assets/videos/.
Optimized outputs are written to:
  - assets/videos/web/
  - assets/videos/posters/
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


VIDEO_DIR = Path("assets/videos")
OUTPUT_DIR = VIDEO_DIR / "web"
POSTER_DIR = VIDEO_DIR / "posters"
FPS = 24
CRF = 26
PRESET = "slow"
LANDSCAPE_MAX_WIDTH = 1440
PORTRAIT_MAX_WIDTH = 960
POSTER_TIME_SECONDS = 1
VIDEO_SUFFIX = ".mp4"


def require_binary(name: str) -> None:
    if shutil.which(name):
        return
    print(f"Error: {name} is required but was not found in PATH.")
    sys.exit(1)


def probe_dimensions(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    return int(stream["width"]), int(stream["height"])


def build_video_filter(width: int, height: int) -> tuple[str, int]:
    max_width = PORTRAIT_MAX_WIDTH if height > width else LANDSCAPE_MAX_WIDTH
    filters = [f"fps={FPS}"]
    if width > max_width:
        filters.append(f"scale={max_width}:-2:flags=lanczos")
    return ",".join(filters), max_width


def needs_refresh(source: Path, output: Path, force: bool) -> bool:
    if force or not output.exists():
        return True
    return output.stat().st_mtime < source.stat().st_mtime


def run(cmd: list[str]) -> None:
    subprocess.run(
        [
            cmd[0],
            "-hide_banner",
            "-loglevel",
            "error",
            "-nostats",
            *cmd[1:],
        ],
        check=True,
    )


def optimize_video(source: Path, output: Path, poster: Path, force: bool) -> str:
    width, height = probe_dimensions(source)
    video_filter, max_width = build_video_filter(width, height)
    refresh_video = needs_refresh(source, output, force)
    refresh_poster = needs_refresh(source, poster, force)

    if not refresh_video and not refresh_poster:
        return f"⊘ Skipping {source.name} (web assets already up-to-date)"

    if refresh_video:
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(source),
                "-an",
                "-vf",
                video_filter,
                "-c:v",
                "libx264",
                "-preset",
                PRESET,
                "-crf",
                str(CRF),
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(output),
            ]
        )
        if output.stat().st_size >= source.stat().st_size:
            shutil.copy2(source, output)

    if refresh_poster:
        poster_cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            str(POSTER_TIME_SECONDS),
            "-i",
            str(source),
            "-frames:v",
            "1",
            "-update",
            "1",
        ]
        if width > max_width:
            poster_cmd.extend(["-vf", f"scale={max_width}:-2:flags=lanczos"])
        poster_cmd.extend(["-q:v", "3", str(poster)])
        run(poster_cmd)

    original_size = source.stat().st_size
    optimized_size = output.stat().st_size if output.exists() else 0
    reduction = 100 - ((optimized_size / original_size) * 100) if original_size else 0
    return (
        f"✓ {source.name:20s} {original_size / 1024 / 1024:6.2f}MB"
        f" → {optimized_size / 1024 / 1024:6.2f}MB ({reduction:5.1f}% smaller)"
    )


def main() -> None:
    force = "--force" in sys.argv or "-f" in sys.argv

    require_binary("ffmpeg")
    require_binary("ffprobe")

    if not VIDEO_DIR.exists():
        print(f"Error: {VIDEO_DIR} directory not found.")
        sys.exit(1)

    sources = sorted(path for path in VIDEO_DIR.glob(f"*{VIDEO_SUFFIX}") if path.is_file())
    if not sources:
        print(f"No {VIDEO_SUFFIX} files found in {VIDEO_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    POSTER_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(sources)} video(s) to optimize...\n")
    for source in sources:
        output = OUTPUT_DIR / source.name
        poster = POSTER_DIR / f"{source.stem}.jpg"
        print(optimize_video(source, output, poster, force))


if __name__ == "__main__":
    main()
