async def stream_text(text: str, chunk_size=32):
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]
