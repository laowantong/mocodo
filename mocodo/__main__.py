import sys

if sys.version_info < (3, 6):
    print(f"Mocodo requires Python 3.6 or later to run.\nThis version is {sys.version}.")
    sys.exit()

import os
from .common import Common, safe_print_for_PHP
from .file_helpers import write_contents
from .argument_parser import parsed_arguments
from .mcd import Mcd
from .relations import Relations
from .font_metrics import font_metrics_factory
from .mcd_to_svg import main as mcd_to_svg
from .mocodo_error import MocodoError


def main():
    try:
        params = parsed_arguments()
        common = Common(params)
        clauses = common.load_input_file()
        get_font_metrics = font_metrics_factory(params)
        if params["restore"]:
            import shutil  # fmt: skip
            shutil.copyfile(
                os.path.join(params["script_directory"], "resources", "pristine_sandbox.mcd"),
                "sandbox.mcd",
            )
            return write_contents("params.json", "{}")
        if params["print_params"]:
            import json  # fmt: skip
            for added_key in params["added_keys"][:]:
                del params[added_key]
            params["print_params"] = False
            params_contents = json.dumps(params, ensure_ascii=False, indent=2, sort_keys=True)
            return safe_print_for_PHP(params_contents)
        if params["obfuscate"]:
            from .obfuscate import obfuscate  # fmt: skip
            return safe_print_for_PHP(obfuscate(clauses, params))
        mcd = Mcd(clauses, get_font_metrics, **params)
        if params["fit"] is not None:
            return safe_print_for_PHP(mcd.get_reformatted_clauses(params["fit"]))
        if params["flip"]:
            return safe_print_for_PHP(
                {
                    "v": mcd.get_clauses_vertical_mirror,
                    "h": mcd.get_clauses_horizontal_mirror,
                    "d": mcd.get_clauses_diagonal_mirror,
                }[params["flip"]]()
            )
        if params["arrange"]:
            params.update(mcd.get_layout_data())
            if params["arrange"] == "ga":
                from .arrange_ga import arrange
            elif params["arrange"] == "bb":
                from .arrange_bb import arrange
            result = arrange(**params)
            if result:
                mcd.set_layout(**result)
                return safe_print_for_PHP(mcd.get_clauses())
            raise MocodoError(9, _('Failed to calculate a planar layout.'))  # fmt: skip
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
