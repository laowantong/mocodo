import json
import yaml
from pathlib import Path
import re

def convert(source: Path, target: Path):

    def finalize_regexes(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in ("match", "begin", "end"):
                    v = re.sub(r"\{\{(\w+)\}\}", lambda m: variables[m[1]], v)
                    d[k] = v.replace(" ", "") # Warning: suppresses spaces in regexes
                else:
                    finalize_regexes(v)
        elif isinstance(d, list):
            for i in d:
                finalize_regexes(i)

    def compress_single_key_dictionaries(json_text):
        return re.sub(r"(?m)^((?:\s*|.+: )\{)\n\s*(.+)\n\s*(\})", r"\1 \2 \3", json_text)

    data = yaml.safe_load(source.read_text())
    variables = data.pop("variables", {})
    for (k, v) in variables.items():
        variables[k] = re.sub(r"\{\{(\w+)\}\}", lambda m: variables[m[1]], v)
    finalize_regexes(data)
    json_text = json.dumps(data, indent=2)
    json_text = compress_single_key_dictionaries(json_text)
    target.write_text(json_text)

if __name__ == "__main__":
    # ~/.vscode/extensions/laowantong.vscode-mocodo
    DIR = Path("laowantong.vscode-mocodo/syntaxes")
    source = DIR / "mocodo.tmLanguage.yaml"
    target = DIR / "mocodo.tmLanguage.json"
    convert(source, target)
