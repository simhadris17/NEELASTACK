from pathlib import Path
class TextLoader:
    def load(self,path): return Path(path).read_text(encoding='utf-8')
