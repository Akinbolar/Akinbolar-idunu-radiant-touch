# Idunu Radiant Touch — Video Ad Generator

This repository contains a Python/MoviePy script to generate a vertical (9:16) promotional video ad for "Idunu Radiant Touch." The script applies cinematic color grading, Ken Burns effects, layered text overlays, and mixes voiceover and background music.

## Contents
- `generate_ad.py` (place the provided Python script here or rename as needed)
- `README.md` (this file)
- Image assets: `1000893010.jpg`, `1000893009.jpg`, `1000893008.jpg`
- Optional: `background_music.mp3`, `voiceover.mp3`

## Requirements
- Python 3.8+
- ffmpeg installed and available on PATH (MoviePy requires ffmpeg)

Python packages (install via pip):

```
pip install moviepy Pillow gTTS numpy
```

Or create a virtual environment and install with:

```
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

(If you want, I can add a `requirements.txt` file.)

## Usage
1. Place your image assets in the repository root or update the paths in the script.
2. Optionally add a higher-quality voiceover as `voiceover.mp3` to override the generated gTTS placeholder.
3. Optionally add background music as `background_music.mp3`.
4. Ensure `ffmpeg` is installed and on your PATH.
5. Run the script:

```
python generate_ad.py
```

The script will render `Idunu_Radiant_Touch_Ad.mp4` in the repository root.

## Configuration
Open `generate_ad.py` and confirm or change these constants at the top of the file:
- `IMAGE_1_PATH`, `IMAGE_3_PATH`, `IMAGE_2_PATH` — paths to your image files
- `OUTPUT_FILENAME` — output video filename
- `VOICEOVER_FILENAME` — path/name for the voiceover file (replace with your professional recording if available)
- `BG_MUSIC_FILENAME` — background music file
- Durations and transition length (e.g., `CLIP_1_DURATION`, `TRANSITION_DURATION`)
- Text strings (TEXT_1, TEXT_2, TEXT_3_MAIN, etc.) and color/font constants

Note on fonts: MoviePy's TextClip uses ImageMagick or the system fonts. If a requested font is unavailable, TextClip may fail; either install the font on the system or change the `FONT_MAIN`/`FONT_SUB` values.

## Voiceover
The script includes a fallback TTS via gTTS (Google Text-to-Speech). For professional quality, replace `voiceover.mp3` with a recorded African baritone voiceover and keep the same filename (or update the script path).

## Background Music
If `background_music.mp3` is present the script will mix it under the voiceover at low volume and fade out at the end. Make sure you have the right to use any music you include.

## Troubleshooting
- MoviePy errors about missing ffmpeg: install ffmpeg (https://ffmpeg.org/) and ensure it's on PATH.
- TextClip errors: install ImageMagick or use system fonts that exist; adjust the `font=` parameter.
- Large memory usage: rendering HD vertical videos can be memory intensive; reduce fps or resolution if needed.

## Next steps I can help with
- Add a `requirements.txt` and CI workflow to render on push
- Create a small example `voiceover.mp3` placeholder or instructions for recording
- Add a simple test that validates assets exist before rendering

## License
Add your preferred license. None provided by default.
