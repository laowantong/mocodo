#!/usr/bin/env python
# encoding: utf-8

from __future__ import division, print_function

import sys
if sys.version < "2.7":
    print("Mocodo requires Python 2.7 or later to run.\nThis version is {version}.".format(version=sys.version))
    sys.exit()

import os
from .common import Common, safe_print_for_PHP
from .file_helpers import write_contents
from .argument_parser import parsed_arguments
from .mcd import Mcd
from .relations import Relations
from .font_metrics import font_metrics_factory
from .mocodo_error import MocodoError

def main():
    try:
        params = parsed_arguments()
        common = Common(params)
        clauses = common.load_input_file()
        get_font_metrics = font_metrics_factory(params)
        if params["restore"]:
            import shutil
            shutil.copyfile(os.path.join(params["script_directory"], "pristine_sandbox.mcd"), "sandbox.mcd")
            return write_contents("params.json", "{}")
        if params["print_params"]:
            import json
            for added_key in params["added_keys"][:]:
                del params[added_key]
            params["print_params"] = False
            params_contents = json.dumps(params, ensure_ascii=False, indent=2, sort_keys=True)
            return safe_print_for_PHP(params_contents)
        if params["obfuscate"]:
            from .obfuscate import obfuscate
            return safe_print_for_PHP(obfuscate(clauses, params))
        mcd = Mcd(clauses, params, get_font_metrics)
        if params["fit"] is not None:
            return safe_print_for_PHP(mcd.get_reformatted_clauses(params["fit"]))
        if params["flip"]:
            return safe_print_for_PHP({
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
            elif params["arrange"] == "lp":
                from .arrange_lp import arrange
            result = arrange(**params)
            if result:
                mcd.set_layout(**result)
                return safe_print_for_PHP(mcd.get_clauses())
            raise MocodoError(9, _('Failed to calculate a planar layout.'))
        relations = Relations(mcd, params)
        common.dump_mld_files(relations)
        if params["image_format"] == "svg":
            from .mcd_to_svg import main
            import runpy
            main(mcd, common)
            runpy.run_path(u"%(output_name)s_svg.py" % params)
            return
        if params["image_format"] == "nodebox":
            from .mcd_to_nodebox import main
            main(mcd, common)
            return os.system(u"""open -a NodeBox "%(output_name)s_nodebox.py" """ % params)
        raise MocodoError(13, _('Should never happen.'))
    except MocodoError as err:
        print(str(err), file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main())
