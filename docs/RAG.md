# RAG

Uploaded UTF-8 text documents are private to their owner and searchable through
`GET /rag/search?q=...`. Search escapes SQL wildcard characters, ranks filename
and content matches, and returns a contextual snippet and score. The dependency-
free chunker and in-memory vector store remain available for local pipelines.
