import os
import numpy as np
from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects
from PIL import Image, ImageEnhance, ImageFilter
from gtts import gTTS

# ==========================================
# CONFIGURATION & ASSETS
# ==========================================

# FILE MAPPING (Please verify which file corresponds to which description)
# Image 1: Orange hair, closed eyes, bold brows (Serene Confidence)
IMAGE_1_PATH = "1000893010.jpg" 
# Image 3 (Sequence 2): Pink eyeshadow, puckered lips (Playful Vibrancy)
IMAGE_3_PATH = "1000893009.jpg"
# Image 2 (Sequence 3): Branded powder brush shot (Brand Reveal)
IMAGE_2_PATH = "1000893008.jpg"

OUTPUT_FILENAME = "Idunu_Radiant_Touch_Ad.mp4"
VOICEOVER_FILENAME = "voiceover.mp3"
BG_MUSIC_FILENAME = "background_music.mp3" # Optional: Place a file named this in the dir

# DURATION SETTINGS (Total approx 40s)
CLIP_1_DURATION = 11
CLIP_2_DURATION = 11
CLIP_3_DURATION = 16  # Longer hold for CTA
TRANSITION_DURATION = 1.5

# TEXT CONTENT
TEXT_1 = "Flawless Brows & Glossy Lips"
TEXT_2 = "Vibrant Eyes & Bold Color"
TEXT_3_MAIN = "Idunu Radiant Touch"
TEXT_3_SUB = "Bring Out Your Inner Beauty"
TEXT_3_CTA = "BOOK NOW → 09031849960"
TEXT_3_SIG = "Oluwatosin CEO"

# COLORS & FONTS
GOLD_COLOR = "#D4AF37"
WHITE_COLOR = "#FFFFFF"
FONT_MAIN = "Times-Bold" # Standard Serif
FONT_SUB = "Times-Roman"

