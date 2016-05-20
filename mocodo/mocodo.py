#!/usr/bin/env python
# encoding: utf-8

import sys
if sys.version < "2.6" or sys.version >= "3":
    print "Mocodo requires Python 2.7 to run.\nThis version is {version}.".format(version=sys.version)
    sys.exit()

import os
from common import Common, safe_print_for_PHP
from file_helpers import write_contents
from argument_parser import parsed_arguments
from mcd import Mcd
from relations import Relations

def main():
    try:
        params = parsed_arguments()
        common = Common(params)
        clauses = common.load_input_file()
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
            from obfuscate import obfuscate
            return safe_print_for_PHP(obfuscate(clauses, params))
        mcd = Mcd(clauses, params)
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
                from arrange_ga import arrange
            elif params["arrange"] == "bb":
                from arrange_bb import arrange
            result = arrange(**params)
            if result:
                return safe_print_for_PHP(mcd.get_clauses_from_layout(**result))
            raise RuntimeError(("Mocodo Err.9 - " + _('Failed to calculate a planar layout.')).encode("utf8"))
        relations = Relations(mcd, params)
        common.dump_mld_files(relations)
        if params["image_format"] == "svg":
            import mcd_to_svg, runpy
            mcd_to_svg.main(mcd, common)
            runpy.run_path(u"%(output_name)s_svg.py" % params)
            return
        if params["image_format"] == "nodebox":
            import mcd_to_nodebox
            mcd_to_nodebox.main(mcd, common)
            return os.system(u"""open -a NodeBox "%(output_name)s_nodebox.py" """ % params)
        raise RuntimeError(("Mocodo Err.13 - " + _('Should never happen.')).encode("utf8"))
    except RuntimeError, err:
        msg = str(err)
        if msg.startswith("Mocodo Err."):
            print >> sys.stderr, msg
        else:
            raise


if __name__ == "__main__":
    sys.exit(main())
