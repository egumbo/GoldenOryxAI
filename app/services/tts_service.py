import uuid
import os
import asyncio
import edge_tts

VOICE = "en-US-GuyNeural"

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


async def generate_audio_async(text: str, filename: str):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)


async def text_to_speech_background(text: str) -> str:
    filename = f"{AUDIO_DIR}/{uuid.uuid4()}.mp3"

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

    return filename
