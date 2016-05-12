import codecs

def read_contents(filename, encoding="utf8"):
    with codecs.open(filename, encoding=encoding) as f:
        return f.read()

def write_contents(filename, contents, encoding="utf8"):
    with codecs.open(filename, encoding=encoding, mode="w") as f:
        f.write(contents)
