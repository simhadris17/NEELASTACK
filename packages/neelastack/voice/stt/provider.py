from .base import STTProvider
class LocalSTT(STTProvider):
    async def transcribe(self,audio): raise NotImplementedError('Connect a local STT engine such as whisper.cpp/faster-whisper')
