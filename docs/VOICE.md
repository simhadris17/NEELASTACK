# VOICE

The API exposes authenticated `GET /voice`, `POST /voice/transcribe`, and
`POST /voice/synthesize` contracts. Browser speech recognition and synthesis are
the dependency-free fallback in the web chat. Server-side audio transcription
returns a clear `501` until a local Whisper/TTS engine is configured.
