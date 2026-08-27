def trace(name):
    def deco(fn): return fn
    return deco
