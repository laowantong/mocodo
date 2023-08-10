import sys

if sys.version_info < (3, 6):
    print(f"Mocodo requires Python 3.6 or later to run.\nThis version is {sys.version}.")
    sys.exit()

import importlib
import os
from .common import Common, safe_print_for_PHP
from .file_helpers import write_contents
from .argument_parser import parsed_arguments
from .mcd import Mcd
from .relations import Relations
from .font_metrics import font_metrics_factory
from .mcd_to_svg import main as mcd_to_svg
from .mocodo_error import MocodoError
from .dump import data_dict

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
            import json  # fmt: skip
            for added_key in params["added_keys"][:]:
                del params[added_key]
            params["print_params"] = False
            params_contents = json.dumps(params, ensure_ascii=False, indent=2, sort_keys=True)
            return safe_print_for_PHP(params_contents)
        if params["modify"] != ["echo"]:
            for sub_option in params["modify"]:
                if sub_option == "echo":
                    continue
                if "_" in sub_option:
                    # Beware that, in the following line, using a single underscore would clash
                    # with the gettext alias, EVEN IF THIS CODE IS NOT REACHED: the compiler would
                    # consider that _ is a local variable, and shadow the global one, resulting in:
                    # UnboundLocalError: local variable '_' referenced before assignment
                    (operation, __, token) = sub_option.partition("_")
                    module = importlib.import_module(f".modify.op_tk", package="mocodo")
                    if operation in module.OPERATIONS:
                        try:
                            source = module.run(source, operation, token).rstrip()
                        except:
                            raise MocodoError(650, _('Unable to apply "{op}" to "{tk}".').format(op=operation, tk=token))  # fmt: skip
                        continue
                    # Now we know that s in not of the form "operation_token"
                if "flip" in sub_option:
                    mcd = Mcd(source, get_font_metrics, **params)
                    s = sub_option.replace("flip", "").replace("_", "")
                    if s.startswith("v"):
                        source = mcd.get_clauses_vertical_mirror()
                    elif s.startswith("h"):
                        source = mcd.get_clauses_horizontal_mirror()
                    else:
                        source = mcd.get_clauses_diagonal_mirror()
                    continue
                if sub_option.startswith("arrange"):
                    # Possible sub-commands:
                    # - arrange_organic: non-constrained layout
                    # - arrange_0: constrain the layout to the smallest balanced grid
                    # - arrange_𝑖: ... to the 𝑖th next grid (with 𝑖 > 0)
                    # - arrange (and any other suffix): ... to the current grid
                    mcd = Mcd(source, get_font_metrics, **params)
                    s = sub_option.replace("arrange_", "")
                    if s.isdigit():
                        source = mcd.get_refitted_clauses(int(s))
                        mcd = Mcd(source, get_font_metrics, **params)
                    module = importlib.import_module(f".modify.arrange_{params['arrangement']}", package="mocodo")
                    params.update(mcd.get_layout_data())
                    params["organic"] = (s == "organic")
                    rearrangement = module.arrange(**params)
                    if rearrangement:
                        mcd.set_layout(**rearrangement)
                        source = mcd.get_clauses()
                    elif s == "organic":
                        raise MocodoError(41, _('Failed to calculate a planar layout.'))  # fmt: skip
                    else:
                        raise MocodoError(9, _('Failed to calculate a planar layout on the given grid.'))  # fmt: skip
                    continue
                try:
                    module = importlib.import_module(f".modify.{sub_option}", package="mocodo")
                except ModuleNotFoundError:
                    raise MocodoError(651, _("Unknown modification operation: {op}".format(op=sub_option)))  # fmt: skip
                source = module.run(source, params=params).rstrip()
            # The source file is updated for further processing
            common.update_input_file(source)
        if "dump" in params and params["dump"]:
            for sub_option in params["dump"]:
                try:
                    module = importlib.import_module(f".dump.{sub_option}", package="mocodo")
                except ModuleNotFoundError:
                    raise MocodoError(652, _("Unknown dump operation: {op}".format(op=sub_option)))  # fmt: skip
                text = module.run(source, params).rstrip()
                common.dump_file(module.FILENAME_SUFFIX, f"{text}\n")
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
