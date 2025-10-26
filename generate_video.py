# generate_video.py
# Génère une courte vidéo verticale (9:16) avec texte et voix.
from gtts import gTTS
from moviepy.editor import *
from datetime import datetime
import random
import os

# --- CONFIGURATION (modifiable) ---
DURATION_SECONDS = 12          # durée totale de la vidéo
WIDTH, HEIGHT = 720, 1280      # vertical 9:16 pour TikTok
FPS = 24
VOICE_LANG = "fr"              # français
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Choix des types de vidéos
THEMES = {
    "faits": [
        "Le poulpe a trois cœurs et du sang bleu. Impressionnant, non ?",
        "Les fourmis n'ont pas de poumons — elles respirent par de petits trous sur leur corps.",
        "Une seule cuillère de terre contient plus d'êtres vivants que d'humains sur la planète."
    ],
    "citations": [
        "Ne laisse jamais les autres éteindre ta curiosité.",
        "Le courage, c'est de chercher la vérité et de la dire.",
        "Apprends comme si tu allais vivre toujours, vis comme si tu allais mourir demain."
    ],
    "mystere": [
        "Ils ont trouvé une maison abandonnée où toutes les horloges étaient arrêtées à 3h13.",
        "Un téléphone sonne dans une forêt vide — mais aucun signal n'arrive à l'adresse indiquée."
    ],
}

# Choisir un thème aléatoire et une phrase aléatoire
theme = random.choice(list(THEMES.keys()))
text = random.choice(THEMES[theme])

# Ajouter la date
today = datetime.utcnow().strftime("%d %b %Y")
full_text = f"{text}\n\n— {today}"

# --- Créer l'audio ---
tts = gTTS(full_text, lang=VOICE_LANG)
audio_path = os.path.join(OUTPUT_DIR, "speech.mp3")
tts.save(audio_path)

# --- Créer la vidéo ---
bg = ColorClip(size=(WIDTH, HEIGHT), color=(18, 24, 50)).set_duration(DURATION_SECONDS)
txt_clip = TextClip(full_text, fontsize=48, font='DejaVu-Sans', color='white', method='caption', size=(WIDTH*0.9, None))
txt_clip = txt_clip.set_position(("center","center")).set_duration(DURATION_SECONDS)

audio = AudioFileClip(audio_path)
audio = audio.set_duration(DURATION_SECONDS)

video = CompositeVideoClip([bg, txt_clip]).set_audio(audio)
video = video.set_fps(FPS)
video = video.fx(vfx.fadein, 0.6).fx(vfx.fadeout, 0.8)

out_name = f"tiktok_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.mp4"
out_path = os.path.join(OUTPUT_DIR, out_name)
video.write_videofile(out_path, codec="libx264", audio_codec="aac", threads=2, verbose=False)

print("VIDEO_CREATED:", out_path)
