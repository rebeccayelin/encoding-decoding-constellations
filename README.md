# encoding-decoding-constellations
landing page for my 'constellations' exhibition



ffmpeg -i projection-2-2.mov \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -profile:v high -level 4.2 -pix_fmt yuv420p \
  -crf 22 -preset slow \
  -movflags +faststart \
  projection-2-2.mp4



- add photo credit for the one esther took
- populate video links (should it be youtube, or would mp4 be OK?)
- make a gallery image full width
- about section: note curator
- add an artist note + photo at the end + acknowledgements (CBA + Media Lab + CSAIL, etc. advisors)
- edit the lighting of some images
- script to convert to webp form
- change the carousel so the thumbnails are on the right instead
-