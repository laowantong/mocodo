import json
import os
from pathlib import Path

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.argument_parser import parsed_arguments
from mocodo.common import Common
from mocodo.font_metrics import font_metrics_factory
from mocodo.mcd import Mcd
from mocodo.mcd_to_svg import main as mcd_to_svg
from mocodo.relations import *


clauses = """
:
    PEUT COHABITER AVEC, 0N ESPÈCE, 0N [commensale] ESPÈCE: nb. max. commensaux
:
:
:

PEUT VIVRE DANS, 1N ESPÈCE, 1N ENCLOS: nb. max. congénères
ESPÈCE: code espèce, libellé
  DF, 0N ESPÈCE, _11 ANIMAL
:
  CARNIVORE: quantité viande

ENCLOS: num. enclos
      OCCUPE, 1N ANIMAL, 1N /PÉRIODE, 1N ENCLOS
  ANIMAL: nom, sexe, date naissance, date décès
  /\ ANIMAL <= CARNIVORE, HERBIVORE: type alimentation
:

:
      PÉRIODE: date début, _date fin
    A MÈRE, 01 ANIMAL, 0N> [mère] ANIMAL
:
  HERBIVORE: plante préférée
"""

snapshot_dir = Path("test/snapshots")
params = parsed_arguments()
params["title"] = "Untitled"
params["guess_title"] = False
params["output_name"] = f"{snapshot_dir}/snapshot"
common = Common(params)
get_font_metrics = font_metrics_factory(params)

result = []
result.append("# Snapshots")
result.append(f"## Source\n\n```{clauses}```\n")
mcd = Mcd(clauses.split("\n"), get_font_metrics, **params)
try:
  os.remove(snapshot_dir / "snapshot_geo.json")
except:
  pass
result.append(f"## SVG output\n")
mcd_to_svg(mcd, common)
result.append("![](snapshot_static.svg)\n")
os.remove(snapshot_dir / "snapshot.svg")

result.append(f"## Relational output\n")
relations = Relations(mcd, params)
for relation_path in Path("mocodo/resources/relation_templates/").glob("*.json"):
    template = json.loads(relation_path.read_text("utf8"))
    output = relations.get_text(template).strip()
    result.append(f"### `{relation_path.name}`\n\n```{template['highlight']}\n{output}\n```\n")

Path(f"{snapshot_dir}/snapshot.md").write_text("\n".join(result))
