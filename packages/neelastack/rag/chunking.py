def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if size <= 0:
        raise ValueError("size must be positive")
    if size <= overlap:
        raise ValueError("size must be > overlap")
    if not text:
        return []
    chunks = []
    start = 0
    step = size - overlap
    while start < len(text):
        end = min(len(text), start + size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start += step
    return chunks
