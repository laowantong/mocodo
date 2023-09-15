from pathlib import Path
from collections import defaultdict
import json

from mocodo.tools import load_mini_yaml

def run():
    template_folder_path = Path(f"mocodo/resources/relation_templates")
    aliases = defaultdict(list)
    metadata = defaultdict(dict)
    for path in sorted(template_folder_path.glob("*.yaml")):
        if "-" in path.name:
            continue
        data = load_mini_yaml.run(path)
        if "help" in data:
            metadata[path.stem] = {
                "category": "cv",
                "help": data["help"],
                "aliases": [],
            }
        elif "parent" in data:
            aliases[data["parent"]].append(path.stem)
        for (parent, children) in aliases.items():
            metadata[parent]["aliases"] = children
    result = json.dumps(metadata, indent=2, ensure_ascii=False)
    result = result.replace("[\n      ", "[")
    result = result.replace("\n    ]", "]")
    Path(template_folder_path, "_index.json").write_text(result + "\n")


if __name__ == "__main__":
    run()