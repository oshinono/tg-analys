from config import settings
from io import BytesIO
from httpx import AsyncClient

class WhisperService:
    api_key = settings.hugging_face_api_key
    whisper_url = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"

    @classmethod
    async def transcribe(cls, raw_audio: bytes) -> str:
        async with AsyncClient() as client:
            response = await client.post(
                url=cls.whisper_url,
                content=raw_audio,
                headers={'Authorization': f"Bearer {cls.api_key}", "Content-Type": "audio/ogg"}
            )

        if response.status_code == 200:
            return response.json()['text']
        else:
            raise Exception(f"Failed: {response.status_code} {response.text}")

    @classmethod
    async def change_api_key(cls, new_api_key: str):
        cls.api_key = new_api_key