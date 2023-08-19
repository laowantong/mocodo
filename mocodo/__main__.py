from pathlib import Path
import sys

if sys.version_info < (3, 6):
    print(f"Mocodo requires Python 3.6 or later to run.\nThis version is {sys.version}.")
    sys.exit()

import importlib
import json
import os
from time import time
import requests

from .common import Common, safe_print_for_PHP
from .file_helpers import write_contents
from .argument_parser import parsed_arguments
from .mcd import Mcd
from .relations import Relations
from .font_metrics import font_metrics_factory
from .mcd_to_svg import main as mcd_to_svg
from .mocodo_error import MocodoError
from .tools.string_tools import urlsafe_encoding
from .tools.graphviz_tools import minify_graphviz
from .guess_title import may_update_params_with_guessed_title

RENDERING_SERVICES = {
    "gv": "https://kroki.io/graphviz/{output_format}/{payload}",
    "mmd": "https://kroki.io/mermaid/{output_format}/{payload}",
    "qr": "https://api.qrserver.com/v1/create-qr-code/?size=800x800&data={payload}",
}


def main():
    try:
        params = parsed_arguments()
        common = Common(params)
        source = common.load_input_file()
        get_font_metrics = font_metrics_factory(params)
        if params["restore"]:
            import shutil  # fmt: skip
            shutil.copyfile(
                os.path.join(params["script_directory"], "resources", "pristine_sandbox.mcd"),
                "sandbox.mcd",
            )
            return write_contents("params.json", "{}")
        if params["print_params"]:
            for added_key in params["added_keys"][:]:
                del params[added_key]
            params["print_params"] = False
            params_contents = json.dumps(params, ensure_ascii=False, indent=2, sort_keys=True)
            return safe_print_for_PHP(params_contents)
        if params["update"]:
            for (subopt, subargs) in params["update"]:
                if subopt == "flip":
                    mcd = Mcd(source, get_font_metrics, **params)
                    for subsubopt in subargs:
                        if subsubopt in ("v", "vertical"):
                            source = mcd.get_clauses_vertical_mirror()
                        elif subsubopt in ("h", "horizontal"):
                            source = mcd.get_clauses_horizontal_mirror()
                        elif subsubopt in ("d", "diagonal"):
                            source = mcd.get_clauses_diagonal_mirror()
                        else:
                            raise MocodoError(653, _("Unknown argument {subsubopt} for operation {subopt}".format(subsubopt=subsubopt, subopt=subopt)))  # fmt: skip
                elif subopt == "arrange":
                    mcd = Mcd(source, get_font_metrics, **params)
                    timeout = subargs.get("timeout")
                    has_expired = (lambda: time() > timeout) if timeout else (lambda: False)
                    algo = subargs.get("algo", "bb")
                    if algo == "bb":
                        # -u arrange -> non-constrained layout
                        # -u arrange:fit -> ... to the current grid
                        # -u arrange:fit=0 -> constrain the layout to the smallest balanced grid
                        # -u arrange:fit=𝑖 -> ... to the 𝑖th next grid (with 𝑖 > 0)
                        grid = subargs.get("grid")
                        if grid is None:
                            subargs["is_organic"] = True
                        elif grid.isdigit():
                            source = mcd.get_refitted_clauses(int(grid))
                            mcd = Mcd(source, get_font_metrics, **params)
                            subargs["is_organic"] = False
                    try:
                        module = importlib.import_module(f".update._arrange_{algo}", package="mocodo")
                    except ModuleNotFoundError:
                        raise MocodoError(654, _("Unknown algorithm {algo} for operation {subopt}".format(algo=algo, subopt=subopt)))
                    layout_data = mcd.get_layout_data()
                    rearrangement = module.arrange(layout_data, subargs, has_expired)
                    if rearrangement:
                        mcd.set_layout(**rearrangement)
                        source = mcd.get_clauses()
                    elif algo == "bb" and not subargs["is_organic"]:
                        raise MocodoError(9, _('Failed to calculate a planar layout on the given grid.'))  # fmt: skip
                    else:
                        raise MocodoError(41, _('Failed to calculate a planar layout.'))  # fmt: skip
                    continue
                else:
                    try:
                        module = importlib.import_module(f".update._{subopt}", package="mocodo")
                    except ModuleNotFoundError:
                        raise MocodoError(651, _("Unknown update operation: {op}".format(op=subopt)))  # fmt: skip
                    source = module.run(source, subargs=subargs, params=params).rstrip()
            # The source file is updated for further processing
            common.update_input_file(source)
        if "export" in params and params["export"]:
            things_to_be_displayed_path = Path(params["output_dir"]) / "things_to_be_displayed.tmp"
            things_to_be_displayed = []
            for (subopt, subargs) in params["export"]:
                try:
                    module = importlib.import_module(f".export._{subopt}", package="mocodo")
                except ModuleNotFoundError:
                    raise MocodoError(652, _("Unknown export operation: {op}".format(op=subopt)))  # fmt: skip
                result = module.run(source, subargs, common)
                result["output_name"] = params["output_name"]
                text = result["text"].rstrip()
                text_path = Path("{output_name}_{stem_suffix}.{extension}".format(**result))
                common.dump_file(text_path, f"{text}\n")
                if not result.get("displayable"):
                    continue
                rendering_service = RENDERING_SERVICES.get(result["extension"])
                if not rendering_service:
                    things_to_be_displayed.append(str(text_path))
                    continue
                if result["extension"] == "gv":
                    payload = minify_graphviz(text) # spare some bandwidth
                payload = urlsafe_encoding(text)
                for output_format in params.get("suck", []):
                    url = rendering_service.format(output_format=output_format, payload=payload)
                    response = requests.get(url)
                    if response.status_code != 200:
                        raise MocodoError(655, _("Failed to download the rendered document from the following url:\n{url}").format(url=url)) # fmt: skip
                    resp_path = text_path.with_suffix(f".{output_format}")
                    if response.headers["content-type"].startswith("text/"):
                        resp_path.write_text(response.text)
                    else:
                        resp_path.write_bytes(response.content)
                    things_to_be_displayed.append(str(resp_path))
            if things_to_be_displayed:
                things_to_be_displayed_path.write_text("\n".join(things_to_be_displayed))
            return
        mcd = Mcd(source, get_font_metrics, **params)
        if params["detect_overlaps"]:
            overlaps = mcd.get_overlaps()
            if overlaps:
                acc = []
                for (b1, b2, b3, b4) in overlaps:
                    if b3 == b4:
                        acc.append(_("- Leg “{b1} — {b2}” overlaps “{b3}”.").format(b1=b1, b2=b2, b3=b3))  # fmt: skip
                    else:
                        acc.append(_("- Legs “{b1} — {b2}” and “{b3} — {b4}” overlap.").format(b1=b1, b2=b2, b3=b3, b4=b4))  # fmt: skip
                details = "\n".join(acc)
                raise MocodoError(29, _('On Mocodo online, click the 🔀 button to fix the following problem(s):\n{details}').format(details=details))  # fmt: skip
        may_update_params_with_guessed_title(source, params)
        relations = Relations(mcd, params)
        # The order of the following two lines ensures that the relational diagram is dumped after
        # the geometry of the MCD. Later on, when drawing this relational diagram, the geometry
        # file is found to be older, and thus regenerated.
        mcd_to_svg(mcd, common)  # potential side-effect: update *_geo.json
        common.dump_mld_files(relations)  # potential side-effect: generate relation diagram
    except MocodoError as err:
        print(str(err), file=sys.stderr)
        sys.exit(err.errno)


if __name__ == "__main__":
    main()
