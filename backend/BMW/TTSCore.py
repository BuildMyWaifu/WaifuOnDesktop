from typing import Literal
from io import BytesIO
import asyncio
import edge_tts

AVAILABLE_VOICE = Literal["girl", "boy"]

# Map 
VOICE_MAPPING = {
    "girl": "zh-CN-XiaoxiaoNeural",  
    "boy": "zh-CN-YunxiNeural",     
}

async def tts(voice: AVAILABLE_VOICE, text: str) -> BytesIO:
    """
    Asynchronous TTS function that generates audio and returns BytesIO.
    :param voice: "girl" for female voice or "boy" for male voice
    :param text: The text to convert to speech
    :return: BytesIO object containing the audio data
    """
    # Ensure valid voice input
    if voice not in VOICE_MAPPING:
        raise ValueError(f"Invalid voice selection: {voice}. Choose 'girl' or 'boy'.")

    # Map the voice input to the Azure TTS voice
    selected_voice = VOICE_MAPPING[voice]

    # Use Edge TTS to generate audio
    communicate = edge_tts.Communicate(text, selected_voice)
    audio_buffer = BytesIO()  # Buffer to hold audio data
    print(f"Generating speech for text: '{text}' with voice: {voice} ({selected_voice})")

    # Save the audio to BytesIO buffer
    async for chunk in communicate.stream():
        audio_buffer.write(chunk)

    # Reset the buffer's position to the start for reading
    audio_buffer.seek(0)
    return audio_buffer


# Example 
if __name__ == "__main__":
    async def main():
        text = "你好，我是毛，虽然是测试的语音，但是最希望你了！"  

        # Girl
        girl_audio = await tts("girl", text)
        with open("girl_voice.wav", "wb") as f:
            f.write(girl_audio.read())  # Save audio file
        print("Female voice audio saved as 'girl_voice.wav'.")

        # Boy
        boy_audio = await tts("boy", text)
        with open("boy_voice.wav", "wb") as f:
            f.write(boy_audio.read())  # Save audio file
        print("Male voice audio saved as 'boy_voice.wav'.")

    asyncio.run(main())
