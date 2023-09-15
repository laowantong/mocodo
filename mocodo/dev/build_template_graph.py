from pathlib import Path
import os

from mocodo.tools import load_mini_yaml

def run():
    folder = Path(f"mocodo/resources/relation_templates")
    edges = []
    for path in sorted(folder.glob("*.yaml")):
        data = load_mini_yaml.run(path)
        color = "white" if len(data) < 6 else "yellow"
        if "parent" in data:
            edges.append(f'"{data["parent"]}" -> "{path.stem}"')
        edges.append(f'"{path.stem}" [fillcolor={color}]')
    edges = "\n  ".join(edges)
    result = f"digraph G {{\n  rankdir=LR\n  node [shape=box, style=filled]\n  {edges}\n}}\n"
    Path(folder, "_graph.gv").write_text(result)
    os.system(f"dot -Tsvg {folder}/_graph.gv > {folder}/_graph.svg")


if __name__ == "__main__":
    run()
