# encoding-decoding-constellations
landing page for my 'constellations' exhibition



ffmpeg -i outside.mov \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -profile:v high -level 4.2 -pix_fmt yuv420p \
  -crf 22 -preset slow \
  -movflags +faststart \
  outside.mp4


- edit the lighting of some images
- more photos but with faces blurred out? do i know how to do that?