from packages.neelastack.tools.sandbox import safe_path
def read_text(root, path):
    return safe_path(root, path).read_text(encoding="utf-8")
