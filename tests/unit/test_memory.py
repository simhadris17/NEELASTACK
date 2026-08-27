def test_memory():
    from packages.neelastack.memory.manager import MemoryManager
    m=MemoryManager(); m.add('hello world'); assert m.search('hello')