# VOICEOVER SCRIPT
VO_SCRIPT = (
    "Discover timeless beauty. "
    "With Idunu Radiant Touch, every look tells your story. "
    "Flawless coverage. Vibrant color. Radiant glow. "
    "Unleash the goddess within. "
    "Idunu Radiant Touch, Beauty that speaks. "
    "Book your transformation today: 09031849960."
)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def apply_cinematic_look(image_path):
    """
    Applies golden lighting, glow, and resize for 9:16 vertical video.
    Returns a numpy array suitable for MoviePy.
    """
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        # Create a black placeholder if file missing
        img = Image.new('RGB', (1080, 1920), color='black')

    # Resize to vertical 1080x1920 (cropping center)
    target_ratio = 9/16
    img_ratio = img.width / img.height
    
    if img_ratio > target_ratio:
        # Image is wider than target, crop width
        new_height = 1920
        new_width = int(new_height * img_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        left = (new_width - 1080) / 2
        img = img.crop((left, 0, left + 1080, 1920))
    else:
        # Image is taller/narrower, crop height
        new_width = 1080
        new_height = int(new_width / img_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        top = (new_height - 1920) / 2
        img = img.crop((0, top, 1080, top + 1920))

    # Apply Warm/Golden Filter
    # Enhance Color (Saturation)
    converter = ImageEnhance.Color(img)
    img = converter.enhance(1.2)
    
    # Enhance Brightness (slightly for glow)
    converter = ImageEnhance.Brightness(img)
    img = converter.enhance(1.05)
    
    # Warmth tint (simulate golden hour)
    # Split channels, boost Red slightly, reduce Blue slightly
    r, g, b = img.split()
    r = r.point(lambda i: i * 1.05)
    b = b.point(lambda i: i * 0.95)
    img = Image.merge('RGB', (r, g, b))

    # Soft Glow (Gaussian Blur overlay simulation)
    # We create a blurred copy and blend it
    glow = img.filter(ImageFilter.GaussianBlur(radius=10))
    img = Image.blend(img, glow, 0.2) # 20% blend for soft glow

    return np.array(img)


def create_ken_burns(clip, zoom_ratio=1.10):
    """
    Applies a slow zoom effect (Ken Burns).
    """
    w, h = clip.size
    
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size
        
        # Calculate current zoom level
        current_zoom = 1 + (zoom_ratio - 1) * (t / clip.duration)
        
        # Crop dimensions
        new_w = w / current_zoom
        new_h = h / current_zoom
        
        left = (w - new_w) / 2
        top = (h - new_h) / 2
        right = left + new_w
        bottom = top + new_h
        
        img_cropped = img.crop((left, top, right, bottom))
        img_resized = img_cropped.resize((w, h), Image.LANCZOS)
        
        return np.array(img_resized)

    return clip.fl(effect)


def generate_voiceover():
    """Generates a placeholder TTS file if one doesn't exist."""
    if not os.path.exists(VOICEOVER_FILENAME):
        print("Generating placeholder voiceover (Standard TTS)...")
        print("NOTE: For the specific 'African Baritone' voice, please replace 'voiceover.mp3' with your own recording.")
        tts = gTTS(text=VO_SCRIPT, lang='en', slow=False)
        tts.save(VOICEOVER_FILENAME)
    return AudioFileClip(VOICEOVER_FILENAME)


# ==========================================
# MAIN VIDEO GENERATION
# ==========================================

def main():
    print("Initializing Video Generation...")
    
    # 1. Prepare Image Clips
    # ----------------------
    print("Processing images...")
    
    # Clip 1
    arr1 = apply_cinematic_look(IMAGE_1_PATH)
    clip1 = ImageClip(arr1).set_duration(CLIP_1_DURATION)
    clip1 = create_ken_burns(clip1, zoom_ratio=1.05) # Subtle zoom in
    
    # Clip 2 (Image 3 in sequence)
    arr2 = apply_cinematic_look(IMAGE_3_PATH)
    clip2 = ImageClip(arr2).set_duration(CLIP_2_DURATION)
    clip2 = create_ken_burns(clip2, zoom_ratio=1.05) # Subtle zoom in
    
    # Clip 3 (Image 2 in sequence - Final Hold)
    arr3 = apply_cinematic_look(IMAGE_2_PATH)
    clip3 = ImageClip(arr3).set_duration(CLIP_3_DURATION)
    # Subtle pan for the last shot (simulated by cropping different parts usually, 
    # but simple zoom out works best for static images)
    clip3 = create_ken_burns(clip3, zoom_ratio=1.08) 

    # 2. Text Overlays
    # ----------------
    def create_text(txt, fontsize, color, y_pos, opacity=0.9, font=FONT_MAIN):
        return (TextClip(txt, fontsize=fontsize, color=color, font=font, method='caption', size=(900, None))
                .set_position(('center', y_pos))
                .set_opacity(opacity))

    # Text for Clip 1
    txt1 = create_text(TEXT_1, 50, WHITE_COLOR, 1500)
    txt1 = txt1.set_start(1).set_duration(CLIP_1_DURATION - 2).crossfadein(1).crossfadeout(1)
    
    # Text for Clip 2
    txt2 = create_text(TEXT_2, 50, WHITE_COLOR, 1500)
    txt2 = txt2.set_start(CLIP_1_DURATION + 1).set_duration(CLIP_2_DURATION - 2).crossfadein(1).crossfadeout(1)
    
    # Text for Clip 3 (Final Stack)
    start_t3 = CLIP_1_DURATION + CLIP_2_DURATION
    
    txt3_main = create_text(TEXT_3_MAIN, 70, GOLD_COLOR, 1200, font=FONT_MAIN)
    txt3_main = txt3_main.set_start(start_t3 + 1).set_duration(CLIP_3_DURATION - 1).crossfadein(2)
    
    txt3_sub = create_text(TEXT_3_SUB, 45, WHITE_COLOR, 1300, font=FONT_SUB)
    txt3_sub = txt3_sub.set_start(start_t3 + 2.5).set_duration(CLIP_3_DURATION - 2.5).crossfadein(2)
    
    txt3_cta = create_text(TEXT_3_CTA, 55, GOLD_COLOR, 1450, font=FONT_MAIN)
    txt3_cta = txt3_cta.set_start(start_t3 + 4).set_duration(CLIP_3_DURATION - 4).crossfadein(1)
    
    txt3_sig = create_text(TEXT_3_SIG, 30, WHITE_COLOR, 1600, font=FONT_SUB)
    txt3_sig = txt3_sig.set_start(start_t3 + 5).set_duration(CLIP_3_DURATION - 5).crossfadein(1)

    # 3. Compositing
    # --------------
    print("Compositing clips and transitions...")
    
    # Apply transitions
    # Note: Crossfadein on clip 2 and 3 overlaps with previous
    final_clip1 = CompositeVideoClip([clip1, txt1]).set_duration(CLIP_1_DURATION)
    
    final_clip2 = CompositeVideoClip([clip2, txt2]).set_duration(CLIP_2_DURATION)
    final_clip2 = final_clip2.crossfadein(TRANSITION_DURATION)
    
    final_clip3 = CompositeVideoClip([clip3, txt3_main, txt3_sub, txt3_cta, txt3_sig]).set_duration(CLIP_3_DURATION)
    final_clip3 = final_clip3.crossfadein(TRANSITION_DURATION)

    # Concatenate (using method='compose' implies we handle overlaps manually or use standard concat)
    # For crossfades to work in concat, we need to pad or use CompositeVideoClip for the whole timeline
    # Easier method:
    video = concatenate_videoclips([final_clip1, final_clip2, final_clip3], method="compose", padding=-TRANSITION_DURATION)

    # 4. Audio Mixing
    # ---------------
    print("Mixing audio...")
    
    # Voiceover
    vo_clip = generate_voiceover()
    # Ensure VO doesn't exceed video length
    if vo_clip.duration > video.duration:
        video = video.set_duration(vo_clip.duration + 2)
    
    # Background Music
    if os.path.exists(BG_MUSIC_FILENAME):
        bg_music = AudioFileClip(BG_MUSIC_FILENAME)
        # Loop music if too short, cut if too long
        if bg_music.duration < video.duration:
            bg_music = bg_music.loop(duration=video.duration)
        else:
            bg_music = bg_music.subclip(0, video.duration)
            
        bg_music = bg_music.volumex(0.15) # Low volume
        bg_music = bg_music.audio_fadeout(3)
        
        # Combine
        final_audio = CompositeAudioClip([bg_music, vo_clip])
    else:
        print("No background music found. Using Voiceover only.")
        final_audio = vo_clip

    video = video.set_audio(final_audio)

    # 5. Rendering
    # ------------
    print(f"Rendering {OUTPUT_FILENAME}...")
    video.write_videofile(
        OUTPUT_FILENAME, 
        fps=24, 
        codec='libx264', 
        audio_codec='aac',
        preset='medium',
        threads=4
    )
    print("Done! Video saved.")


if __name__ == "__main__":
    main()
