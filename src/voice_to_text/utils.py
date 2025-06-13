from io import BytesIO
from typing import BinaryIO
import asyncio
from pydub import AudioSegment

async def bynary_to_ogg(binary: BinaryIO) -> bytes:
    loop = asyncio.get_running_loop()
    
    audio = await loop.run_in_executor(None, AudioSegment.from_file, binary)
    
    ogg_audio = BytesIO()
    await loop.run_in_executor(None, 
                             lambda: audio.export(ogg_audio, format="ogg"))
    ogg_audio.seek(0)
    return ogg_audio.read()