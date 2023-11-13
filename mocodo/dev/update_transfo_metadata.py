from pathlib import Path
from collections import defaultdict
import json
import os

from mocodo.argument_parser import init_localization, Transformations
from mocodo.tools import load_mini_yaml

# Build the index of templates

folder = Path(f"mocodo/resources/relation_templates")
aliases = defaultdict(list)
metadata = defaultdict(dict)
for path in sorted(folder.glob("*.yaml")):
    if "-" in path.name:
        continue
    data = load_mini_yaml.run(path)
    if "help_en" in data:
        metadata[path.stem] = {
            "category": "cv",
            "help_en": data["help_en"],
            "help_fr": data["help_fr"],
            "help_zh": data["help_zh"],
            "aliases": [],
        }
        if "fr_examples" in data:
            fr_examples = {}
            for d in data["fr_examples"]:
                fr_examples[d["example"]] = d["explanation"]
            metadata[path.stem]["fr_examples"] = fr_examples
    elif "parent" in data:
        aliases[data["parent"]].append(path.stem)
    for (parent, children) in aliases.items():
        metadata[parent]["aliases"] = children
result = json.dumps(metadata, indent=2, ensure_ascii=False)
result = result.replace("[\n      ", "[")
result = result.replace("\n    ]", "]")
result = result.replace(",\n      ", ", ")
Path(folder, "_index.json").write_text(result + "\n", encoding="utf8")
print(f"File written: {folder}/_index.json")

# Build the graph of templates

edges = []
for path in sorted(folder.glob("*.yaml")):
    data = load_mini_yaml.run(path)
    data.pop("help_fr", None)
    data.pop("help_en", None)
    data.pop("fr_examples", None)
    color = min(9, len(data))
    font_color = "white" if color > 5 else "black"
    if "parent" in data:
        edges.append(f'"{data["parent"]}" -> "{path.stem}"')
    edges.append(f'"{path.stem}" [fillcolor={color} fontcolor={font_color}]')
edges = "\n  ".join(edges)
result = f'digraph G {{\n  rankdir=LR\n  edge [dir="back"]\n  node [shape=box style="rounded,filled" colorscheme=reds9 fontname="Arial" penwidth=0]\n  {edges}\n}}\n'
path = Path(folder, "_graph.gv")
path.write_text(result, encoding="utf8")
os.system(f"dot -Tsvg {folder}/_graph.gv > {folder}/_graph.svg")
path.unlink()
print(f"File written: {folder}/_graph.svg")

# Build the cheat sheet

init_localization("fr")
metadata = Transformations("fr").metadata
tables = {}
for category in ["rw", "cv"]:
    rows = []
    rows.append(("Sous-option", "Description", "Exemples", "Explications"))
    rows.append((":--", ":--", ":--", ":--"))
    for (option, data) in sorted(metadata.items()):
        if data["category"] != category:
            continue
        title = f" title=\"Alias : {', '.join(data['aliases'])}.\"" if data.get("aliases") else ""
        option = f'<span{title} style="font-family:monospace; font-weight:600">{option}</span>'
        row = [option, data['help']]
        if not data.get(f"fr_examples"):
            rows.append(row + ["", ""])
            continue
        for (example, description) in data[f"fr_examples"].items():
            example = example.replace("\n", "\\n")
            example = f"`` {example} ``"
            row.extend([example, description])
            rows.append(row)
            row = ["", ""]  # empty cells for the first two columns
    tables[category] = "\n".join("| " + " | ".join(row) + " |" for row in rows)
text = f"""
### Opérations de conversion

{tables['cv']}

### Opérations de réécriture

{tables['rw']}
""".strip()
output_path = Path("doc/fr_cheat_sheet.md")
output_path.write_text(text, encoding="utf8")
print(f"File written: {output_path}")
