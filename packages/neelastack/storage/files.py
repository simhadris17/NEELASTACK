from pathlib import Path
def save(root,name,data):
    p=Path(root)/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data); return str(p)
