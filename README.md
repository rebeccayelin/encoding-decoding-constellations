# encoding-decoding-constellations
landing page for my 'constellations' exhibition



ffmpeg -i projection-2-2.mov \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -profile:v high -level 4.2 -pix_fmt yuv420p \
  -crf 22 -preset slow \
  -movflags +faststart \
  projection-2-2.mp4



- populate video links (should it be youtube, or would mp4 be OK?)
- make a gallery image full width
- about section: note curator
- edit the lighting of some images
- more photos but with faces blurred out? do i know how to do that?