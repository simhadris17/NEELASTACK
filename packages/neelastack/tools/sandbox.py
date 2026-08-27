from pathlib import Path
def safe_path(root: str, requested: str) -> Path:
    base = Path(root).resolve()
    target = (base / requested).resolve()
    if base not in target.parents and target != base: raise PermissionError("Path escapes sandbox")
    return target
