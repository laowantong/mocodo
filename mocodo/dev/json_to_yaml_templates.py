from pathlib import Path
from json import loads

def repr_single(s):
    """repr() but with single quotes"""
    return "'" + repr('"' + s)[2:]

def convert(source_path, target_path):
    for path in sorted(source_path.glob("*.json"), reverse=True):
        print(path)
        data = loads(path.read_text(encoding="utf8"))
        result = []
        for (key, stuff) in data.items():
            if isinstance(stuff, str):
                stuff = repr_single(stuff).replace(r"\\", "\\").replace("\\'", "''")
                result.append(f"{key}: {stuff}")
            elif isinstance(stuff, list):
                result.append(f"{key}:")
                for d in stuff:
                    sub_result = []
                    for (k, v) in d.items():
                        if isinstance(v, str):
                            v = repr_single(v).replace(r"\\", "\\").replace("\\'", "''")
                        else:
                            v = str(v)
                        sub_result.append(f"{k}: {v}")
                    result.append("  - " + "\n    ".join(sub_result))
            elif isinstance(stuff, bool):
                result.append(f"{key}: {str(stuff).lower()}")
            elif stuff is None:
                result.append(f"{key}: null")
            else:
                result.append(f"{key}: {stuff}")
        result.append("")
        dest = Path(target_path, path.stem + ".yaml")
        dest.write_text("\n".join(result), encoding="utf8")

if __name__ == "__main__":
    convert(Path("test/test_data/templates"), Path("test/test_data/new_templates"))
