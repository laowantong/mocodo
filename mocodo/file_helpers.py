from pathlib import Path

def read_contents(path, encoding="utf8"):
    return Path(path).read_text(encoding=encoding)

def write_contents(path, contents, encoding="utf8"):
    Path(path).write_text(contents, encoding=encoding)
