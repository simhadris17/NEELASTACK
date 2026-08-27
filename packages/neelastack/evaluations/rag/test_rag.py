def test_chunking():
    from packages.neelastack.rag.chunking import chunk_text
    assert chunk_text('abcdef',4,1)
