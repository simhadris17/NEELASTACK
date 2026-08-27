class MemoryManager:
    def __init__(self): self.items = []
    def add(self, text): self.items.append(text)
    def search(self, query):
        q = set(query.lower().split())
        return sorted(self.items, key=lambda x: len(q & set(x.lower().split())), reverse=True)[:5]
