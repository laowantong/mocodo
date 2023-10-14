from pathlib import Path

from mocodo.argument_parser import init_localization, Transformations

init_localization("fr")
metadata = Transformations("fr").metadata
aliases = {}
for (option, data) in list(metadata.items()):
    for alias in data["aliases"]:
        metadata[alias] = {
                    "category": data["category"],
                    "help": f"cf. `{option}`",
                }
rows = []
rows.append(("Sous-option", "Description", "Exemples", "Explications"))
rows.append(("--:", ":--", ":--", ":--"))
for (option, data) in sorted(metadata.items()):
    color = "green" if data["category"] == "rw" else "blue"
    title = f" title=\"Alias : {', '.join(data['aliases'])}.\"" if data.get("aliases") else ""
    option = f'<span{title} style="color:{color}; font-family:monospace; font-weight:600">{option}</span>'
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
table = "\n".join("| " + " | ".join(row) + " |" for row in rows)
text = f'- Opérations de <span style="color:blue; font-family:monospace; font-weight:600;">conversion en bleu</span> et de <span style="color:green; font-family:monospace; font-weight:600;">réécriture en vert</span>.\n- Survolez un nom d\'opération pour voir ses éventuels alias.\n\n{table}\n'
output_path = Path("doc/fr_cheat_sheet.md")
output_path.write_text(text)
print(f"File written: {output_path}")
