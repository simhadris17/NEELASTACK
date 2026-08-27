def test_rag():
    from packages.neelastack.rag.embeddings import embed
    assert len(embed('hello')) == 128
