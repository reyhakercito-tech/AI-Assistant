import os
import json
import requests
import torch
import torchaudio
import soundfile as sf
import platform
import subprocess
from TTS.api import TTS

# --- 1. LOAD CONFIGURATION ---
if not os.path.exists("config.json"):
    print("❌ Error: config.json not found. Please create it from the template.")
    exit(1)

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

NAME = config.get("character_name", "AI")
MODEL = config.get("model_name", "local-model")
LANGUAGE = config.get("language", "es")
THINKING_PHRASE = config.get("thinking_phrase", "Let me think...")
SYSTEM_PROMPT = config.get("system_prompt", "You are a helpful AI.")
SAMPLES = config.get("voice_samples", [])

# Map sample paths to the 'data' folder
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
sample_paths = [os.path.join(DATA_DIR, sample) for sample in SAMPLES]

# Verify samples exist
for path in sample_paths:
    if not os.path.exists(path):
        print(f"❌ Error: Voice sample '{path}' not found. Please place it in the '{DATA_DIR}' folder.")
        exit(1)

# --- 2. SCIENTIFIC COMPATIBILITY PATCHES (PYTORCH 2.6+) ---
_original_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load

def _patched_torchaudio_load(filepath, *args, **kwargs):
    data, samplerate = sf.read(filepath, dtype='float32')
    tensor = torch.from_numpy(data)
    if tensor.ndim == 1:
        tensor = tensor.unsqueeze(0)
    else:
        tensor = tensor.T
    return tensor, samplerate
torchaudio.load = _patched_torchaudio_load

# --- 3. AUDIO PLAYBACK HELPERS ---
IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    import winsound

def play_thinking_audio(filepath):
    if IS_WINDOWS:
        winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)

def stop_thinking_audio():
    if IS_WINDOWS:
        winsound.PlaySound(None, winsound.SND_PURGE)

def play_response_audio(filepath):
    if IS_WINDOWS:
        winsound.PlaySound(filepath, winsound.SND_FILENAME)
    elif platform.system() == "Darwin": # macOS
        subprocess.run(["afplay", filepath])
    else: # Linux
        subprocess.run(["aplay", filepath])

# --- 4. SYSTEM INITIALIZATION ---
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

print(f"🎙️ Getting ready {NAME}'s voice cords (XTTS v2)...")
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)

audio_pensando = os.path.join(DATA_DIR, f"{NAME.lower()}_thinking.wav")
archivo_salida = os.path.join(DATA_DIR, f"{NAME.lower()}_response.wav")

if not os.path.exists(audio_pensando):
    print("⏳ Creating voice file for thought transitions...")
    tts.tts_to_file(text=THINKING_PHRASE, speaker_wav=sample_paths, language="en", file_path=audio_pensando)

# --- 5. MAIN LOOP ---
def chat_with_character():
    print("\n========================================================")
    print(f"🔬 OPERATING SYSTEM! Talk to {NAME} (Type 'exit' to finish) 🔬")
    print("========================================================\n")
    
    historial_chat = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print(f"🚀 {NAME}: Shutting down...")
            break
            
        if not user_input.strip():
            continue
            
        historial_chat.append({"role": "user", "content": user_input})
        
        play_thinking_audio(audio_pensando)
        
        payload = {
            "model": MODEL,
            "messages": historial_chat,
            "temperature": 0.6,
            "stream": False
        }
        
        try:
            respuesta = requests.post(LM_STUDIO_URL, json=payload, headers={"Content-Type": "application/json"})
            respuesta.raise_for_status()
            
            texto_original = respuesta.json()['choices'][0]['message']['content']
            
            if "</think>" in texto_original:
                texto_final = texto_original.split("</think>")[-1].strip()
            else:
                texto_final = texto_original.strip()
                
            print(f"🧠 ({NAME} processed internal logic)")
            print(f"🗣️ {NAME}: {texto_final}\n")
            
            stop_thinking_audio()
            
            tts.tts_to_file(
                text=texto_final,
                speaker_wav=sample_paths,
                language=LANGUAGE,
                file_path=archivo_salida
            )
            
            play_response_audio(archivo_salida)
            
            historial_chat.append({"role": "assistant", "content": texto_original})
            
        except requests.exceptions.ConnectionError:
            stop_thinking_audio()
            print("\n❌ Error: LM Studio server is offline. Turn it on at port 1234.")
            break
        except Exception as e:
            stop_thinking_audio()
            print(f"\n❌ An error occurred: {e}")
            break

if __name__ == "__main__":
    chat_with_character()