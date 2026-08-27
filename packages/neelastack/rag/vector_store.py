from .embeddings import embed
class InMemoryVectorStore:
    def __init__(self): self.items=[]
    def add(self, text, metadata=None): self.items.append((embed(text), text, metadata or {}))
    def search(self, query, k=5):
        q=embed(query)
        def score(v): return sum(a*b for a,b in zip(q,v))
        return sorted(self.items, key=lambda x: score(x[0]), reverse=True)[:k]
