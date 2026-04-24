# encoding-decoding-constellations
landing page for my 'constellations' exhibition

## Image optimization

The site uses optimized images from `assets/web/`. Run `convert_to_webp.py` to generate them:

```bash
python convert_to_webp.py
```

- **Input:** Original JPG, PNG, JPEG in `assets/` (kept as-is)
- **Output:** `assets/web/` — WebP for modern browsers, resized JPG/PNG fallbacks for older browsers
- **Config** (in the script): `QUALITY = 78`, `MAX_DIMENSION = 2000` (capped for 1000px layout @ 2× retina)

Regenerate after changing settings:

```bash
python convert_to_webp.py --force
```

Requires: `pip install Pillow`

## Video optimization

The site uses optimized MP4s from `assets/videos/web/` and JPEG posters from
`assets/videos/posters/`. Generate them with:

```bash
python optimize_videos.py
```

Use `--force` to rebuild everything:

```bash
python optimize_videos.py --force
```

This keeps the source masters in `assets/videos/` and creates smaller web-sized
copies for GitHub Pages delivery.

---

ffmpeg -i outside.mov \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -profile:v high -level 4.2 -pix_fmt yuv420p \
  -crf 22 -preset slow \
  -movflags +faststart \
  outside.mp4


- edit the lighting of some images
- more photos but with faces blurred out? do i know how to do that?
