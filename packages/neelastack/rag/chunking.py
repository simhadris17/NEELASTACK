def chunk_text(text, size=800, overlap=100):
    if size <= overlap: raise ValueError("size must be > overlap")
    out=[]; start=0
    while start < len(text):
        out.append(text[start:start+size]); start += size-overlap
    return out
