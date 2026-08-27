from .embeddings import embed


class InMemoryVectorStore:
    """Dependency-free vector store for local development and tests."""

    def __init__(self):
        self.items = []

    def add(self, text: str, metadata: dict | None = None):
        if not text or not text.strip():
            return
        self.items.append((embed(text), text, metadata or {}))

    def search(self, query: str, k: int = 5):
        """Return the original ``(embedding, text, metadata)`` shape."""
        if k <= 0:
            return []
        return sorted(self.items, key=lambda item: self._score(query, item[0]), reverse=True)[:k]

    def _score(self, query: str, vector):
        q = embed(query)
        return sum(a * b for a, b in zip(q, vector))

    def search_with_scores(self, query: str, k: int = 5):
        if k <= 0:
            return []
        return [
            {"text": text, "metadata": metadata, "score": self._score(query, item[0])}
            for item in sorted(self.items, key=lambda value: self._score(query, value[0]), reverse=True)[:k]
            for _, text, metadata in [item]
        ]
