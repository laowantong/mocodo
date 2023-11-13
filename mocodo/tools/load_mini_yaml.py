from ast import literal_eval
import re

def parse_value(v):
    v = v.strip()
    if v.startswith("'"):
        if v != "''":
            v = v.replace("''", "\\'")
        v = literal_eval(f"r{v}")
        v = v.replace("\\'", "'")
        v = re.sub(r"(?<!\\)\\n", "\n", v) # replace \n into newline, except if preceded by \
        v = v.replace(r"\\n", r"\n") # replace stuff like \\newcommand into \newcommand
        v = re.sub(r"(?<!\\)\\t", "\t", v) # idem for \t
        v = v.replace(r"\\t", r"\t") # idem for \t
        v = v.replace("\\xa0", '\xa0') # replace \xa0 into non-breaking space
        return v
    elif v.lower() == "true":
        return True
    elif v.lower() == "false":
        return False
    elif v.lower() == "null":
        return None
    elif v:
        return literal_eval(v)
    else:
        return []

def run(path):
    text = path.read_text(encoding="utf8")
    data = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        (k1, v1) = re.match(r"(\S+?) *: *(.*?) *$", line).groups()
        data[k1] = parse_value(v1)
        if data[k1] == []: # list of dicts
            while i < len(lines):
                line = lines[i]
                (prefix, k2, v2) = re.match(r"([- ]*)(\w+?) *: *(.*?) *$", line).groups()
                if prefix == "  - ": # new dict
                    data[k1].append({k2: parse_value(v2)})
                    i += 1
                elif prefix == "    ": # continuation of previous dict
                    data[k1][-1][k2] = parse_value(v2)
                    i += 1
                else:
                    break
    return data
