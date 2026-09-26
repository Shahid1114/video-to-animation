
# Video → Animation (Free MVP)

## What it does
- Uploads MP4/MOV/MKV/AVI/WEBM/M4V
- Converts video to a cartoon/animation-style look using FFmpeg
- Keeps audio
- No paid AI API
- No artificial video-duration limit
- Mobile-friendly web UI

## Important
This is an animation-style filter, not a full generative AI rotoscoping model.
Long videos can take a long time and require enough disk space.

## Run on a PC/server
1. Install Python 3.10+.
2. Install FFmpeg and make sure `ffmpeg` works in your terminal.
3. Open this folder.
4. Run:
   pip install -r requirements.txt
5. Run:
   python app.py
6. Open http://127.0.0.1:5000

## Android
Pydroid 3 can run the Flask Python part, but FFmpeg availability on Android can vary.
For a reliable Android build, package an FFmpeg binary or use an Android-native wrapper.

## Improving quality later
A real AI animation version can use an open-source image-to-image/video pipeline, but it needs much more RAM/GPU and is substantially slower.
