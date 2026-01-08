"""python
"""
import os
from gtts import gTTS

"""
Example script to generate a short example voiceover placeholder for the Idunu Radiant Touch project.

This script will create `voiceover_example.mp3` in the repository root using gTTS. You can replace the text or the filename as needed.

Usage:
    python examples/generate_voiceover_example.py

Requirements:
    pip install gTTS

Note: This script must be run locally (or in CI) because it uses network access to Google's TTS service.
"""

OUTPUT_FILENAME = "voiceover_example.mp3"
EXAMPLE_TEXT = (
    "This is an example voiceover for Idunu Radiant Touch. "
    "Replace this file with a professionally recorded African baritone voiceover for production. "
    "Book your transformation today: 09031849960."
)


def main():
    if os.path.exists(OUTPUT_FILENAME):
        print(f"{OUTPUT_FILENAME} already exists — remove it first if you want to regenerate.")
        return

    print("Generating example voiceover using gTTS...")
    tts = gTTS(text=EXAMPLE_TEXT, lang='en', slow=False)
    tts.save(OUTPUT_FILENAME)
    print(f"Saved example voiceover to {OUTPUT_FILENAME}")


if __name__ == '__main__':
    main()
