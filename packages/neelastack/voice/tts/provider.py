from .base import TTSProvider
class LocalTTS(TTSProvider):
    async def synthesize(self,text): raise NotImplementedError('Connect a local TTS engine')
