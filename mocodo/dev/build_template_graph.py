from pathlib import Path
import os

from mocodo.tools import load_mini_yaml

folder = Path(f"mocodo/resources/relation_templates")
edges = []
for path in sorted(folder.glob("*.yaml")):
    data = load_mini_yaml.run(path)
    color = min(9, len(data))
    font_color = "white" if color > 5 else "black"
    if "parent" in data:
        edges.append(f'"{data["parent"]}" -> "{path.stem}"')
    edges.append(f'"{path.stem}" [fillcolor={color} fontcolor={font_color}]')
edges = "\n  ".join(edges)
result = f'digraph G {{\n  rankdir=LR\n  node [shape=box style="rounded,filled" colorscheme=reds9 fontname="Arial" penwidth=0]\n  {edges}\n}}\n'
path = Path(folder, "_graph.gv")
path.write_text(result)
os.system(f"dot -Tsvg {folder}/_graph.gv > {folder}/_graph.svg")
path.unlink()
