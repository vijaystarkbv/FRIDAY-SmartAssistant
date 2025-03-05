import edge_tts
import asyncio

async def test():
    voice = "en-US-AriaNeural"  # Microsoft's safest voice
    communicate = edge_tts.Communicate("Testing Edge-TTS.", voice)
    await communicate.save("test_audio.mp3")

asyncio.run(test())
