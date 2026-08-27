import hashlib, math
def embed(text, dims=128):
    h = hashlib.sha256(text.encode()).digest()
    vals = [((h[i % len(h)] / 255.0) * 2 - 1) for i in range(dims)]
    n = math.sqrt(sum(v*v for v in vals)) or 1
    return [v/n for v in vals]
